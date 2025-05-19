import requests, json, typing as _t


class GPTFrenzyClient:
    """Super-light client—no asyncio, no streaming."""

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

    def manifest(self) -> _t.List[dict]:
        return requests.get(f"{self.base}/manifest", timeout=10).json()
