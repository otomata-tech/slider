"""Internal helper : chrome de page PCDI (kit Capital Innovation).

Ossature constante des pages intérieures :
  1. wordmark + numéro de page (haut-gauche), capitales tracées
  2. mention d'usage (haut-droite)
  3. filet noir 1px séparant l'en-tête du contenu
  4. pied de page : date (gauche) + logo Crédit Agricole (droite)

Le bloc de titre (titre capitales + sous-titre vert) reste à la charge de
chaque masque — il fait partie du contenu, pas du chrome.
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, add_image, para, run, right_align,
)

# Marge de page : 60px sur canvas 1920 ≈ 1.06 cm.
MARGIN_CM = 1.06


def _track(r, centipt: int):
    """Letter-spacing (tracking) en centièmes de point sur un run."""
    r._r.get_or_add_rPr().set("spc", str(centipt))


def draw(slide, ca, *,
         page_num: int,
         brand_text: str = "PCDI – Capital Innovation",
         usage_text: str = "Usage Interne / Internal Use",
         date_text: str | None = None,
         logo_path: str | None = None,
         logo_h_cm: float = 0.7,
         section_tag: str | None = None):  # déprécié — ignoré (compat appelants)
    """Dessine le chrome standard. Idempotent par slide.

    `section_tag` est conservé pour compat mais n'est plus rendu (le kit n'a
    pas de pastille de section dans le chrome).
    """
    top_y = 0.62
    half = SLIDE_W_CM / 2

    # 1. wordmark + numéro de page (haut-gauche), capitales tracées
    _, tf = add_text(slide, MARGIN_CM, top_y, half - MARGIN_CM, 0.5,
                     margins=(0, 0, 0, 0))
    p = para(tf, first=True)
    r = run(p, f"{page_num:02d}   {brand_text.upper()}",
            size=8, color=ca.color("muted"), font=ca.font_primary)
    _track(r, 60)

    # 2. mention d'usage (haut-droite), alignée à droite
    _, tf = add_text(slide, half, top_y, half - MARGIN_CM, 0.5,
                     margins=(0, 0, 0, 0))
    p = para(tf, first=True, align="right")
    r = run(p, usage_text.upper(),
            size=8, color=ca.color("muted-soft"), font=ca.font_primary)
    _track(r, 60)

    # 3. filet noir 1px sous l'en-tête
    add_rect(slide, MARGIN_CM, 1.28, SLIDE_W_CM - 2 * MARGIN_CM, 0.03,
             fill=ca.color("text-strong"))

    # 4. pied de page : date (gauche) + logo (droite)
    foot_y = SLIDE_H_CM - 1.15
    if date_text:
        _, tf = add_text(slide, MARGIN_CM, foot_y, 6.0, 0.55, anchor="m",
                         margins=(0, 0, 0, 0))
        p = para(tf, first=True)
        run(p, date_text, size=8, color=ca.color("muted-soft"),
            font=ca.font_primary)
    if logo_path:
        pic = add_image(slide, logo_path, 0, foot_y - 0.15, h_cm=logo_h_cm)
        if pic is not None:
            right_align(pic, SLIDE_W_CM, margin_cm=MARGIN_CM)


def title_block(slide, ca, *, title: str,
                eyebrow: str | None = None,
                subtitle: str | None = None,
                y_cm: float = 1.6,
                w_cm: float | None = None):
    """Bloc de titre standard : eyebrow + titre CAPITALES + sous-titre vert.
    Élément de contenu commun à toutes les pages intérieures du kit."""
    if w_cm is None:
        w_cm = SLIDE_W_CM - 2 * MARGIN_CM
    _, tf = add_text(slide, MARGIN_CM, y_cm, w_cm, 2.6, margins=(0, 0, 0, 0))
    if eyebrow:
        p = para(tf, first=True, space_after=4)
        r = run(p, eyebrow.upper(), size=8, color=ca.color("muted-soft"),
                font=ca.font_primary)
        _track(r, 60)
    p = para(tf, first=(eyebrow is None), space_after=3, line_spacing=1.05)
    run(p, title.upper(), size=22, bold=True, color=ca.color("text"),
        font=ca.font_primary)
    if subtitle:
        p = para(tf, space_after=0, line_spacing=1.15)
        run(p, subtitle, size=14, color=ca.color("primary"), font=ca.font_primary)
    return tf
