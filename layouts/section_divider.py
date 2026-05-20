"""section_divider — pleine page colorée pour introduire une section.

Visuel :
    ┌────────────────────────────────────────────────────┐
    │                                                    │
    │  ▌  PARTIE — TAG                                   │
    │  ▌                                                 │
    │  ▌  TITRE PRINCIPAL DE                             │
    │  ▌  LA SECTION                                     │
    │                                                    │
    │  Sous-titre éventuel.                              │
    │                                                    │
    │                                                 NN │
    └────────────────────────────────────────────────────┘
    fond `primary-deep` · texte blanc

Usage :
    section_divider.render(slide, charte,
        tag="PARTIE 1",
        title="TITRE DE SECTION",
        subtitle="Sous-titre descriptif optionnel...",
        page_num=2)
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, para, run,
)


def render(slide, ca, *,
           tag: str,
           title: str,
           subtitle: str,
           page_num: int):
    """Render a full-bleed section divider."""
    # Full bleed background in primary-deep
    add_rect(slide, 0, 0, SLIDE_W_CM, SLIDE_H_CM, fill=ca.color("primary-deep"))

    # Vertical signature accent
    add_rect(slide, 2.0, 4.5, 0.4, 2.2, fill=ca.color("signature"))

    # eyebrow
    _, tf = add_text(slide, 2.8, 4.5, 25, 1.0, margins=(0,0,0,0))
    p = para(tf, first=True)
    run(p, f"PARTIE — {tag}", size=11, bold=True,
        color=ca.color("signature"), font=ca.font_primary)

    # title (large white)
    _, tf = add_text(slide, 2.8, 5.4, 28, 4.5, margins=(0,0,0,0))
    p = para(tf, first=True, line_spacing=1.0, space_after=8)
    run(p, title, size=36, bold=True, color=ca.color("bg"), font=ca.font_primary)

    # subtitle
    _, tf = add_text(slide, 2.8, 9.6, 24, 3.5, margins=(0,0,0,0))
    p = para(tf, first=True, line_spacing=1.3)
    run(p, subtitle, size=15, color=ca.color("panel-mint"), font=ca.font_primary)

    # page num bottom-right
    _, tf = add_text(slide, SLIDE_W_CM - 3, SLIDE_H_CM - 1.4, 2, 0.7,
                     anchor="m", margins=(0,0,0,0))
    p = para(tf, first=True, align="right")
    run(p, f"{page_num:02d}", size=14, bold=True,
        color=ca.color("signature"), font=ca.font_primary)
