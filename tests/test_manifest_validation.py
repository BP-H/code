import yaml
import pytest
import api.character_router as cr


def test_manifest_requires_prompt_file(tmp_path, monkeypatch):
    m = tmp_path / "manifest.yaml"
    m.write_text(yaml.safe_dump([{"id": "x", "entrypoint": "e"}]))
    monkeypatch.setattr(cr, "MANIFEST", m)
    with pytest.raises(ValueError):
        cr._load_manifest()


def test_manifest_requires_entrypoint(tmp_path, monkeypatch):
    m = tmp_path / "manifest.yaml"
    m.write_text(yaml.safe_dump([{"id": "x", "prompt_file": "p"}]))
    monkeypatch.setattr(cr, "MANIFEST", m)
    with pytest.raises(ValueError):
        cr._load_manifest()


def test_manifest_requires_id(tmp_path, monkeypatch):
    m = tmp_path / "manifest.yaml"
    m.write_text(yaml.safe_dump([{"prompt_file": "p", "entrypoint": "e"}]))
    monkeypatch.setattr(cr, "MANIFEST", m)
    with pytest.raises(ValueError):
        cr._load_manifest()


def test_manifest_must_be_list(tmp_path, monkeypatch):
    m = tmp_path / "manifest.yaml"
    m.write_text(
        yaml.safe_dump({"id": "x", "prompt_file": "p", "entrypoint": "e"})
    )
    monkeypatch.setattr(cr, "MANIFEST", m)
    with pytest.raises(ValueError):
        cr._load_manifest()
