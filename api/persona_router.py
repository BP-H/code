from fastapi import FastAPI, HTTPException, Body
from pathlib import Path
import persona_selector as ps

app = FastAPI(title="Persona Merge API")

@app.post("/merge_persona")
def merge_persona(id: int = Body(...)):
    """Return merged instruction and knowledge text for persona ``id``."""
    persona = ps.PERSONAS.get(str(id))
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found – check ID or path")
    _, instr, know = persona
    instr_path = ps.find_file(instr)
    know_path = ps.find_file(know)
    if not instr_path or not know_path:
        raise HTTPException(status_code=404, detail="Persona not found – check ID or path")
    try:
        merged = (
            Path(instr_path).read_text(encoding="utf-8").rstrip()
            + "\n\n"
            + Path(know_path).read_text(encoding="utf-8").lstrip()
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Persona not found – check ID or path") from exc
    return {"text": merged}
