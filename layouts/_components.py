"""Composants réutilisables du kit PCDI (Capital Innovation).

Mécaniques distinctives du kit :
  - marker_list : listes à marqueur « + » vert (ou « – » rouge pour les risques),
    qui remplacent la puce ronde.
  - stat_card   : carte mint avec un chiffre-clé vert et un libellé encre.
  - pill        : pastille / bandeau arrondi (statut, recommandation, audience).

Tout passe par la charte (couleurs, police) — aucune valeur hardcodée.
"""
from __future__ import annotations

from lib.pptx_helpers import (
    add_round_rect, add_text, para, run, set_hanging, set_line,
)


def marker_list(slide, ca, x_cm, y_cm, w_cm, items, *,
                kind: str = "plus",
                size: float = 11,
                line_spacing: float = 1.3,
                space_after: float = 8,
                h_cm: float = 10.0):
    """Liste à marqueur typographique.

    `kind` : "plus" (marqueur « + » vert) ou "risk" (marqueur « – » rouge).
    `items` : liste de str, ou de tuples (terme_gras, suite) pour mettre le
              terme-clé en gras en début d'item.
    """
    marker = "+" if kind == "plus" else "–"
    mcolor = ca.color("primary") if kind == "plus" else ca.color("alert")

    _, tf = add_text(slide, x_cm, y_cm, w_cm, h_cm, margins=(0, 0, 0, 0))
    for i, item in enumerate(items):
        p = para(tf, first=(i == 0), space_after=space_after,
                 line_spacing=line_spacing)
        set_hanging(p, 0.7)
        run(p, f"{marker}  ", size=size, bold=True, color=mcolor,
            font=ca.font_primary)
        if isinstance(item, (tuple, list)):
            lead, rest = item
            run(p, lead, size=size, bold=True, color=ca.color("text"),
                font=ca.font_primary)
            if rest:
                run(p, rest, size=size, color=ca.color("text"),
                    font=ca.font_primary)
        else:
            run(p, item, size=size, color=ca.color("text"),
                font=ca.font_primary)
    return tf


def stat_card(slide, ca, x_cm, y_cm, w_cm, h_cm, *,
              number: str, label: str,
              number_pt: float = 32):
    """Carte mint : chiffre-clé vert + libellé encre (kit slide 11)."""
    add_round_rect(slide, x_cm, y_cm, w_cm, h_cm,
                   fill=ca.color("panel-mint"), radius_frac=0.10)
    pad = 0.7
    _, tf = add_text(slide, x_cm + pad, y_cm + pad, w_cm - 2 * pad,
                     h_cm - 2 * pad, anchor="m", margins=(0, 0, 0, 0))
    p = para(tf, first=True, space_after=4, line_spacing=1.0)
    run(p, number, size=number_pt, bold=True, color=ca.color("primary"),
        font=ca.font_primary)
    p = para(tf, space_after=0, line_spacing=1.15)
    run(p, label, size=11, color=ca.color("text"), font=ca.font_primary)


def pill(slide, ca, x_cm, y_cm, *, text: str, style: str = "mint",
         size: float = 9, h_cm: float = 0.7, pad_cm: float = 0.45):
    """Pastille / bandeau arrondi.

    `style` : "mint" (fond mint, texte vert) · "green" (fond vert, texte blanc)
              · "outline" (contour, texte encre). Largeur auto ≈ longueur texte.
    Retourne la largeur en cm pour chaîner plusieurs pastilles.
    """
    # largeur approximative : ~0.55× la taille de police par caractère + padding
    w_cm = pad_cm * 2 + len(text) * (size * 0.021)

    if style == "green":
        bg, fg = ca.color("primary"), ca.color("bg")
    elif style == "outline":
        bg, fg = ca.color("bg"), ca.color("text")
    else:  # mint
        bg, fg = ca.color("panel-mint"), ca.color("primary")

    shape = add_round_rect(slide, x_cm, y_cm, w_cm, h_cm, fill=bg, radius_frac=0.5)
    if style == "outline":
        set_line(shape, ca.color("rule"), width_pt=1.0)
    _, tf = add_text(slide, x_cm, y_cm, w_cm, h_cm, anchor="m",
                     margins=(0, 0, 0, 0))
    p = para(tf, first=True, align="center", space_after=0)
    r = run(p, text.upper(), size=size, bold=True, color=fg,
            font=ca.font_primary)
    r._r.get_or_add_rPr().set("spc", "40")
    return w_cm
