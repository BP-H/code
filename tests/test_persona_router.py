from fastapi.testclient import TestClient
from api import persona_router as pr
import persona_selector as ps


def test_merge_persona_404(monkeypatch):
    monkeypatch.setattr(ps, "PERSONAS", {})
    with TestClient(pr.app) as client:
        resp = client.post("/merge_persona", json={"id": 999})
        assert resp.status_code == 404
        assert resp.json() == {"detail": "Persona not found – check ID or path"}

