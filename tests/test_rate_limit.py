import redis
from fastapi import HTTPException
import api.character_router as cr
from api import rate_limit


def test_rate_limit_redis_down(monkeypatch):
    def boom(*args, **kwargs):
        raise redis.exceptions.ConnectionError

    monkeypatch.setattr(cr.r, "incr", boom)
    try:
        rate_limit("1.1.1.1")
    except HTTPException as exc:
        assert exc.status_code == 503
        assert exc.detail == "Rate limiter unavailable"
    else:
        assert False, "HTTPException not raised"

