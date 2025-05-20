import json
from pathlib import Path
import sys
import types

import yaml  # Ensure pyyaml is installed

from gptfrenzy.utils import ensure_parent_dirs
from api.character_router import app as character_app
from app import app

# Stub optional dependencies that are unnecessary for spec generation
sys.modules.setdefault(
    "redis",
    types.SimpleNamespace(
        from_url=lambda *a, **kw: types.SimpleNamespace(),
        exceptions=types.SimpleNamespace(ConnectionError=Exception),
    ),
)
sys.modules.setdefault("openai", types.SimpleNamespace(OpenAI=lambda *a, **kw: object()))

# Mount the character API so the spec includes those routes
app.include_router(character_app.router)

path = Path("openapi.json")
ensure_parent_dirs(path)
with path.open("w", encoding="utf-8") as f:
    json.dump(app.openapi(), f, indent=2)
