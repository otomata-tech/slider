"""cover_split — couverture deux colonnes : image+brand à gauche, titre à droite.

Visuel :
    ┌─────────────────────┬──────────────────────────────┐
    │ ▌ Brand label       │                              │
    │ ▌ Eyebrow           │  Titre principal (2 lignes)  │
    │ ▌                   │                              │
    │ ▌  [ photo carrée ] │  Sous-titre (2 lignes)       │
    │ ▌                   │  Accroche (2 lignes max)     │
    │ ▌ « citation »      │                              │
    │ ▌                   │  ────────────                │
    │                     │  [logo client]   signoff     │
    └─────────────────────┴──────────────────────────────┘
    fond sarcelle foncé        fond crème

Usage typique :
    cover_split.render(slide, charte,
        brand_label="CRÉDIT AGRICOLE",
        eyebrow="BENCHMARK · 2026 — 2027",
        photo_path=ca.asset("photo/ca-siege.jpg"),
        photo_caption="« Agir chaque jour... »",
        title_lines=["Événements", "stratégiques."],
        subtitle_lines=["Capter l'attention", "des décideurs."],
        accroche=["26 rendez-vous incontournables —",
                  "France · Europe · Cercles d'influence."],
        logo_path=ca.asset("logo/ca-logo-baseline.png"),
        signoff="Présenté par La Fabrique by CA · 2026")
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, add_image, para, run,
)


def render(slide, ca, *,
           brand_label: str,
           eyebrow: str,
           title_lines: list[str],
           subtitle_lines: list[str],
           accroche: list[str],
           signoff: str,
           photo_path: str | None = None,
           photo_caption: str | None = None,
           logo_path: str | None = None):
    """Render the split cover. See module docstring for layout.

    `photo_path` and `logo_path` fall back to the charte's defaults
    (``defaults.cover_photo`` and ``defaults.cover_logo`` in tokens.json) when
    the caller passes ``None``. Pass an explicit path to override, or pass an
    empty string ``""`` to disable the asset entirely.
    """
    # Auto-inject charte defaults when caller didn't specify
    if photo_path is None:
        photo_path = ca.default("cover_photo")
    if logo_path is None:
        logo_path = ca.default("cover_logo")

    half_w = SLIDE_W_CM * 0.46

    # backgrounds
    add_rect(slide, 0, 0, half_w, SLIDE_H_CM, fill=ca.color("primary-deep"))
    add_rect(slide, half_w, 0, SLIDE_W_CM - half_w, SLIDE_H_CM, fill=ca.color("panel-cream"))

    # vertical signature-green accent strip
    add_rect(slide, half_w, 0, 0.18, SLIDE_H_CM, fill=ca.color("signature"))

    # === LEFT — branding + photo ============================================
    _, tf = add_text(slide, 1.3, 1.2, 12, 0.8, margins=(0,0,0,0))
    p = para(tf, first=True)
    run(p, brand_label, size=10, bold=True, color=ca.color("bg"), font=ca.font_primary)

    _, tf = add_text(slide, 1.3, 2.0, 12, 0.7, margins=(0,0,0,0))
    p = para(tf, first=True)
    run(p, eyebrow, size=9, bold=True, color=ca.color("signature"), font=ca.font_primary)

    if photo_path:
        photo_size = 13.5
        photo_x = (half_w - photo_size) / 2
        photo_y = 3.2
        add_image(slide, photo_path, photo_x, photo_y, w_cm=photo_size, h_cm=photo_size)
        if photo_caption:
            _, tf = add_text(slide, 1.3, photo_y + photo_size + 0.3, half_w - 2.6, 0.6,
                             margins=(0,0,0,0))
            p = para(tf, first=True)
            run(p, photo_caption, size=9, italic=True,
                color=ca.color("panel-mint"), font=ca.font_primary)

    # === RIGHT — title + subtitle + logo ====================================
    right_x = half_w + 1.5

    _, tf = add_text(slide, right_x, 2.8, 14, 5, margins=(0,0,0,0))
    for i, line in enumerate(title_lines):
        p = para(tf, first=(i==0), line_spacing=1.0, space_after=4)
        run(p, line, size=int(ca.token_size("h1")), bold=True,
            color=ca.color("primary-deep"), font=ca.font_primary)

    _, tf = add_text(slide, right_x, 8.8, 14, 4.5, margins=(0,0,0,0))
    for i, line in enumerate(subtitle_lines):
        p = para(tf, first=(i==0), space_after=4 if i == 0 else 10)
        run(p, line, size=22, bold=True, color=ca.color("primary"), font=ca.font_primary)
    for line in accroche:
        p = para(tf, space_after=2)
        run(p, line, size=12, color=ca.color("text"), font=ca.font_primary)

    # footer rule
    add_rect(slide, half_w + 0.18, SLIDE_H_CM - 1.7,
             SLIDE_W_CM - half_w - 0.18, 0.03, fill=ca.color("rule"))

    if logo_path:
        add_image(slide, logo_path,
                  x_cm=SLIDE_W_CM - 1.3 - 7.0,
                  y_cm=SLIDE_H_CM - 1.4,
                  h_cm=0.95)

    _, tf = add_text(slide, right_x, SLIDE_H_CM - 1.2, 6, 0.7, margins=(0,0,0,0))
    p = para(tf, first=True)
    run(p, signoff, size=9, italic=True, color=ca.color("muted"), font=ca.font_primary)
