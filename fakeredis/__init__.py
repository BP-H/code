class FakeRedis:
    """Very small subset of fakeredis.FakeRedis for tests."""

    def __init__(self):
        self._data = {}

    def incr(self, key):
        self._data[key] = self._data.get(key, 0) + 1
        return self._data[key]

    def expire(self, key, ttl):
        # TTL ignored but kept for interface compatibility
        pass
