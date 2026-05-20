"""logo_wall — mur de logos partenaires / clients / sponsors.

Visuel :
    ┌────────────────────────────────────────────────────┐
    │ ▌ header                                             │
    │                                                     │
    │  TITRE                                              │
    │  ──                                                 │
    │  Accroche                                           │
    │                                                     │
    │  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐                 │
    │  │L1│ │L2│ │L3│ │L4│ │L5│ │L6│ │L7│                 │
    │  └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘                 │
    │                                                     │
    │  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐                 │
    │  │L8│ │..│ │..│ │..│ │..│ │..│ │..│                 │
    │  └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ └──┘                 │
    │                                                     │
    └────────────────────────────────────────────────────┘
    Logos centrés en `panel-cream` cells. Auto-layout en grille
    `cols × rows` pour caser N logos.

Usage :
    logo_wall.render(slide, charte,
        title="Backed by strong investors",
        logos=["media/logo-yc.png", "media/logo-a16z.png", ...],
        page_num=4,
        cols=7,                                            # défaut 6
        subtitle="Our existing partner base spans across Europe and UK",
        section_tag="ECOSYSTEM")
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, add_image, fit_image, para, run,
)
from layouts._header import draw as draw_header


def render(slide, ca, *,
           title: str,
           logos: list[str],
           page_num: int,
           cols: int = 6,
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

    # --- grid
    n = len(logos)
    if n == 0:
        return
    cols = max(2, min(cols, 8))
    rows = (n + cols - 1) // cols

    margin_x = 0.9
    gutter   = 0.3
    avail_w  = SLIDE_W_CM - 2 * margin_x - gutter * (cols - 1)
    cell_w   = avail_w / cols
    avail_h  = SLIDE_H_CM - grid_top - 1.0 - gutter * (rows - 1)
    cell_h   = min(avail_h / rows, 3.5)

    for idx, logo_path in enumerate(logos):
        row = idx // cols
        col = idx % cols
        x = margin_x + col * (cell_w + gutter)
        y = grid_top + row * (cell_h + gutter)

        # cell background
        add_rect(slide, x, y, cell_w, cell_h, fill=ca.color("panel-cream"))

        # logo centered, padded
        pad = 0.4
        max_w = cell_w - 2 * pad
        max_h = cell_h - 2 * pad
        pic = add_image(slide, logo_path, x + pad, y + pad,
                        h_cm=max_h)
        if pic is not None:
            fit_image(pic, max_w_cm=max_w, max_h_cm=max_h)
            # re-center horizontally after fit
            pic_w_cm = pic.width / 360000
            pic.left = int((x + (cell_w - pic_w_cm) / 2) * 360000)
            # re-center vertically
            pic_h_cm = pic.height / 360000
            pic.top  = int((y + (cell_h - pic_h_cm) / 2) * 360000)
