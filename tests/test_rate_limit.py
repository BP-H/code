import redis
import collections
import pytest
from fastapi import HTTPException
from api import character_router as cr
from api import rate_limit


def test_rate_limit_redis_down(monkeypatch):
    class BoomRedis:
        def incr(self, *args, **kwargs):
            raise redis.exceptions.ConnectionError

        def expire(self, *args, **kwargs):
            raise redis.exceptions.ConnectionError

    monkeypatch.setattr(cr, "r", BoomRedis())
    monkeypatch.setattr(cr, "_fallback_counter", collections.Counter())
    rate_limit("1.1.1.1", limit=1)
    with pytest.raises(HTTPException) as exc:
        rate_limit("1.1.1.1", limit=1)
    assert exc.value.status_code == 429

