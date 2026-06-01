"""text_image — split 50/50 photo + texte.

Visuel :
    ┌────────────────────────────────────────────────────┐
    │ ▌ header  brand · TAG · NN                          │
    │                                                    │
    │ ┌──────────────┐  EYEBROW                          │
    │ │              │  TITRE GRAS                       │
    │ │   [photo     │  ──                               │
    │ │   pleine     │  paragraphe d'intro 2-3 lignes    │
    │ │   colonne]   │                                   │
    │ │              │  ▸ point clé 1                    │
    │ │              │  ▸ point clé 2                    │
    │ │              │  ▸ point clé 3                    │
    │ └──────────────┘                                   │
    │                                                    │
    └────────────────────────────────────────────────────┘
    Photo gauche, contenu droite. Variante moins dense que event_fiche,
    pour présenter un atelier, un moment fort, une initiative.

Usage :
    text_image.render(slide, charte,
        title="L'Atelier Innovation",
        eyebrow="ATELIER 2",                # optionnel
        photo_path="...",
        intro="Une matinée pour ...",       # optionnel
        bullets=["...", "..."],             # optionnel
        page_num=9,
        section_tag=None,
        brand_logo_path=ca.asset(...),
        photo_side="left")                  # "left" (default) ou "right"
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, add_image, fit_image,
    para, run, set_hanging,
)
from layouts._header import draw as draw_header


def render(slide, ca, *,
           title: str,
           page_num: int,
           photo_path: str | None = None,
           eyebrow: str | None = None,
           intro: str | None = None,
           bullets: list[str] | None = None,
           photo_side: str = "left",
           section_tag: str | None = None,
           brand_logo_path: str | None = None):
    """Render a 50/50 photo + text slide.

    `brand_logo_path` falls back to ``charte.default("header_logo")`` when None.
    """
    if brand_logo_path is None:
        brand_logo_path = ca.default("header_logo")

    add_rect(slide, 0, 0, SLIDE_W_CM, SLIDE_H_CM, fill=ca.color("bg"))
    draw_header(slide, ca, page_num=page_num, section_tag=section_tag,
                logo_path=brand_logo_path)

    # Layout columns : photo half + text half on a 33.867cm slide.
    # Margins 0.9 each side, gutter 0.8 → photo 14, text ~17.
    photo_w = 14.0
    photo_y = 1.7
    photo_h = SLIDE_H_CM - photo_y - 1.7  # clearance pour le pied de page

    if photo_side == "left":
        photo_x = 0.9
        text_x  = photo_x + photo_w + 0.8
    else:
        photo_x = SLIDE_W_CM - photo_w - 0.9
        text_x  = 0.9

    text_w = SLIDE_W_CM - text_x - 0.9
    if photo_side == "left":
        # text fills from text_x to right margin
        pass
    else:
        # text fills from left margin to start of photo
        text_w = photo_x - text_x - 0.8

    # Photo (with `primary-deep` placeholder if missing)
    if photo_path:
        # Background panel behind the image (in case aspect doesn't fill)
        add_rect(slide, photo_x, photo_y, photo_w, photo_h,
                 fill=ca.color("panel-mint"))
        pic = add_image(slide, photo_path, photo_x, photo_y,
                        w_cm=photo_w, h_cm=photo_h)
        fit_image(pic, max_w_cm=photo_w, max_h_cm=photo_h)
    else:
        # placeholder — `primary-deep` band
        add_rect(slide, photo_x, photo_y, photo_w, photo_h,
                 fill=ca.color("primary-deep"))

    # Right side : single text frame stacking eyebrow → title → underline →
    # intro → bullets. Stacking via paragraphs avoids overlap from fixed-height
    # boxes when content varies.
    text_y = photo_y + 0.3
    text_h = photo_h - 0.6
    _, tf = add_text(slide, text_x, text_y, text_w, text_h,
                     margins=(0, 0, 0, 0))

    first = True
    if eyebrow:
        p = para(tf, first=first, space_after=4)
        first = False
        r = run(p, eyebrow.upper(), size=8, bold=True,
                color=ca.color("muted-soft"), font=ca.font_primary)
        r._r.get_or_add_rPr().set("spc", "60")

    p = para(tf, first=first, line_spacing=1.05, space_after=10)
    first = False
    run(p, title.upper(), size=22, bold=True,
        color=ca.color("text"), font=ca.font_primary)

    if intro:
        p = para(tf, line_spacing=1.5, space_after=12)
        run(p, intro, size=11,
            color=ca.color("text-soft"), font=ca.font_primary)

    if bullets:
        for item in bullets:
            p = para(tf, space_before=4, space_after=6, line_spacing=1.3)
            set_hanging(p, 0.7)
            run(p, "+  ", size=11, bold=True,
                color=ca.color("primary"), font=ca.font_primary)
            run(p, item, size=11,
                color=ca.color("text"), font=ca.font_primary)
