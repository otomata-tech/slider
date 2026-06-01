"""Gabarit : zoom société / opportunité (kit PCDI slide 18).

Logo cible + pastille de recommandation, intitulé de l'opportunité, fourchette
de valorisation, description, et chiffres-clés optionnels.
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, add_rect, add_round_rect, add_image, add_text, para, run,
)
from layouts._header import draw as draw_header, title_block, MARGIN_CM
from layouts import _components as C


def render(slide, ca, *,
           name: str,
           description: str,
           page_num: int,
           reco: str | None = None,
           valuation: str | None = None,
           logo_path: str | None = None,
           stats: list | None = None,
           eyebrow: str | None = None,
           section_tag: str | None = None,
           date_text: str | None = None):
    """`reco` : ex. « Recommandation : Build » → pastille verte.
    `valuation` : fourchette / angle d'entrée, en sous-titre."""
    add_rect(slide, 0, 0, SLIDE_W_CM, 19.05, fill=ca.color("bg"))
    draw_header(slide, ca, page_num=page_num, date_text=date_text,
                logo_path=ca.default("header_logo"))

    # logo cible (encart en haut à gauche)
    box = 2.6
    add_round_rect(slide, MARGIN_CM, 1.7, box, box,
                   fill=ca.color("bg-soft"), radius_frac=0.08)
    if logo_path:
        pic = add_image(slide, logo_path, MARGIN_CM + 0.3, 1.7 + 0.3,
                        w_cm=box - 0.6)
    else:
        _, tf = add_text(slide, MARGIN_CM, 1.7, box, box, anchor="m",
                         margins=(0, 0, 0, 0))
        p = para(tf, first=True, align="center")
        run(p, "LOGO\nCIBLE", size=9, bold=True, color=ca.color("muted-soft"),
            font=ca.font_primary)

    # pastille de recommandation (à droite du logo)
    if reco:
        C.pill(slide, ca, MARGIN_CM + box + 0.6, 2.0, text=reco, style="green",
               size=10, h_cm=0.8)

    # titre + valorisation
    title_block(slide, ca, title=name, subtitle=valuation,
                y_cm=4.8, w_cm=SLIDE_W_CM - 2 * MARGIN_CM)

    # description
    _, tf = add_text(slide, MARGIN_CM, 7.6, SLIDE_W_CM - 2 * MARGIN_CM, 4.0,
                     margins=(0, 0, 0, 0))
    p = para(tf, first=True, space_after=2)
    run(p, "DESCRIPTION", size=8, bold=True, color=ca.color("muted-soft"),
        font=ca.font_primary)
    p = para(tf, line_spacing=1.5)
    run(p, description, size=11, color=ca.color("text-soft"),
        font=ca.font_primary)

    if stats:
        n = min(3, len(stats))
        gap = 0.8
        cw = (SLIDE_W_CM - 2 * MARGIN_CM - (n - 1) * gap) / n
        cy = 13.2
        for i, (num, lab) in enumerate(stats[:n]):
            C.stat_card(slide, ca, MARGIN_CM + i * (cw + gap), cy, cw, 3.4,
                        number=num, label=lab, number_pt=28)
