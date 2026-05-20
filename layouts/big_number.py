"""big_number — KPI géant centré + label + contexte court.

Visuel :
    ┌────────────────────────────────────────────────────┐
    │                                                    │
    │   ▌ EYEBROW                                        │
    │                                                    │
    │           1 4 0 +                                  │
    │       (giant centered, 200pt+)                     │
    │                                                    │
    │       label en `signature` bold                    │
    │                                                    │
    │       contexte / source en muted                   │
    │                                                    │
    │   ──────────────────────────────────── NN          │
    └────────────────────────────────────────────────────┘
    Fond `panel-cream`, KPI `primary-deep` géant. Slide narrative forte.
    Pas de header.

Usage :
    big_number.render(slide, charte,
        value="140+",
        label="participants",
        context="Contexte court — événement, lieu, date",
        eyebrow="EN UN CHIFFRE",     # optionnel
        page_num=7)
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text,
    para, run,
)


def render(slide, ca, *,
           value: str,
           label: str,
           page_num: int,
           context: str | None = None,
           eyebrow: str | None = None):
    """Render a giant KPI slide."""

    # Cream background — softer than full white for hero stat
    add_rect(slide, 0, 0, SLIDE_W_CM, SLIDE_H_CM, fill=ca.color("panel-cream"))

    # Eyebrow (top-left)
    if eyebrow:
        add_rect(slide, 1.5, 1.5, 0.4, 0.7, fill=ca.color("signature"))
        _, tf = add_text(slide, 2.1, 1.5, 18, 0.7, anchor="m",
                         margins=(0, 0, 0, 0))
        p = para(tf, first=True)
        run(p, eyebrow.upper(), size=11, bold=True,
            color=ca.color("primary"), font=ca.font_primary)

    # Giant value — centered
    val_y = (SLIDE_H_CM - 8) / 2 - 1.5
    _, tf = add_text(slide, 1, val_y, SLIDE_W_CM - 2, 8,
                     anchor="m", margins=(0, 0, 0, 0))
    p = para(tf, first=True, align="center", line_spacing=0.9)
    run(p, value, size=180, bold=True,
        color=ca.color("primary-deep"), font=ca.font_primary)

    # Label
    label_y = val_y + 6.5
    _, tf = add_text(slide, 1, label_y, SLIDE_W_CM - 2, 1.5,
                     margins=(0, 0, 0, 0))
    p = para(tf, first=True, align="center", line_spacing=1.2)
    run(p, label, size=18, bold=True,
        color=ca.color("primary"), font=ca.font_primary)

    # Optional context line
    if context:
        ctx_y = label_y + 1.2
        _, tf = add_text(slide, 1, ctx_y, SLIDE_W_CM - 2, 1.0,
                         margins=(0, 0, 0, 0))
        p = para(tf, first=True, align="center", line_spacing=1.3)
        run(p, context, size=11, italic=True,
            color=ca.color("muted"), font=ca.font_primary)

    # Page number bottom-right
    _, tf = add_text(slide, SLIDE_W_CM - 2.2, SLIDE_H_CM - 1.0, 1.5, 0.6,
                     anchor="m", margins=(0, 0, 0, 0))
    p = para(tf, first=True, align="right")
    run(p, f"{page_num:02d}", size=10, bold=True,
        color=ca.color("primary-deep"), font=ca.font_primary)
