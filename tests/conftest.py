import collections
import pytest
import fakeredis
from api import character_router as cr

@pytest.fixture(autouse=True)
def fake_redis(monkeypatch):
    fake = fakeredis.FakeRedis()
    monkeypatch.setattr(cr, "r", fake)
    monkeypatch.setattr(cr, "_fallback_counter", collections.Counter())
    monkeypatch.setattr(cr, "_redis_client", fake, raising=False)
    monkeypatch.setattr(cr, "get_redis", lambda: fake, raising=False)
    return fake
