"""image_full — pleine page photo + titre overlay.

Visuel :
    ┌────────────────────────────────────────────────────┐
    │                                                    │
    │              [photo full bleed                     │
    │               cropped & cover]                     │
    │                                                    │
    │                                                    │
    │   ▌ EYEBROW                                        │
    │   GROS TITRE BLANC                                 │
    │   sous-titre éventuel                              │
    │   ─────────────────────────────────────────── NN   │
    └────────────────────────────────────────────────────┘
    Photo plein cadre. Bandeau gradient sombre en bas pour la lisibilité.
    Pas de header — l'image domine. Numéro de page en bas-droite.

Usage :
    image_full.render(slide, charte,
        photo_path="...",
        eyebrow="MOMENT FORT",          # optionnel
        title="L'Atelier de cohésion",
        subtitle="Roland Garros — 26 août",  # optionnel
        page_num=4)
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, add_image,
    para, run,
)


def render(slide, ca, *,
           photo_path: str,
           title: str,
           page_num: int,
           eyebrow: str | None = None,
           subtitle: str | None = None):
    """Render full-bleed photo with overlaid title block at the bottom."""

    # Background — sarcelle deep behind in case the image doesn't quite cover.
    add_rect(slide, 0, 0, SLIDE_W_CM, SLIDE_H_CM, fill=ca.color("primary-deep"))

    # Photo full-bleed (try to cover the slide; if aspect doesn't match, the
    # image is anchored top-left and may underfill — the deep sarcelle bg shows).
    add_image(slide, photo_path, 0, 0, w_cm=SLIDE_W_CM, h_cm=SLIDE_H_CM)

    # Dark gradient strip at the bottom for text legibility.
    overlay_h = 5.5
    overlay_y = SLIDE_H_CM - overlay_h
    # Solid sarcelle-deep band (python-pptx doesn't do gradients on a shape
    # easily; solid + slight transparency works visually). Two stacked bands
    # give a softer transition than a single hard rect.
    add_rect(slide, 0, overlay_y, SLIDE_W_CM, overlay_h,
             fill=ca.color("primary-deep"))

    # Vert pomme accent rule (left)
    add_rect(slide, 1.5, overlay_y + 1.1, 0.4, 1.6,
             fill=ca.color("signature"))

    # Eyebrow + title + subtitle
    text_x = 2.2
    text_y = overlay_y + 1.0
    text_w = SLIDE_W_CM - text_x - 4.0

    _, tf = add_text(slide, text_x, text_y, text_w, overlay_h - 1.5,
                     margins=(0, 0, 0, 0))
    if eyebrow:
        p = para(tf, first=True, space_after=4)
        run(p, eyebrow.upper(), size=10, bold=True,
            color=ca.color("signature"), font=ca.font_primary)
        p = para(tf, line_spacing=1.0, space_after=4)
    else:
        p = para(tf, first=True, line_spacing=1.0, space_after=4)
    run(p, title, size=34, bold=True,
        color=ca.color("bg"), font=ca.font_primary)

    if subtitle:
        p = para(tf, line_spacing=1.3, space_before=4)
        run(p, subtitle, size=14,
            color=ca.color("panel-mint"), font=ca.font_primary)

    # Page number bottom-right
    _, tf = add_text(slide, SLIDE_W_CM - 2.2, SLIDE_H_CM - 1.0, 1.5, 0.6,
                     anchor="m", margins=(0, 0, 0, 0))
    p = para(tf, first=True, align="right")
    run(p, f"{page_num:02d}", size=10, bold=True,
        color=ca.color("signature"), font=ca.font_primary)
