import importlib
import sys
import types
from fastapi.testclient import TestClient
import pytest


def test_missing_openai_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    # stub openai.ChatCompletion.create so we can detect if it's called
    called = False

    def fail(*a, **kw):
        nonlocal called
        called = True
        raise AssertionError("OpenAI should not be called")

    sys.modules.setdefault(
        "openai", types.SimpleNamespace(ChatCompletion=types.SimpleNamespace(create=fail))
    )

    import api.character_router as cr
    importlib.reload(cr)

    assert cr.client is None

    with TestClient(cr.app) as client:
        resp = client.get("/")
        assert resp.status_code == 200
        resp = client.post(
            "/chat", json={"character": "blueprint-nova", "message": "hi"}
        )
        assert resp.status_code == 503
        assert "OpenAI API key" in resp.json()["detail"]

    assert called is False
