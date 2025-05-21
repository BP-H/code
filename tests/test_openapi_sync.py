import json
from pathlib import Path

from scripts import generate_openapi


def test_openapi_json_is_up_to_date(tmp_path):
    temp = tmp_path / "openapi.json"
    generate_openapi.generate(temp)

    generated = json.loads(temp.read_text())
    existing = json.loads(Path("openapi.json").read_text())

    assert generated == existing, "openapi.json is out of date, run `make openapi`"
