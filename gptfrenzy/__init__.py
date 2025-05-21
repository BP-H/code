"""GPT Frenzy package.

Raises a clear error when imported on unsupported Python versions.
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 10):
    raise RuntimeError("GPT Frenzy requires Python 3.10 or later")

from .spawn import launch, make_manifest
