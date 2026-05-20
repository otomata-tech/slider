"""portrait_grid — grille de portraits + nom + rôle.

Visuel :
    ┌────────────────────────────────────────────────────┐
    │ ▌ header  brand · TAG · NN                          │
    │                                                    │
    │ TITRE GRILLE                                       │
    │ ──                                                 │
    │ accroche / contexte court                          │
    │                                                    │
    │  ┌──┐  ┌──┐  ┌──┐  ┌──┐                            │
    │  │ph│  │ph│  │ph│  │ph│                            │
    │  └──┘  └──┘  └──┘  └──┘                            │
    │  Nom1  Nom2  Nom3  Nom4                            │
    │  rôle  rôle  rôle  rôle                            │
    │                                                    │
    │  ┌──┐  ┌──┐  …                                     │
    └────────────────────────────────────────────────────┘
    Grille 2 à 6 colonnes, hauteur auto. Photo carrée + nom + rôle.

Usage :
    portrait_grid.render(slide, charte,
        title="L'équipe d'animation",
        people=[
            {"photo": "...", "name": "Marie Durand", "role": "Coach"},
            {"photo": "...", "name": "Paul Martin",  "role": "Facilitateur"},
            ...
        ],
        page_num=6,
        section_tag=None,
        brand_logo_path=ca.asset(...),
        subtitle=None)
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, add_image, fit_image,
    para, run,
)
from layouts._header import draw as draw_header


def render(slide, ca, *,
           title: str,
           people: list[dict],
           page_num: int,
           subtitle: str | None = None,
           section_tag: str | None = None,
           brand_logo_path: str | None = None):
    """Render a grid of portraits. Each person is {photo, name, role}.

    `brand_logo_path` falls back to ``charte.default("header_logo")`` when None.
    """
    if brand_logo_path is None:
        brand_logo_path = ca.default("header_logo")

    add_rect(slide, 0, 0, SLIDE_W_CM, SLIDE_H_CM, fill=ca.color("bg"))
    draw_header(slide, ca, page_num=page_num, section_tag=section_tag,
                logo_path=brand_logo_path)

    # Title block
    _, tf = add_text(slide, 0.9, 1.7, SLIDE_W_CM - 1.8, 1.5, margins=(0, 0, 0, 0))
    p = para(tf, first=True, line_spacing=1.05, space_after=2)
    run(p, title, size=22, bold=True,
        color=ca.color("text-strong"), font=ca.font_primary)

    add_rect(slide, 0.9, 3.4, 2.8, 0.08, fill=ca.color("signature"))

    if subtitle:
        _, tf = add_text(slide, 0.9, 3.6, SLIDE_W_CM - 1.8, 0.8, margins=(0, 0, 0, 0))
        p = para(tf, first=True, line_spacing=1.3)
        run(p, subtitle, size=11,
            color=ca.color("muted"), font=ca.font_primary)
        grid_y = 5.0
    else:
        grid_y = 4.2

    # Grid sizing: choose columns based on count (max 5 per row → readable)
    n = len(people)
    cols = min(5, max(2, n if n <= 5 else (n + 1) // 2))
    rows = (n + cols - 1) // cols

    grid_w = SLIDE_W_CM - 1.8
    cell_w = grid_w / cols
    photo_size = min(cell_w - 1.0, 4.0)  # square photo
    label_h = 1.6
    cell_h = photo_size + label_h + 0.6

    for i, person in enumerate(people):
        r, c = divmod(i, cols)
        cx = 0.9 + c * cell_w + (cell_w - photo_size) / 2
        cy = grid_y + r * cell_h

        # Background card behind photo (subtle panel)
        add_rect(slide, cx - 0.2, cy - 0.2, photo_size + 0.4, photo_size + 0.4,
                 fill=ca.color("panel-mint"))

        if person.get("photo"):
            pic = add_image(slide, person["photo"], cx, cy,
                            w_cm=photo_size, h_cm=photo_size)
            fit_image(pic, max_w_cm=photo_size, max_h_cm=photo_size)

        # Name + role under the photo
        label_y = cy + photo_size + 0.25
        _, tf = add_text(slide, cx - 0.4, label_y, photo_size + 0.8, label_h,
                         margins=(0, 0, 0, 0))
        p = para(tf, first=True, align="center", line_spacing=1.2, space_after=2)
        run(p, person.get("name", ""), size=11, bold=True,
            color=ca.color("primary-deep"), font=ca.font_primary)
        if person.get("role"):
            p = para(tf, align="center", line_spacing=1.2)
            run(p, person["role"], size=9,
                color=ca.color("muted"), font=ca.font_primary)
