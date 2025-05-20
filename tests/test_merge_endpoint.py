import types as _types
from fastapi.testclient import TestClient
import api.character_router as cr
import persona_selector as ps


def _mock_rate_limit(monkeypatch):
    monkeypatch.setattr(cr.r, "incr", lambda *a, **kw: 1)
    monkeypatch.setattr(cr.r, "expire", lambda *a, **kw: None)


def test_merge(monkeypatch, tmp_path):
    _mock_rate_limit(monkeypatch)
    # openai not used but mock to follow other tests
    monkeypatch.setattr(cr.client.chat.completions, "create", lambda *a, **kw: None)

    instr = tmp_path / "instruction.txt"
    know = tmp_path / "knowledge.txt"
    instr.write_text("hello\n")
    know.write_text("\nworld")

    monkeypatch.setattr(ps, "PERSONAS", {"1": ("Test", str(instr), str(know))})
    monkeypatch.setattr(ps, "SEARCH_DIRS", [str(tmp_path)])

    with TestClient(cr.app) as client:
        resp = client.post("/merge", json={"id": 1})
        assert resp.status_code == 200
        assert resp.json() == {"text": "hello\n\nworld"}
