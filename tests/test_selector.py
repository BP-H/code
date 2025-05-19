import persona_selector as ps


def _make_persona(tmp_path, name):
    d = tmp_path / name
    d.mkdir()
    (d / "instruction.txt").write_text("i")
    (d / "knowledge.txt").write_text("k")
    return d


def test_load_personas_sorted(tmp_path):
    _make_persona(tmp_path, "b")
    _make_persona(tmp_path, "a")
    personas = ps.load_personas([str(tmp_path)])
    assert list(personas.keys()) == ["1", "2"]
    assert personas["1"][0] == "a"
    assert personas["2"][0] == "b"


def test_load_personas_detects_new(tmp_path):
    _make_persona(tmp_path, "one")
    first = ps.load_personas([str(tmp_path)])
    _make_persona(tmp_path, "two")
    updated = ps.load_personas([str(tmp_path)])
    assert len(updated) == len(first) + 1
