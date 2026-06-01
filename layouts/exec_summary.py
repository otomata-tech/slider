"""Gabarit : Executive summary (kit PCDI slide 16).

Thèse centrale en titre, paragraphe d'amorce, puis deux axes de synthèse en
listes « + ».
"""
from __future__ import annotations

from lib.pptx_helpers import SLIDE_W_CM, add_rect, add_text, para, run
from layouts._header import draw as draw_header, title_block, MARGIN_CM
from layouts import _components as C


def render(slide, ca, *,
           title: str,
           intro: str,
           axes: list[dict],
           page_num: int,
           eyebrow: str | None = None,
           section_tag: str | None = None,
           date_text: str | None = None):
    """`axes` : list de {"heading": str, "items": [str | (lead, rest)]}."""
    add_rect(slide, 0, 0, SLIDE_W_CM, 19.05, fill=ca.color("bg"))
    draw_header(slide, ca, page_num=page_num, date_text=date_text,
                logo_path=ca.default("header_logo"))
    title_block(slide, ca, title=title, eyebrow=eyebrow or "Executive summary")

    # paragraphe d'amorce
    _, tf = add_text(slide, MARGIN_CM, 4.6, SLIDE_W_CM - 2 * MARGIN_CM, 2.0,
                     margins=(0, 0, 0, 0))
    p = para(tf, first=True, line_spacing=1.5)
    run(p, intro, size=11, color=ca.color("text-soft"), font=ca.font_primary)

    # deux axes en colonnes
    col_w = (SLIDE_W_CM - 2 * MARGIN_CM - 1.2) / 2
    y = 7.2
    for k, axis in enumerate(axes[:2]):
        x = MARGIN_CM + k * (col_w + 1.2)
        _, tf = add_text(slide, x, y, col_w, 0.8, margins=(0, 0, 0, 0))
        p = para(tf, first=True)
        run(p, axis["heading"].upper(), size=11, bold=True,
            color=ca.color("primary"), font=ca.font_primary)
        C.marker_list(slide, ca, x, y + 0.9, col_w, axis["items"], size=11)
