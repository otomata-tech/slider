"""services_grid — grille de N cards (offre / service / capability).

Visuel :
    ┌────────────────────────────────────────────────────┐
    │ ▌ header  brand · TAG · NN                          │
    │                                                     │
    │  TITRE                                              │
    │  ──                                                 │
    │  Accroche                                           │
    │                                                     │
    │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐      │
    │  │ icon │ │ icon │ │ icon │ │ icon │ │ icon │      │
    │  │      │ │      │ │      │ │      │ │      │      │
    │  │ Title│ │ Title│ │ Title│ │ Title│ │ Title│      │
    │  │ desc │ │ desc │ │ desc │ │ desc │ │ desc │      │
    │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘      │
    │                                                     │
    └────────────────────────────────────────────────────┘
    Cards `panel-mint`. Icône facultative (logo, picto). Title bold,
    description en muted. Auto-layout 3 à 6 colonnes selon `len(items)`.

Usage :
    services_grid.render(slide, charte,
        title="Solaris business model",
        items=[
            {"title": "Digital Banking",
             "description": "Provide bank accounts and transactions...",
             "icon_path": "media/icon-bank.png"},          # optionnel
            {"title": "Cards",          "description": "Offer VISA or Master debit cards..."},
            {"title": "Payments",       "description": "Provide compliant and digital..."},
            {"title": "Lending",        "description": "Offer instant consumer..."},
            {"title": "Digital Assets", "description": "Offer digital assets services..."},
        ],
        page_num=3,
        subtitle="Services overview",
        section_tag="MODEL")
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, add_image, fit_image, para, run,
)
from layouts._header import draw as draw_header


def render(slide, ca, *,
           title: str,
           items: list[dict],
           page_num: int,
           subtitle: str | None = None,
           section_tag: str | None = None,
           brand_logo_path: str | None = None):
    if brand_logo_path is None:
        brand_logo_path = ca.default("header_logo")

    add_rect(slide, 0, 0, SLIDE_W_CM, SLIDE_H_CM, fill=ca.color("bg"))
    draw_header(slide, ca, page_num=page_num, section_tag=section_tag,
                logo_path=brand_logo_path)

    # --- title
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

    # --- grid : 3-6 cols on a single row by default
    n = len(items)
    if n == 0:
        return
    cols = min(n, 6)
    rows = (n + cols - 1) // cols

    margin_x = 0.9
    gutter   = 0.4
    avail_w  = SLIDE_W_CM - 2 * margin_x - gutter * (cols - 1)
    col_w    = avail_w / cols
    card_h   = (SLIDE_H_CM - grid_top - 1.5 - gutter * (rows - 1)) / rows

    for idx, item in enumerate(items):
        row = idx // cols
        col = idx % cols
        x = margin_x + col * (col_w + gutter)
        y = grid_top + row * (card_h + gutter)

        # card background
        add_rect(slide, x, y, col_w, card_h, fill=ca.color("panel-mint"))

        # accent rule top
        add_rect(slide, x, y, col_w, 0.1, fill=ca.color("signature"))

        inner_x = x + 0.3
        inner_w = col_w - 0.6
        cursor_y = y + 0.4

        # icon (optional)
        if item.get("icon_path"):
            pic = add_image(slide, item["icon_path"], inner_x, cursor_y,
                            h_cm=1.3)
            if pic is not None:
                fit_image(pic, max_w_cm=1.5, max_h_cm=1.3)
                cursor_y += 1.7

        # title
        _, tf = add_text(slide, inner_x, cursor_y, inner_w, 1.2)
        p = para(tf, first=True)
        run(p, item["title"], size=12, bold=True,
            color=ca.color("primary-deep"), font=ca.font_primary)

        # description
        _, tf = add_text(slide, inner_x, cursor_y + 1.1,
                         inner_w, card_h - (cursor_y + 1.1 - y) - 0.3)
        p = para(tf, first=True)
        run(p, item.get("description", ""), size=9,
            color=ca.color("text"), font=ca.font_primary)
