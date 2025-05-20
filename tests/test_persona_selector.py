import sys
import persona_selector as ps
import pytest


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


def test_find_file_searches_dirs(tmp_path, monkeypatch):
    d1 = tmp_path / "d1"
    d2 = tmp_path / "d2"
    d1.mkdir()
    d2.mkdir()
    target = d2 / "example.txt"
    target.write_text("data")

    monkeypatch.setattr(ps, "SEARCH_DIRS", [str(d1), str(d2)])

    assert ps.find_file("example.txt") == str(target)
    assert ps.find_file("missing.txt") is None


def test_merge_files_writes_merged(tmp_path, monkeypatch, capsys):
    persona_id = "X"
    instr_name = "instr.txt"
    know_name = "knowledge.txt"
    monkeypatch.setattr(ps, "PERSONAS", {persona_id: ("Test", instr_name, know_name)})
    monkeypatch.setattr(ps, "SEARCH_DIRS", [str(tmp_path)])

    instr_path = tmp_path / instr_name
    know_path = tmp_path / know_name
    instr_path.write_text("hello\n")
    know_path.write_text("\nworld")

    out_file = tmp_path / "out.txt"
    ps.merge_files(persona_id, str(out_file))
    captured = capsys.readouterr()

    assert f"Merged text written to {out_file}" in captured.out
    assert out_file.read_text() == "hello\n\nworld"


def test_merge_files_missing_file(tmp_path, monkeypatch, capsys):
    persona_id = "X"
    instr_name = "instr.txt"
    know_name = "knowledge.txt"
    monkeypatch.setattr(ps, "PERSONAS", {persona_id: ("Test", instr_name, know_name)})
    monkeypatch.setattr(ps, "SEARCH_DIRS", [str(tmp_path)])

    instr_path = tmp_path / instr_name
    instr_path.write_text("only instructions")
    out_file = tmp_path / "out.txt"
    ps.merge_files(persona_id, str(out_file))
    captured = capsys.readouterr()

    assert "Instruction or knowledge file not found." in captured.out
    assert not out_file.exists()


def test_interactive_mode(monkeypatch, tmp_path, capsys):
    persona_id = "1"
    instr_name = "instr.txt"
    know_name = "knowledge.txt"
    monkeypatch.setattr(ps, "PERSONAS", {persona_id: ("Test", instr_name, know_name)})
    monkeypatch.setattr(ps, "MENU", "1. Test")
    monkeypatch.setattr(ps, "SEARCH_DIRS", [str(tmp_path)])

    (tmp_path / instr_name).write_text("hello")
    (tmp_path / know_name).write_text("world")

    monkeypatch.setattr("builtins.input", lambda _: persona_id)
    ps.interactive_mode()
    captured = capsys.readouterr()

    assert "Persona Selector" in captured.out
    assert "To activate the Test persona:" in captured.out


def test_merge_files_dir_not_file(tmp_path, monkeypatch, capsys):
    persona_id = "X"
    instr_name = "instr.txt"
    know_name = "knowledge.txt"
    monkeypatch.setattr(ps, "PERSONAS", {persona_id: ("Test", instr_name, know_name)})
    monkeypatch.setattr(ps, "SEARCH_DIRS", [str(tmp_path)])

    (tmp_path / instr_name).mkdir()
    (tmp_path / know_name).mkdir()

    out_file = tmp_path / "out.txt"
    ps.merge_files(persona_id, str(out_file))
    captured = capsys.readouterr()

    assert "Instruction or knowledge file not found." in captured.out
    assert not out_file.exists()


def test_merge_files_write_failure(tmp_path, monkeypatch, capsys):
    persona_id = "X"
    instr_name = "instr.txt"
    know_name = "knowledge.txt"
    monkeypatch.setattr(ps, "PERSONAS", {persona_id: ("Test", instr_name, know_name)})
    monkeypatch.setattr(ps, "SEARCH_DIRS", [str(tmp_path)])

    instr_path = tmp_path / instr_name
    know_path = tmp_path / know_name
    instr_path.write_text("hello\n")
    know_path.write_text("\nworld")

    out_file = tmp_path / "out.txt"

    import builtins

    real_open = builtins.open

    def fail_open(path, mode="r", *args, **kwargs):
        if path == str(out_file) and "w" in mode:
            raise OSError("boom")
        return real_open(path, mode, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fail_open)

    with pytest.raises(OSError):
        ps.merge_files(persona_id, str(out_file))

    captured = capsys.readouterr()
    assert "Failed to write to" in captured.out


def test_builtin_personas_available_with_dir(tmp_path, monkeypatch, capsys):
    base_root = tmp_path / "base"
    extra_root = tmp_path / "extra"
    builtins_dir = base_root / "personas"
    builtin = builtins_dir / "base"
    extra = extra_root / "custom"

    builtin.mkdir(parents=True)
    extra.mkdir(parents=True)

    (builtin / "instruction.txt").write_text("b")
    (builtin / "knowledge.txt").write_text("b")
    (extra / "instruction.txt").write_text("c")
    (extra / "knowledge.txt").write_text("c")

    monkeypatch.setattr(ps, "BASE_DIR", str(base_root))
    monkeypatch.setattr(ps, "SEARCH_DIRS", [str(base_root), str(builtins_dir)])
    monkeypatch.setattr(sys, "argv", ["prog", "--dir", str(extra_root), "--list"])

    ps.main()
    captured = capsys.readouterr()

    assert "base" in captured.out
    assert "custom" in captured.out


def test_merge_files_open_failure(tmp_path, monkeypatch):
    persona_id = "X"
    instr_name = "instr.txt"
    know_name = "knowledge.txt"
    monkeypatch.setattr(ps, "PERSONAS", {persona_id: ("Test", instr_name, know_name)})
    monkeypatch.setattr(ps, "SEARCH_DIRS", [str(tmp_path)])

    instr_path = tmp_path / instr_name
    know_path = tmp_path / know_name
    instr_path.write_text("hello")
    know_path.write_text("world")

    import builtins

    real_open = builtins.open

    def fail_open(path, *args, **kwargs):
        if path == str(instr_path):
            raise FileNotFoundError
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fail_open)

    with pytest.raises(ps.HTTPException) as exc:
        ps.merge_files(persona_id, None)

    assert exc.value.status_code == 404
