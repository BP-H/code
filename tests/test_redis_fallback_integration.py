import importlib
import sys
import types
from fastapi.testclient import TestClient
import pytest


# override the autouse fake_redis fixture
@pytest.fixture(autouse=True)
def fake_redis():
    pass


def test_fallback_to_fakeredis(monkeypatch):
    monkeypatch.setenv("REDIS_URL", "redis://does-not-exist")
    sys.modules.setdefault(
        "openai", types.SimpleNamespace(OpenAI=lambda *a, **kw: object())
    )
    import api.character_router as cr

    importlib.reload(cr)
    with TestClient(cr.app) as client:
        resp = client.get("/")
        assert resp.status_code == 200


def test_use_fake_redis_env(monkeypatch):
    monkeypatch.setenv("USE_FAKE_REDIS", "1")
    sys.modules.setdefault(
        "openai", types.SimpleNamespace(OpenAI=lambda *a, **kw: object())
    )
    import api.character_router as cr

    importlib.reload(cr)
    with TestClient(cr.app) as client:
        resp = client.get("/")
        assert resp.status_code == 200
