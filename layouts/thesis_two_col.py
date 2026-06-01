"""Gabarit : thèse en deux colonnes + bandeau de chiffres-clés (kit PCDI slide 17).

Titre-thèse en capitales, sous-titre vert, deux colonnes d'arguments en listes
« + », et une rangée optionnelle de stat-cards en bas.
"""
from __future__ import annotations

from lib.pptx_helpers import SLIDE_W_CM, add_rect, add_text, para, run
from layouts._header import draw as draw_header, title_block, MARGIN_CM
from layouts import _components as C


def render(slide, ca, *,
           title: str,
           left: dict,
           right: dict,
           page_num: int,
           subtitle: str | None = None,
           stats: list | None = None,
           eyebrow: str | None = None,
           section_tag: str | None = None,
           date_text: str | None = None):
    """`left`/`right` : {"heading": str, "items": [...]}.
    `stats` : list de (number, label), jusqu'à 3, rendue en bas."""
    add_rect(slide, 0, 0, SLIDE_W_CM, 19.05, fill=ca.color("bg"))
    draw_header(slide, ca, page_num=page_num, date_text=date_text,
                logo_path=ca.default("header_logo"))
    title_block(slide, ca, title=title, eyebrow=eyebrow, subtitle=subtitle)

    col_w = (SLIDE_W_CM - 2 * MARGIN_CM - 1.2) / 2
    y = 5.0
    for k, col in enumerate((left, right)):
        x = MARGIN_CM + k * (col_w + 1.2)
        _, tf = add_text(slide, x, y, col_w, 0.8, margins=(0, 0, 0, 0))
        p = para(tf, first=True)
        run(p, col["heading"].upper(), size=11, bold=True,
            color=ca.color("primary"), font=ca.font_primary)
        C.marker_list(slide, ca, x, y + 0.9, col_w, col["items"], size=11)

    if stats:
        n = min(3, len(stats))
        gap = 0.8
        cw = (SLIDE_W_CM - 2 * MARGIN_CM - (n - 1) * gap) / n
        cy = 13.2
        for i, (num, lab) in enumerate(stats[:n]):
            C.stat_card(slide, ca, MARGIN_CM + i * (cw + gap), cy, cw, 3.4,
                        number=num, label=lab, number_pt=28)
