import yaml
import pytest
import api.character_router as cr


def test_manifest_requires_prompt_file(tmp_path, monkeypatch):
    m = tmp_path / "manifest.yaml"
    m.write_text(yaml.safe_dump([{"id": "x"}]))
    monkeypatch.setattr(cr, "MANIFEST", m)
    with pytest.raises(ValueError):
        cr._load_manifest()
