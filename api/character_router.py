from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, PlainTextResponse
from pydantic import BaseModel
import os
import time
import redis
import yaml
import pathlib
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BASE = pathlib.Path(__file__).parent.parent
PERSONA_DIR = BASE / "personas"
MANIFEST = BASE / "manifest.yaml"
PROMPTS = {}
# Allow the Redis host and port to be configured via environment variables so
# the API can connect to external instances when needed. Prefer a single
# REDIS_URL if provided for full flexibility.
redis_url = os.getenv("REDIS_URL")
if not redis_url:
    host = os.getenv("REDIS_HOST", "redis")
    port = int(os.getenv("REDIS_PORT", "6379"))
    redis_url = f"redis://{host}:{port}/0"
r = redis.from_url(redis_url, decode_responses=True)
app = FastAPI()

# --- CORS so browsers, WebGL & mobile apps can hit us directly ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load_manifest():
    with MANIFEST.open(encoding="utf-8") as f:
        return {d["id"]: d for d in yaml.safe_load(f)}


def _prime_prompts():
    for pid, data in _load_manifest().items():
        PROMPTS[pid] = (PERSONA_DIR / data["prompt_file"]).read_text(encoding="utf-8")


_prime_prompts()


class Msg(BaseModel):
    character: str
    message: str


def rate_limit(ip, limit=60):
    key = f"rl:{ip}:{int(time.time())//60}"
    try:
        if r.incr(key) > limit:
            raise HTTPException(429, "Rate limit exceeded")
        r.expire(key, 61)
    except redis.exceptions.ConnectionError as exc:
        raise HTTPException(status_code=503, detail="Rate limiter unavailable") from exc


@app.post("/chat")
def chat(req: Msg, request: Request):
    rate_limit(request.client.host)
    reply = (
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PROMPTS[req.character]},
                {"role": "user", "content": req.message},
            ],
        )
        .choices[0]
        .message.content
    )
    return {"reply": reply}


@app.post("/chat/stream")
def chat_stream(req: Msg, request: Request):
    rate_limit(request.client.host)

    def gen():
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PROMPTS[req.character]},
                {"role": "user", "content": req.message},
            ],
            stream=True,
        )
        for c in resp:
            if "content" in c.choices[0].delta:
                yield c.choices[0].delta.content

    return StreamingResponse(gen(), media_type="text/event-stream")


# ------------------------------------------------------------------------
# Health-check for load balancers / Kubernetes
@app.get("/")
def root():
    return {"status": "ok"}


# Serve manifest as JSON so SDKs auto-discover characters
@app.get("/manifest")
def get_manifest():
    return _load_manifest()


@app.get("/manifest.yaml", response_class=PlainTextResponse)
def get_manifest_yaml():
    """Return the raw manifest file as plain text."""
    return MANIFEST.read_text(encoding="utf-8")
