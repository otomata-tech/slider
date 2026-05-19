"""quote — citation centrée + attribution.

Visuel :
    ┌────────────────────────────────────────────────────┐
    │                                                    │
    │                  ▌                                 │
    │          « Une citation marquante                  │
    │            sur 1 à 3 lignes,                       │
    │             en italique. »                         │
    │                                                    │
    │                — AUTEUR · fonction                 │
    │                                                    │
    │                                              NN    │
    └────────────────────────────────────────────────────┘
    Fond crème, citation italique grande, accent vert pomme à gauche.
    Pas de header — slide de respiration narrative.

Usage :
    quote.render(slide, charte,
        text="L'innovation, c'est dire non à 1000 choses.",
        author="Steve Jobs",
        role="Apple",                    # optionnel
        page_num=5)
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text,
    para, run,
)


def render(slide, ca, *,
           text: str,
           author: str,
           page_num: int,
           role: str | None = None):
    """Render a centered citation slide."""

    # Cream background
    add_rect(slide, 0, 0, SLIDE_W_CM, SLIDE_H_CM, fill=ca.color("panel-cream"))

    # Vertical accent bar (signature green) just left of the quote block
    bar_h = 4.5
    bar_y = (SLIDE_H_CM - bar_h) / 2 - 0.5
    add_rect(slide, SLIDE_W_CM / 2 - 11.0, bar_y, 0.18, bar_h,
             fill=ca.color("signature"))

    # Quote text — centered, large italic
    quote_y = (SLIDE_H_CM - 8) / 2
    _, tf = add_text(slide, 5, quote_y, SLIDE_W_CM - 10, 8,
                     anchor="m", margins=(0, 0, 0, 0))
    p = para(tf, first=True, align="center", line_spacing=1.3)
    run(p, f"« {text} »", size=28, italic=True, bold=False,
        color=ca.color("primary-deep"), font=ca.font_primary)

    # Attribution — below quote
    attrib_y = quote_y + 6.5
    _, tf = add_text(slide, 5, attrib_y, SLIDE_W_CM - 10, 1.0,
                     margins=(0, 0, 0, 0))
    p = para(tf, first=True, align="center", line_spacing=1.2)
    run(p, "— ", size=13,
        color=ca.color("muted"), font=ca.font_primary)
    run(p, author.upper(), size=13, bold=True,
        color=ca.color("primary"), font=ca.font_primary)
    if role:
        run(p, "  ·  " + role, size=13,
            color=ca.color("muted"), font=ca.font_primary)

    # Page number bottom-right
    _, tf = add_text(slide, SLIDE_W_CM - 2.2, SLIDE_H_CM - 1.0, 1.5, 0.6,
                     anchor="m", margins=(0, 0, 0, 0))
    p = para(tf, first=True, align="right")
    run(p, f"{page_num:02d}", size=10, bold=True,
        color=ca.color("primary-deep"), font=ca.font_primary)
