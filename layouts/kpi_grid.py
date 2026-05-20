"""kpi_grid — grille de N KPI (chiffres-clés) avec label court.

Visuel :
    ┌────────────────────────────────────────────────────┐
    │ ▌ header  brand · TAG · NN                          │
    │                                                     │
    │  TITRE                                              │
    │  ──                                                 │
    │  Accroche / contexte court (optionnel)              │
    │                                                     │
    │   45%       700+      €1.4B     5M+      60+        │
    │   ──        ──        ──        ──       ──         │
    │   with a    Employees Valuation Cards    Nation-    │
    │   tech                          issued   alities    │
    │   background                                        │
    │                                                     │
    │  ──────────────────────────────── footnote / src NN │
    └────────────────────────────────────────────────────┘
    Fond `bg`. Valeurs en `primary-deep` géant, labels en `muted`.
    N items, alignés en une rangée ou deux selon le nombre.

Usage :
    kpi_grid.render(slide, charte,
        title="Tech company with a banking license",
        items=[
            {"value": "45%",   "label": "with a tech\nbackground"},
            {"value": "700+",  "label": "Employees"},
            {"value": "€1.4B", "label": "Valuation"},
            {"value": "5M+",   "label": "Cards issued"},
            {"value": "60+",   "label": "Nationalities"},
        ],
        page_num=2,
        subtitle="Established and Robust BaaS & PaaS provider",
        footnote="Source : annual report, 2024",
        section_tag="OVERVIEW")
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, para, run,
)
from layouts._header import draw as draw_header


def render(slide, ca, *,
           title: str,
           items: list[dict],
           page_num: int,
           subtitle: str | None = None,
           footnote: str | None = None,
           section_tag: str | None = None,
           brand_logo_path: str | None = None):
    """N items → grille auto. 1-5 items = une rangée, 6-10 = deux rangées."""
    if brand_logo_path is None:
        brand_logo_path = ca.default("header_logo")

    add_rect(slide, 0, 0, SLIDE_W_CM, SLIDE_H_CM, fill=ca.color("bg"))
    draw_header(slide, ca, page_num=page_num, section_tag=section_tag,
                logo_path=brand_logo_path)

    # --- title block
    _, tf = add_text(slide, 0.9, 1.7, SLIDE_W_CM - 1.8, 1.6)
    p = para(tf, first=True)
    run(p, title, size=int(ca.token_size("h2")), bold=True,
        color=ca.color("text-strong"), font=ca.font_primary)

    add_rect(slide, 0.9, 3.4, 2.8, 0.08, fill=ca.color("signature"))

    if subtitle:
        _, tf = add_text(slide, 0.9, 3.7, SLIDE_W_CM - 1.8, 0.9)
        p = para(tf, first=True)
        run(p, subtitle, size=12,
            color=ca.color("muted"), font=ca.font_primary)
        grid_top = 5.2
    else:
        grid_top = 4.5

    # --- grid layout
    n = len(items)
    if n == 0:
        return
    rows = 2 if n > 5 else 1
    per_row = (n + 1) // 2 if rows == 2 else n

    margin_x = 0.9
    avail_w  = SLIDE_W_CM - 2 * margin_x
    col_w    = avail_w / per_row
    row_h    = 5.5 if rows == 1 else 4.5

    for idx, item in enumerate(items):
        row = idx // per_row
        col = idx % per_row
        x = margin_x + col * col_w
        y = grid_top + row * (row_h + 0.6)

        # value (giant)
        _, tf = add_text(slide, x, y, col_w, 2.4, anchor="b",
                         margins=(0.05, 0, 0.05, 0))
        p = para(tf, first=True, align="left")
        run(p, item["value"], size=44, bold=True,
            color=ca.color("primary-deep"), font=ca.font_primary)

        # signature underline
        add_rect(slide, x + 0.05, y + 2.5, 1.2, 0.06,
                 fill=ca.color("signature"))

        # label
        _, tf = add_text(slide, x, y + 2.7, col_w - 0.3, row_h - 2.7,
                         margins=(0.05, 0, 0.1, 0))
        p = para(tf, first=True)
        run(p, item["label"], size=10,
            color=ca.color("muted"), font=ca.font_primary)

    # --- footnote
    if footnote:
        _, tf = add_text(slide, 0.9, SLIDE_H_CM - 1.5, SLIDE_W_CM - 4.0, 0.7)
        p = para(tf, first=True)
        run(p, footnote, size=9, italic=True,
            color=ca.color("muted-soft"), font=ca.font_primary)
