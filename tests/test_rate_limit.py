import redis
from fastapi import HTTPException
from api import character_router as cr
from api import rate_limit


def test_rate_limit_redis_down(monkeypatch):
    class BoomRedis:
        def incr(self, *args, **kwargs):
            raise redis.exceptions.ConnectionError

        def expire(self, *args, **kwargs):
            pass

    monkeypatch.setattr(cr, "get_redis", lambda: BoomRedis())
    try:
        rate_limit("1.1.1.1")
    except HTTPException as exc:
        assert exc.status_code == 503
        assert exc.detail == "Rate limiter unavailable"
    else:
        assert False, "HTTPException not raised"

