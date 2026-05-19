"""Charte loader — exposes colors / fonts / sizes / asset paths from
chartes/<name>/.

A charte is a directory with:
    tokens.json   # source of truth (colors, fonts, scale)
    tokens.py     # python-pptx RGBColor constants
    tokens.css    # CSS variables (for any HTML rendering)
    assets/       # logos, fonts, photos

Usage:
    from lib.charte import Charte
    ca = Charte.load("credit-agricole")
    ca.color("primary")            # RGBColor — sarcelle CA
    ca.font_primary                 # "Raleway"
    ca.asset("logo/ca-logo.jpg")    # absolute path
    ca.token_size("h1")             # 46.0 (pt)
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pptx.dml.color import RGBColor


# Chartes live as subdirs of the engine's chartes/. Theme repos are cloned
# directly into this dir (e.g. `git clone <theme> chartes/<client>`), making
# slider self-contained as a working directory.
ENGINE_CHARTES = Path(__file__).resolve().parent.parent / "chartes"


def _theme_search_paths() -> list[Path]:
    """Resolve directories to search for chartes, in priority order.

    1. ``$PWD/chartes`` — local overrides when slide-craft is run from a
       directory that has its own chartes/ (rare).
    2. Engine's ``chartes/`` — where theme repos are cloned into.
    """
    paths = [Path.cwd() / "chartes", ENGINE_CHARTES]
    # Dedup if cwd happens to be the engine itself.
    seen, out = set(), []
    for p in paths:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            out.append(p)
    return out


def _hex_to_rgb(hex_str: str) -> RGBColor:
    """#82B600 → RGBColor(0x82, 0xB6, 0x00). Also accepts no leading #."""
    h = hex_str.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"invalid hex color: {hex_str!r}")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


@dataclass
class Charte:
    """A loaded charte. Holds the raw tokens dict plus convenience accessors."""

    name: str
    root: Path
    tokens: dict[str, Any] = field(repr=False)

    # ------------------------------------------------------------------ load

    @classmethod
    def load(cls, name: str, *, root: Path | None = None) -> "Charte":
        """Load a charte by name. Searches multiple roots — see
        :func:`_theme_search_paths`. Pass ``root`` to override search.
        """
        if root is not None:
            search = [Path(root)]
        else:
            search = _theme_search_paths()

        for base_root in search:
            tokens_path = base_root / name / "tokens.json"
            if tokens_path.exists():
                tokens = json.loads(tokens_path.read_text(encoding="utf-8"))
                return cls(name=name, root=base_root / name, tokens=tokens)

        roots_listed = "\n  - ".join(str(p) for p in search)
        raise FileNotFoundError(
            f"Charte '{name}' not found. Searched:\n  - {roots_listed}\n"
            f"Tip: clone the theme repo into chartes/{name}/ "
            f"(e.g. `git clone <theme-repo> chartes/{name}`)."
        )

    @classmethod
    def discover(cls) -> list[tuple[str, Path]]:
        """Return [(name, root)] of all chartes findable across search paths.
        Used by `slide-craft list-chartes`. Stable order, deduped by name
        (first-seen wins, matching `load()` priority).
        """
        seen: dict[str, Path] = {}
        for base in _theme_search_paths():
            if not base.exists():
                continue
            for d in sorted(base.iterdir()):
                if d.is_dir() and (d / "tokens.json").exists():
                    if d.name not in seen:
                        seen[d.name] = d
        return list(seen.items())

    # ------------------------------------------------------------------ colors

    def color(self, key: str) -> RGBColor:
        """Return the color for `key` (e.g. "primary", "signature").
        Raises KeyError if missing."""
        entry = self.tokens["colors"].get(key)
        if entry is None:
            raise KeyError(f"color '{key}' not in charte '{self.name}'")
        return _hex_to_rgb(entry["value"])

    def color_hex(self, key: str) -> str:
        return self.tokens["colors"][key]["value"]

    # ------------------------------------------------------------------ fonts

    @property
    def font_primary(self) -> str:
        return self.tokens["fonts"]["primary"]["family"]

    @property
    def font_condensed(self) -> str:
        fonts = self.tokens["fonts"]
        return fonts.get("condensed", fonts["primary"])["family"]

    # ------------------------------------------------------------------ scale

    def token_size(self, key: str) -> float:
        """Return the pt size for a named scale entry (h1, h2, body, …)."""
        return float(self.tokens["type-scale"][key]["size_pt"])

    # ------------------------------------------------------------------ assets

    def asset(self, rel_path: str) -> str:
        """Return absolute path to an asset under assets/. Raises if missing."""
        p = self.root / "assets" / rel_path
        if not p.exists():
            raise FileNotFoundError(f"asset '{rel_path}' missing in charte '{self.name}' ({p})")
        return str(p)

    def has_asset(self, rel_path: str) -> bool:
        return (self.root / "assets" / rel_path).exists()

    # ------------------------------------------------------------------ defaults

    def default(self, key: str) -> str | None:
        """Return the absolute path to a default asset declared in tokens.json
        under `defaults.<key>`, or None if the entry is absent.

        Used by layouts to auto-inject brand assets (cover photo, header logo…)
        when the caller doesn't pass them explicitly.

        Standard keys: ``cover_photo``, ``cover_logo``, ``header_logo``.
        """
        defaults = self.tokens.get("defaults") or {}
        rel = defaults.get(key)
        if not rel:
            return None
        p = self.root / "assets" / rel
        return str(p) if p.exists() else None
