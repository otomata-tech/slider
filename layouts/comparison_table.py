"""Masque : tableau comparatif (kit PCDI slide 12).

En-tête mint, lignes alternées, et indicateurs circulaires plutôt que des notes.
Chaque cellule de valeur est soit un texte (« 0 % », « 0,3 € »), soit une note
0–4 rendue en pastilles circulaires (4 = couvert, 0 = absent).
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, add_rect, add_oval, add_text, para, run,
)
from layouts._header import draw as draw_header, title_block, MARGIN_CM

RATING_MAX = 4


def _cell_text(slide, ca, x, y, w, h, text, *, bold=False, color=None, align="center"):
    _, tf = add_text(slide, x, y, w, h, anchor="m", margins=(0.1, 0, 0.1, 0))
    p = para(tf, first=True, align=align, space_after=0)
    run(p, text, size=10.5, bold=bold,
        color=color or ca.color("text"), font=ca.font_primary)


def _cell_rating(slide, ca, x, y, w, h, level):
    """Row of RATING_MAX discs, `level` filled (primary) rest hollow (rule)."""
    d = 0.32
    gap = 0.18
    total = RATING_MAX * d + (RATING_MAX - 1) * gap
    cx = x + (w - total) / 2
    cy = y + (h - d) / 2
    for i in range(RATING_MAX):
        if i < level:
            add_oval(slide, cx + i * (d + gap), cy, d, fill=ca.color("primary"))
        else:
            add_oval(slide, cx + i * (d + gap), cy, d, line=ca.color("rule"))


def render(slide, ca, *,
           title: str,
           columns: list[str],
           rows: list[dict],
           page_num: int,
           eyebrow: str | None = None,
           subtitle: str | None = None,
           section_tag: str | None = None,
           date_text: str | None = None):
    """`rows` : list of {"label": str, "values": [...]}, où value = str (texte)
    ou {"rating": int 0–4}. `columns` = libellés d'options (colonnes)."""
    add_rect(slide, 0, 0, SLIDE_W_CM, 19.05, fill=ca.color("bg"))
    draw_header(slide, ca, page_num=page_num, date_text=date_text,
                logo_path=ca.default("header_logo"))
    title_block(slide, ca, title=title, eyebrow=eyebrow, subtitle=subtitle)

    x0 = MARGIN_CM
    table_w = SLIDE_W_CM - 2 * MARGIN_CM
    label_w = 8.5
    ncol = len(columns)
    col_w = (table_w - label_w) / ncol
    y = 4.9
    row_h = 1.25

    # header row (mint band)
    add_rect(slide, x0, y, table_w, row_h, fill=ca.color("panel-mint"))
    for j, c in enumerate(columns):
        _cell_text(slide, ca, x0 + label_w + j * col_w, y, col_w, row_h,
                   c.upper(), bold=True, color=ca.color("primary"))
    y += row_h

    # body rows (alternating)
    for i, rrow in enumerate(rows):
        if i % 2 == 1:
            add_rect(slide, x0, y, table_w, row_h, fill=ca.color("bg-soft"))
        _cell_text(slide, ca, x0 + 0.2, y, label_w - 0.2, row_h,
                   rrow["label"].upper(), bold=True, align="left",
                   color=ca.color("text"))
        for j, val in enumerate(rrow["values"]):
            cx = x0 + label_w + j * col_w
            if isinstance(val, dict) and "rating" in val:
                _cell_rating(slide, ca, cx, y, col_w, row_h, int(val["rating"]))
            else:
                _cell_text(slide, ca, cx, y, col_w, row_h, str(val))
        y += row_h

    # bottom hairline
    add_rect(slide, x0, y, table_w, 0.03, fill=ca.color("rule"))
