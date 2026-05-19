"""Shared helpers for slide-craft CLI scripts. Sets up sys.path and project root."""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Skill is installed as a symlink. Resolve to the underlying project root
# (which contains lib/, layouts/, chartes/, decks/).
SKILL_DIR  = Path(__file__).resolve().parent.parent
PROJECT    = SKILL_DIR.parent          # /data/projects/slide-craft
LIB        = PROJECT / "lib"
LAYOUTS    = PROJECT / "layouts"
CHARTES    = PROJECT / "chartes"
DECKS      = PROJECT / "decks"

if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))


def fail(msg: str, code: int = 1) -> "NoReturn":
    print(f"slide-craft: error: {msg}", file=sys.stderr)
    sys.exit(code)


def ok(msg: str):
    print(msg)
