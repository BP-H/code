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
import logging

log = logging.getLogger(__name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Allow callers to set the OpenAI model via env with a sensible default so we
# can easily swap models when deploying.
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
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
app = FastAPI(title="GPT Frenzy API")

# --- CORS so browsers, WebGL & mobile apps can hit us directly ----------
# Allow callers to restrict origins via ALLOWED_ORIGINS. Provide a comma-
# separated list or "*" for the default open policy.
_origins = os.getenv("ALLOWED_ORIGINS", "*")
if _origins == "*":
    allow_origins = ["*"]
else:
    allow_origins = [o.strip() for o in _origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load_manifest():
    """Return the manifest as a dict keyed by persona id."""
    try:
        with MANIFEST.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"manifest file not found: {MANIFEST}") from exc

    if not isinstance(data, list):
        raise ValueError("manifest must be a list of entries")

    manifest = {}
    for idx, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise ValueError(f"Invalid manifest entry at {MANIFEST}:{idx}")

        missing = [
            key
            for key in ("id", "prompt_file", "entrypoint")
            if not entry.get(key)
        ]
        if missing:
            missing_keys = ", ".join(missing)
            raise ValueError(
                f"Manifest entry {MANIFEST}:{idx} missing {missing_keys}"
            )

        manifest[entry["id"]] = entry

    return manifest


def _prime_prompts():
    log = logging.getLogger(__name__)
    try:
        manifest = _load_manifest()
    except FileNotFoundError as exc:
        log.warning("Manifest not found: %s", exc)
        return
    except (yaml.YAMLError, ValueError) as exc:
        log.warning("Failed to load manifest: %s", exc)
        return

    for pid, data in manifest.items():
        try:
            PROMPTS[pid] = (PERSONA_DIR / data["prompt_file"]).read_text(
                encoding="utf-8"
            )
        except FileNotFoundError as exc:
            log.warning("Prompt file for '%s' missing: %s", pid, exc)

_prime_prompts()


class Msg(BaseModel):
    character: str
    message: str


def rate_limit(ip, limit=60):
    key = f"rl:{ip}:{int(time.time())//60}"
    try:
        count = r.incr(key)
        # Expire first so new keys always get a TTL even when over limit
        r.expire(key, 61)
        if count > limit:
            raise HTTPException(429, "Rate limit exceeded")
    except redis.exceptions.ConnectionError as exc:
        raise HTTPException(status_code=503, detail="Rate limiter unavailable") from exc


@app.post("/chat")
def chat(req: Msg, request: Request):
    rate_limit(request.client.host)
    if req.character not in PROMPTS:
        raise HTTPException(status_code=404, detail="Persona not found")
    try:
        reply = (
            client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": PROMPTS[req.character]},
                    {"role": "user", "content": req.message},
                ],
            )
            .choices[0]
            .message.content
        )
    except Exception as exc:
        log.exception("OpenAI API request failed: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=f"⚠️ Sorry, something went wrong: {exc}"
        ) from exc
    return {"reply": reply}


@app.post("/chat/stream")
def chat_stream(req: Msg, request: Request):
    rate_limit(request.client.host)
    if req.character not in PROMPTS:
        raise HTTPException(status_code=404, detail="Persona not found")

    def gen():
        try:
            resp = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": PROMPTS[req.character]},
                    {"role": "user", "content": req.message},
                ],
                stream=True,
            )
            for c in resp:
                if "content" in c.choices[0].delta:
                    token = c.choices[0].delta.content
                    yield f"data: {token}\n\n"
        except Exception as exc:
            log.exception("OpenAI API request failed: %s", exc)
            raise HTTPException(
                status_code=502,
                detail=f"⚠️ Sorry, something went wrong: {exc}"
            ) from exc

    return StreamingResponse(gen(), media_type="text/event-stream")


# ------------------------------------------------------------------------
# Health-check for load balancers / Kubernetes
@app.get("/")
def root():
    return {"status": "ok"}


# Serve manifest as JSON so SDKs auto-discover characters
@app.get("/manifest")
def get_manifest():
    try:
        return _load_manifest()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Manifest file not found") from exc
    except (yaml.YAMLError, ValueError) as exc:
        log.warning("Failed to load manifest: %s", exc)
        raise HTTPException(status_code=500, detail="Invalid manifest file") from exc


@app.get("/manifest.yaml", response_class=PlainTextResponse)
def get_manifest_yaml():
    """Return the raw manifest file as plain text."""
    return MANIFEST.read_text(encoding="utf-8")
