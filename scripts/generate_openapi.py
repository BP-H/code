import json
from pathlib import Path
import sys
import types

try:
    import yaml  # Ensure pyyaml is installed
except Exception:
    yaml = types.SimpleNamespace(safe_load=lambda *_args, **_kw: [])
    sys.modules.setdefault("yaml", yaml)

# Stub optional dependencies that are unnecessary for spec generation
sys.modules.setdefault(
    "redis",
    types.SimpleNamespace(
        from_url=lambda *a, **kw: types.SimpleNamespace(),
        exceptions=types.SimpleNamespace(ConnectionError=Exception),
    ),
)
sys.modules.setdefault("openai", types.SimpleNamespace(OpenAI=lambda *a, **kw: object()))

from gptfrenzy.utils import ensure_parent_dirs
from api.character_router import app as character_app
from app import app


# Mount the character API so the spec includes those routes
app.include_router(character_app.router)


def generate(path: Path) -> None:
    """Write the OpenAPI spec to *path*."""
    ensure_parent_dirs(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(app.openapi(), f, indent=2)


def main(argv: list[str] | None = None) -> None:
    """Entry point for CLI usage."""
    argv = argv or sys.argv[1:]
    if argv:
        path = Path(argv[0])
    else:
        path = Path("openapi.json")
    generate(path)


if __name__ == "__main__":
    main()
