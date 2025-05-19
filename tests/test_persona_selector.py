import os
import persona_selector as ps
import pytest


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
