#!/usr/bin/env python3
"""Persona Selector for GPT FRENZY.

This script can run interactively or via command-line options. Use ``--merge``
to combine a persona's instruction and knowledge files. Provide ``--output`` to
write the merged text to a file, otherwise it is printed to ``stdout``.
Specify ``--dir`` to add an extra search location for persona files alongside
the built-in ``personas`` folder.
"""

import argparse
import os
from pathlib import Path
from typing import Dict, List, Tuple
from fastapi import HTTPException

from gptfrenzy.core.utils import ensure_parent_dirs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Default search locations for persona files. ``main()`` resets this list
# before applying any command-line options so repeated calls behave
# consistently.
SEARCH_DIRS: List[str] = [BASE_DIR, os.path.join(BASE_DIR, "personas")]


def load_personas(dirs: List[str]) -> Dict[str, Tuple[str, str, str]]:
    """Return personas discovered under ``dirs``.

    The loader first looks for persona subdirectories containing
    ``instruction.txt`` and ``knowledge.txt`` files. If none are found, it
    falls back to pairing ``*GPT_INSTRUCTIONS.txt`` and ``*DEEP_KNOWLEDGE*.txt``
    files located directly inside the ``personas`` folder. IDs are assigned in
    alphabetical order of persona names so they remain stable across runs.
    """

    discovered: Dict[str, Tuple[str, str, str]] = {}

    for d in dirs:
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            persona_dir = os.path.join(d, name)
            if not os.path.isdir(persona_dir):
                continue
            instr = os.path.join(persona_dir, "instruction.txt")
            know = os.path.join(persona_dir, "knowledge.txt")
            if os.path.isfile(instr) and os.path.isfile(know):
                discovered[name] = (name, instr, know)

    if not discovered:
        import re

        for d in dirs:
            if not os.path.isdir(d):
                continue

            instructions: Dict[str, str] = {}
            knowledge: Dict[str, str] = {}

            for fname in os.listdir(d):
                if fname.endswith("GPT_INSTRUCTIONS.txt"):
                    # Some files use heavy prefixes like
                    # ``!!!ATTENTION_READ_ALL!!!_MIMI_GPT_INSTRUCTIONS.txt``.
                    # Extract the persona name after the *last* underscore
                    # before ``_GPT_INSTRUCTIONS`` so arbitrary prefixes work.
                    base = fname.rsplit("_GPT_INSTRUCTIONS", 1)[0]
                    if "_" in base:
                        name = base.rsplit("_", 1)[-1]
                    else:
                        name = base
                    if name:
                        instructions[name] = os.path.join(d, fname)

                if "DEEP_KNOWLEDGE" in fname and fname.endswith(".txt"):
                    m = re.search(r"_DEEP_KNOWLEDGE_([^.]*)\.txt$", fname)
                    if m:
                        knowledge[m.group(1)] = os.path.join(d, fname)

            for name in set(instructions) & set(knowledge):
                discovered[name] = (
                    name,
                    instructions[name],
                    knowledge[name],
                )

    sorted_names = sorted(discovered)
    return {str(i + 1): discovered[n] for i, n in enumerate(sorted_names)}


def build_menu(personas: Dict[str, Tuple[str, str, str]]) -> str:
    return "\n".join(f"{pid}. {info[0]}" for pid, info in personas.items())


def find_file(filename: str) -> str | None:
    """Return the first path that exists for ``filename``.

    The function checks both the script directory and a ``personas``
    subdirectory so the script works whether the persona files are in
    the repository folder structure or placed alongside the script in a
    custom GPT environment.
    """
    for d in SEARCH_DIRS:
        candidate = os.path.join(d, filename)
        if os.path.isfile(candidate):
            return candidate
    return None


PERSONAS = load_personas([os.path.join(BASE_DIR, "personas")])
MENU = build_menu(PERSONAS)


def _resolve(path: str) -> str | None:
    if os.path.isabs(path):
        return path if os.path.isfile(path) else None
    return find_file(path)


def merge_files(persona_id: str, output: str | None) -> None:
    """Merge instruction and knowledge files for ``persona_id``.

    If ``output`` is provided, write the merged content to that file,
    otherwise print it to ``stdout``.
    """
    persona = PERSONAS.get(persona_id)
    if not persona:
        print("Invalid persona ID.")
        return

    _, instr, knowledge = persona
    instr_path = _resolve(instr)
    knowledge_path = _resolve(knowledge)
    if not (instr_path and knowledge_path):
        print("Instruction or knowledge file not found.")
        return

    try:
        with open(instr_path, "r", encoding="utf-8") as f:
            merged = f.read().rstrip() + "\n\n"
        with open(knowledge_path, "r", encoding="utf-8") as f:
            merged += f.read().lstrip()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="persona not found") from exc

    if output:
        try:
            ensure_parent_dirs(Path(output))
            with open(output, "w", encoding="utf-8") as f:
                f.write(merged)
        except OSError as e:
            print(f"Failed to write to {output}: {e}")
            raise
        print(f"Merged text written to {output}")
    else:
        print(merged)


def interactive_mode() -> None:
    """Run the original interactive persona selector."""
    print("Persona Selector\n")
    print(MENU)
    choice = input("Choose a persona number: ").strip()
    persona = PERSONAS.get(choice)
    if not persona:
        print("Invalid choice.")
        return
    name, instr, knowledge = persona
    instr_path = _resolve(instr)
    knowledge_path = _resolve(knowledge)
    if not (instr_path and knowledge_path):
        print("Instruction or knowledge file not found.")
        return
    print(f"\nTo activate the {name} persona:")
    print(f"1. Open {instr_path}")
    print(f"2. Append the contents of {knowledge_path}")
    print("3. Upload the combined text to ChatGPT Codex and start your conversation.")
    print("\nNote: Only one persona can be active at a time.")


def main() -> None:
    parser = argparse.ArgumentParser(description="GPT FRENZY persona selector")
    parser.add_argument(
        "--merge",
        metavar="ID",
        help="merge instruction and knowledge for persona ID",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="write merged text to FILE (used with --merge)",
    )
    parser.add_argument(
        "--dir",
        metavar="PATH",
        help="additional directory to search for persona files",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="list available personas and exit",
    )

    args = parser.parse_args()

    global PERSONAS, MENU, SEARCH_DIRS
    # Reset search directories to their defaults before applying command-line
    # arguments so repeated ``main()`` calls behave consistently.
    SEARCH_DIRS = [BASE_DIR, os.path.join(BASE_DIR, "personas")]
    if args.dir:
        extra = os.path.abspath(args.dir)
        SEARCH_DIRS.insert(0, extra)
        PERSONAS = load_personas(
            [
                extra,
                os.path.join(BASE_DIR, "personas"),
            ]
        )
    else:
        PERSONAS = load_personas([os.path.join(BASE_DIR, "personas")])
    MENU = build_menu(PERSONAS)

    if args.list:
        print(MENU)
        return

    if args.merge:
        merge_files(args.merge, args.output)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
