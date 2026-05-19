"""Internal helper : top header strip + page number + section tag.

Used by content layouts that need a recurring header (event fiches, etc.).
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM,
    add_rect, add_text, add_image, para, run,
)


def draw(slide, ca, *,
         page_num: int,
         section_tag: str | None = None,
         brand_text: str = "Événements stratégiques",
         logo_path: str | None = None,
         logo_h_cm: float = 0.75):
    """Draw the standard top header. Idempotent per slide.

    `logo_h_cm` controls the height of the brand logo at top-left. Width is
    auto-scaled to preserve aspect ratio. Brand text is placed just to the
    right of the logo, so wide horizontal logos push it further right.
    """
    # thin top accent bar
    add_rect(slide, 0, 0, SLIDE_W_CM, 0.18, fill=ca.color("primary"))

    text_x = 0.9
    if logo_path:
        pic = add_image(slide, logo_path, 0.9, 0.55, h_cm=logo_h_cm)
        if pic is not None:
            # text starts just after the logo's actual rendered width
            text_x = 0.9 + pic.width / 360000 + 0.4  # EMU → cm + gap

    _, tf = add_text(slide, text_x, 0.55, SLIDE_W_CM - text_x - 5.5, 0.7,
                     margins=(0,0,0,0))
    p = para(tf, first=True)
    run(p, brand_text, size=9, color=ca.color("muted"), font=ca.font_primary)

    # section tag (right)
    if section_tag:
        tag_w = 3.0
        x0 = SLIDE_W_CM - 0.9 - tag_w - 1.2
        add_rect(slide, x0, 0.5, tag_w, 0.55, fill=ca.color("panel-cream"))
        _, tf = add_text(slide, x0, 0.5, tag_w, 0.55, anchor="m",
                         margins=(0.1, 0.05, 0.1, 0.05))
        p = para(tf, first=True, align="center")
        run(p, section_tag, size=8.5, bold=True,
            color=ca.color("primary-deep"), font=ca.font_primary)

    # page number (right)
    _, tf = add_text(slide, SLIDE_W_CM - 1.8, 0.5, 1.0, 0.55,
                     anchor="m", margins=(0,0,0,0))
    p = para(tf, first=True, align="right")
    run(p, f"{page_num:02d}", size=11, bold=True,
        color=ca.color("primary-deep"), font=ca.font_primary)
