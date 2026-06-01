"""Deck — composes layouts + a charte into a PPTX, with optional PDF/viewer export."""
from __future__ import annotations

import inspect
import os
from dataclasses import dataclass, field
from pathlib import Path

from pptx import Presentation
from pptx.util import Cm

from lib.charte import Charte
from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_blank_slide,
)

# Lint mode : `slide-craft lint` sets SLIDE_CRAFT_LINT=1, runs build.py, and
# Deck.add validates each call instead of rendering. Issues land here.
_LINT_ISSUES: list[dict] = []
_IMAGE_HINTS = ("_path", "_photo", "photo_", "_logo", "logo_")


def _lint_mode() -> bool:
    return os.environ.get("SLIDE_CRAFT_LINT") == "1"


def _validate_add(render_fn, kwargs: dict, page: int):
    """Collect contract violations for one deck.add() call (no rendering)."""
    params = inspect.signature(render_fn).parameters
    has_var_kw = any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values())
    names = {n for n in params if n not in ("slide", "ca")}
    layout = render_fn.__module__.split(".")[-1]

    # kwargs inconnus (sauf si le layout a **kwargs)
    if not has_var_kw:
        for k in kwargs:
            if k not in names:
                _LINT_ISSUES.append({"page": page, "layout": layout, "level": "error",
                                     "msg": f"kwarg inconnu '{k}'"})
    # requis manquants (page_num est auto-injecté → exclu)
    for n, p in params.items():
        if n in ("slide", "ca", "page_num"):
            continue
        if p.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        if p.default is inspect.Parameter.empty and n not in kwargs:
            _LINT_ISSUES.append({"page": page, "layout": layout, "level": "error",
                                 "msg": f"kwarg requis manquant '{n}'"})
    # chemins image inexistants (récursif : couvre logos=[{logo_path:…}], people=[…])
    def _walk(key, val):
        if isinstance(val, str):
            if val and any(h in key for h in _IMAGE_HINTS) and not os.path.exists(val):
                _LINT_ISSUES.append({"page": page, "layout": layout, "level": "warn",
                                     "msg": f"image introuvable ({key}=) : {val}"})
        elif isinstance(val, dict):
            for k2, v2 in val.items():
                _walk(k2, v2)
        elif isinstance(val, (list, tuple)):
            for item in val:
                _walk(key, item)

    for k, v in kwargs.items():
        _walk(k, v)


@dataclass
class Deck:
    """A 16:9 widescreen deck under a single charte.

    Usage:
        deck = Deck(Charte.load("blank"))
        deck.add(cover_split.render, brand_label=..., title_lines=..., ...)
        deck.add(event_fiche.render, name="<event>", title="...", ...)
        deck.save_pptx("out/deck.pptx")
        deck.export_pdf("out/deck.pdf")
    """

    charte: Charte
    prs: Presentation = field(default_factory=Presentation)
    pages: int = 0
    _slide_metas: list[dict] = field(default_factory=list)

    def __post_init__(self):
        self.prs.slide_width  = Cm(SLIDE_W_CM)
        self.prs.slide_height = Cm(SLIDE_H_CM)

    # ---------------------------------------------------------------- add

    def add(self, render_fn, *, meta: dict | None = None, **kwargs):
        """Add a slide by calling `render_fn(slide, charte, **kwargs)`.

        If `render_fn` declares a `page_num` parameter, the deck injects the
        auto-incremented page number. Same for `charte`.

        `meta` is stored on the slide for downstream uses (viewer index,
        section navigation, etc.).
        """
        self.pages += 1
        # Lint mode : valider le contrat de l'appel, sans rien rendre.
        if _lint_mode():
            _validate_add(render_fn, kwargs, self.pages)
            return None

        slide = add_blank_slide(self.prs)
        # auto-inject page_num if the render fn wants it
        sig = inspect.signature(render_fn)
        params = sig.parameters
        if "page_num" in params and "page_num" not in kwargs:
            kwargs["page_num"] = self.pages

        render_fn(slide, self.charte, **kwargs)
        self._slide_metas.append({
            "page": self.pages,
            "layout": render_fn.__module__,
            "meta": meta or {},
        })
        return slide

    # ---------------------------------------------------------------- save

    def save_pptx(self, path: str | os.PathLike) -> str:
        if _lint_mode():
            return str(path)  # no-op : on ne builde pas en mode lint
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.prs.save(str(path))
        return str(path)

    def export_pdf(self, pptx_path: str | os.PathLike,
                   pdf_path: str | os.PathLike | None = None) -> str | None:
        """Convert pptx → pdf via LibreOffice.

        Returns the PDF path, or None if PDF export is unavailable/disabled:
          - SLIDER_NO_PDF=1 in env (e.g. `slide-craft build --no-pdf` sets it)
          - LibreOffice not installed (graceful skip with a one-line notice)
        """
        from lib.pdf_export import pptx_to_pdf, soffice_path

        if _lint_mode():
            return None  # no-op : pas de build en mode lint
        if os.environ.get("SLIDER_NO_PDF") == "1":
            print("PDF skipped (SLIDER_NO_PDF=1)")
            return None
        if soffice_path() is None:
            print("PDF skipped (LibreOffice not found — install it for PDF export, "
                  "or pass --no-pdf to silence this).")
            return None
        return pptx_to_pdf(pptx_path, pdf_path)

    @property
    def slide_metas(self) -> list[dict]:
        return list(self._slide_metas)
