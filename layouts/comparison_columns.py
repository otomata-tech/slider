"""comparison_columns — 2 ou 3 colonnes comparatives (avant/après, A/B/C).

Visuel :
    ┌────────────────────────────────────────────────────┐
    │ ▌ header                                             │
    │                                                     │
    │  TITRE                                              │
    │  ──                                                 │
    │  Accroche                                           │
    │                                                     │
    │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
    │  │  HEADER     │ │  HEADER     │ │  HEADER     │   │
    │  │  era / mode │ │  era / mode │ │  era / mode │   │
    │  │  ──         │ │  ──         │ │  ──         │   │
    │  │  Sub-title  │ │  Sub-title  │ │  Sub-title  │   │
    │  │             │ │             │ │             │   │
    │  │  • item     │ │  • item     │ │  • item     │   │
    │  │  • item     │ │  • item     │ │  • item     │   │
    │  │  • item     │ │  • item     │ │  • item     │   │
    │  └─────────────┘ └─────────────┘ └─────────────┘   │
    │                                                     │
    └────────────────────────────────────────────────────┘
    Colonne centrale (si 3) en `panel-cream` pour souligner le pivot.
    Headers en `primary-deep`, bullets bullets en `signature`.

Usage :
    comparison_columns.render(slide, charte,
        title="Embedded Finance is the next stage in the fintech evolution",
        columns=[
            {"header": "Traditional FS Models",
             "era":    "<2010",
             "items":  ["Brick & mortar", "Branch network", "Product-led"]},
            {"header": "Fintechs, Challengers",
             "era":    "2020",
             "items":  ["Digital-native", "App-first", "Bundled features"]},
            {"header": "Embedded Finance",
             "era":    "Future",
             "items":  ["At point of need", "Non-FS firms offer", "Context-aware"],
             "highlight": True},                           # → fond panel-cream
        ],
        page_num=5,
        subtitle="From traditional banking to ubiquitous finance",
        section_tag="EVOLUTION")
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, para, run,
)
from layouts._header import draw as draw_header


def render(slide, ca, *,
           title: str,
           columns: list[dict],
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

    # --- columns (2 or 3)
    n = max(2, min(len(columns), 3))
    margin_x = 0.9
    gutter   = 0.5
    avail_w  = SLIDE_W_CM - 2 * margin_x - gutter * (n - 1)
    col_w    = avail_w / n
    col_h    = SLIDE_H_CM - grid_top - 1.2

    for idx, col_data in enumerate(columns[:n]):
        x = margin_x + idx * (col_w + gutter)
        y = grid_top

        # background panel — highlighted column uses panel-cream
        bg_token = "panel-cream" if col_data.get("highlight") else "panel-mint"
        add_rect(slide, x, y, col_w, col_h, fill=ca.color(bg_token))

        # accent rule top
        accent_token = "signature" if col_data.get("highlight") else "primary"
        add_rect(slide, x, y, col_w, 0.12, fill=ca.color(accent_token))

        inner_x = x + 0.4
        inner_w = col_w - 0.8
        cursor_y = y + 0.5

        # era (eyebrow)
        if col_data.get("era"):
            _, tf = add_text(slide, inner_x, cursor_y, inner_w, 0.7)
            p = para(tf, first=True)
            run(p, col_data["era"].upper(), size=9, bold=True,
                color=ca.color(accent_token), font=ca.font_primary)
            cursor_y += 0.7

        # header
        _, tf = add_text(slide, inner_x, cursor_y, inner_w, 1.4)
        p = para(tf, first=True)
        run(p, col_data["header"], size=14, bold=True,
            color=ca.color("primary-deep"), font=ca.font_primary)
        cursor_y += 1.5

        # underline
        add_rect(slide, inner_x, cursor_y, 1.6, 0.06,
                 fill=ca.color(accent_token))
        cursor_y += 0.4

        # items (bullets)
        for item in col_data.get("items", []):
            _, tf = add_text(slide, inner_x, cursor_y, inner_w, 0.8,
                             margins=(0, 0, 0, 0))
            p = para(tf, first=True)
            run(p, "• ", size=11, bold=True,
                color=ca.color(accent_token), font=ca.font_primary)
            run(p, item, size=10,
                color=ca.color("text"), font=ca.font_primary)
            cursor_y += 0.85
