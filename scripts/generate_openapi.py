import json
from pathlib import Path
import sys
import types

# Make repo root importable when executed from the scripts directory
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Stub optional dependencies that are unnecessary for spec generation
sys.modules.setdefault(
    "redis",
    types.SimpleNamespace(
        Redis=lambda *a, **kw: types.SimpleNamespace(ping=lambda: None),
        from_url=lambda *a, **kw: types.SimpleNamespace(ping=lambda: None),
        RedisError=Exception,
        exceptions=types.SimpleNamespace(
            ConnectionError=Exception, RedisError=Exception
        ),
    ),
)
sys.modules.setdefault("openai", types.SimpleNamespace(OpenAI=lambda *a, **kw: object()))
sys.modules.setdefault("yaml", types.SimpleNamespace(safe_load=lambda *_: []))

from gptfrenzy.core.utils import ensure_parent_dirs
from app import app

path = Path("openapi.json")
ensure_parent_dirs(path)
with path.open("w", encoding="utf-8") as f:
    json.dump(app.openapi(), f, indent=2)
