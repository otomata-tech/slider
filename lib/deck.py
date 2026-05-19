"""Deck — composes layouts + a charte into a PPTX, with optional PDF/viewer export."""
from __future__ import annotations

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


@dataclass
class Deck:
    """A 16:9 widescreen deck under a single charte.

    Usage:
        deck = Deck(Charte.load("credit-agricole"))
        deck.add(cover_split.render, brand_label=..., title_lines=..., ...)
        deck.add(event_fiche.render, name="CHANGENOW", title="...", ...)
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
        slide = add_blank_slide(self.prs)
        self.pages += 1
        # auto-inject page_num if the render fn wants it
        import inspect
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
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.prs.save(str(path))
        return str(path)

    def export_pdf(self, pptx_path: str | os.PathLike,
                   pdf_path: str | os.PathLike | None = None) -> str:
        """Convert pptx → pdf via LibreOffice. Requires libreoffice-impress."""
        from lib.pdf_export import pptx_to_pdf
        return pptx_to_pdf(pptx_path, pdf_path)

    @property
    def slide_metas(self) -> list[dict]:
        return list(self._slide_metas)
