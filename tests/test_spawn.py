import yaml
from gptfrenzy.spawn import launch, make_manifest


def test_manifest_load_success(tmp_path):
    d = tmp_path / "persona"
    d.mkdir()
    make_manifest(d)
    (d / "persona.py").write_text(
        "class Persona:\n    def __init__(self, **k): pass\n    def generate(self, t): return t.upper()"
    )
    inst = launch("discord", str(d))
    assert inst.generate("hi") == "HI"


def test_capability_flags(tmp_path):
    d = tmp_path / "persona"
    d.mkdir()
    manifest = {
        "sap_version": "0.3",
        "entrypoint": "gptfrenzy.spawn:launch",
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
