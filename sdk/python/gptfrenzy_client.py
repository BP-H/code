import requests, json, typing as _t


class GPTFrenzyClient:
    """Super-light client for GPTFrenzy."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base = base_url.rstrip("/")

    def chat(self, character: str, message: str) -> str:
        r = requests.post(
            f"{self.base}/chat",
            json={"character": character, "message": message},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()["reply"]

    def chat_stream(self, character: str, message: str) -> _t.Iterator[str]:
        """Yield the reply as tokens using server-sent events."""
        r = requests.post(
            f"{self.base}/chat/stream",
            json={"character": character, "message": message},
            stream=True,
            timeout=30,
        )
        r.raise_for_status()
        try:
            for line in r.iter_lines(decode_unicode=True):
                if line.startswith("data: "):
                    yield line[6:]
        finally:
            r.close()

    def manifest(self) -> _t.List[dict]:
        return requests.get(f"{self.base}/manifest", timeout=10).json()
