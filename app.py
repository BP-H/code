import json
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import persona_selector as ps

app = FastAPI(title="Persona Selector API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/personas")
def get_personas():
    """Return available persona IDs."""
    return list(ps.PERSONAS.keys())


def _merge_text(pid: str) -> str:
    persona = ps.PERSONAS.get(pid)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    _, instr, know = persona
    instr_path = ps.find_file(instr)
    know_path = ps.find_file(know)
    if not (instr_path and know_path):
        raise HTTPException(status_code=404, detail="Files missing")
    with open(instr_path, "r", encoding="utf-8") as f:
        merged = f.read().rstrip() + "\n\n"
    with open(know_path, "r", encoding="utf-8") as f:
        merged += f.read().lstrip()
    return merged


@app.post("/merge")
def merge(id: int):
    """Return merged instruction and knowledge text."""
    return {"text": _merge_text(str(id))}


if __name__ == "__main__":
    if "--openapi" in sys.argv:
        import types
        sys.modules.setdefault(
            "redis",
            types.SimpleNamespace(
                from_url=lambda *a, **kw: types.SimpleNamespace(),
                exceptions=types.SimpleNamespace(ConnectionError=Exception),
            ),
        )
        sys.modules.setdefault("yaml", types.SimpleNamespace(safe_load=lambda *_: []))
        sys.modules.setdefault("openai", types.SimpleNamespace(OpenAI=lambda *a, **kw: object()))

        from api.character_router import app as character_app

        with open("openapi.json", "w", encoding="utf-8") as f:
            json.dump(character_app.openapi(), f, indent=2)
    else:
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=8000)
