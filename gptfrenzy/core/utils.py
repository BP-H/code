from __future__ import annotations

from pathlib import Path


def ensure_parent_dirs(path: Path) -> None:
    """Create parent directories for ``path`` if they do not exist."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
