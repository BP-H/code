"""Spawn a persona process via the SAP controller.

Run as a module using::

    python -m scripts.frenzy_spawn <persona_dir> [--host HOST]

The command is also installed as ``frenzy-spawn`` via the package entry point.
"""

import argparse
from pathlib import Path

from gptfrenzy.core.spawn import launch


def main() -> None:
    parser = argparse.ArgumentParser(description="Spawn persona via SAP")
    parser.add_argument("persona", help="path to persona directory")
    parser.add_argument("--host", default="local", help="target host name")
    args = parser.parse_args()

    instance = launch(args.host, args.persona)
    caps = ", ".join(sorted(instance.capabilities))
    name = Path(args.persona).name
    print(f"\u2713 Spawned {name} in {args.host} ({caps} enabled)")


if __name__ == "__main__":
    main()
