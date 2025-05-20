from fastapi.testclient import TestClient
from api import character_router as cr


def _setup_persona(tmp_path, missing_instr=False, missing_know=False):
    d = tmp_path / "1"
    d.mkdir()
    if not missing_instr:
        (d / "test_GPT_INSTRUCTIONS.txt").write_text("hello\n")
    if not missing_know:
        (d / "test_DEEP_KNOWLEDGE_data.txt").write_text("\nworld")
    return d


def test_merge_success(monkeypatch, tmp_path):
    _setup_persona(tmp_path)
    monkeypatch.setattr(cr, "PERSONA_DIR", tmp_path)
    with TestClient(cr.app) as client:
        resp = client.post("/merge", json={"id": 1})
        assert resp.status_code == 200
        assert resp.json() == {"merged": "hello\n\nworld"}


def test_merge_missing_instr(monkeypatch, tmp_path):
    _setup_persona(tmp_path, missing_instr=True)
    monkeypatch.setattr(cr, "PERSONA_DIR", tmp_path)
    with TestClient(cr.app) as client:
        resp = client.post("/merge", json={"id": 1})
        assert resp.status_code == 422


def test_merge_missing_know(monkeypatch, tmp_path):
    _setup_persona(tmp_path, missing_know=True)
    monkeypatch.setattr(cr, "PERSONA_DIR", tmp_path)
    with TestClient(cr.app) as client:
        resp = client.post("/merge", json={"id": 1})
        assert resp.status_code == 422

