import yaml
import asyncio
from gptfrenzy.core.spawn import launch, make_manifest


def test_manifest_load_success(tmp_path):
    d = tmp_path / "persona"
    d.mkdir()
    make_manifest(d)
    (d / "persona.py").write_text(
        "class Persona:\n    def __init__(self, **k): pass\n    def generate(self, t): return t.upper()"
    )
    inst = launch("discord", str(d))
    assert asyncio.run(inst.generate("hi")) == "HI"


def test_capability_flags(tmp_path):
    d = tmp_path / "persona"
    d.mkdir()
    manifest = {
        "sap_version": "0.3",
        "entrypoint": "gptfrenzy.core.spawn:launch",
        "assets": [],
        "capabilities": ["text", "voice"],
        "license_ref": "./LICENSE_PERSONAS",
    }
    (d / "manifest.yaml").write_text(yaml.safe_dump(manifest))
    (d / "persona.py").write_text(
        "class Persona:\n    def __init__(self, **k): pass\n    def generate(self, t): return t\n    def speak(self, a=None): return 'ok'"
    )
    inst = launch("unreal", str(d))
    assert hasattr(inst, "generate")
    assert hasattr(inst, "speak")
    assert not hasattr(inst, "embody")


def test_invalid_version_raises(tmp_path):
    d = tmp_path / "persona"
    d.mkdir()
    (d / "manifest.yaml").write_text(
        yaml.safe_dump({"sap_version": "0.2", "entrypoint": "x"})
    )
    try:
        launch("host", str(d))
    except ValueError:
        pass
    else:
        assert False, "ValueError not raised"


def test_missing_manifest(tmp_path):
    d = tmp_path / "persona"
    d.mkdir()
    (d / "persona.py").write_text("class Persona:\n    def __init__(self, **k): pass")
    try:
        launch("host", str(d))
    except ValueError as e:
        assert "manifest.yaml missing or unreadable" in str(e)
    else:
        assert False, "ValueError not raised"


def test_bad_manifest_yaml(tmp_path):
    d = tmp_path / "persona"
    d.mkdir()
    (d / "manifest.yaml").write_text(":\n")
    (d / "persona.py").write_text("class Persona:\n    def __init__(self, **k): pass")
    try:
        launch("host", str(d))
    except ValueError as e:
        assert "manifest.yaml missing or unreadable" in str(e)
    else:
        assert False, "ValueError not raised"


def test_async_speak(tmp_path):
    d = tmp_path / "persona"
    d.mkdir()
    manifest = {
        "sap_version": "0.3",
        "entrypoint": "gptfrenzy.core.spawn:launch",
        "assets": [],
        "capabilities": ["text", "voice"],
        "license_ref": "./LICENSE_PERSONAS",
    }
    (d / "manifest.yaml").write_text(yaml.safe_dump(manifest))
    (d / "persona.py").write_text(
        "class Persona:\n"
        "    def __init__(self, **k): pass\n"
        "    async def generate(self, t): return t\n"
        "    async def speak(self, a=None): return 'async'"
    )
    inst = launch("host", str(d))
    assert asyncio.run(inst.speak()) == "async"


def test_async_embody(tmp_path):
    d = tmp_path / "persona"
    d.mkdir()
    manifest = {
        "sap_version": "0.3",
        "entrypoint": "gptfrenzy.core.spawn:launch",
        "assets": [],
        "capabilities": ["text", "realtime_embodiment"],
        "license_ref": "./LICENSE_PERSONAS",
    }
    (d / "manifest.yaml").write_text(yaml.safe_dump(manifest))
    (d / "persona.py").write_text(
        "class Persona:\n"
        "    def __init__(self, **k): pass\n"
        "    async def generate(self, t): return t\n"
        "    async def embody(self, *a, **kw): return 'done'"
    )
    inst = launch("host", str(d))
    assert asyncio.run(inst.embody()) == "done"


def test_custom_entrypoint(tmp_path):
    d = tmp_path / "persona"
    d.mkdir()
    (d / "persona.py").write_text("class Persona: pass")
    (d / "custom_entry.py").write_text(
        "def alt_launch(host, path, **kw):\n    return {'called': True, 'h': host, 'p': path}"
    )
    manifest = {
        "sap_version": "0.3",
        "entrypoint": "custom_entry:alt_launch",
        "assets": [],
        "capabilities": ["text"],
        "license_ref": "./LICENSE_PERSONAS",
    }
    (d / "manifest.yaml").write_text(yaml.safe_dump(manifest))
    import sys

    sys.path.insert(0, str(d))
    try:
        res = launch("host", str(d))
    finally:
        sys.path.remove(str(d))
    assert res == {"called": True, "h": "host", "p": str(d)}
