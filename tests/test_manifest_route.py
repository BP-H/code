from fastapi.testclient import TestClient
from api.character_router import app, MANIFEST


def test_manifest_yaml_route():
    client = TestClient(app)
    resp = client.get("/manifest.yaml")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/plain")
    assert resp.text == MANIFEST.read_text(encoding="utf-8")
