"""event_fiche — fiche événement détaillée (benchmark, partenaire, opportunity).

Visuel :
    ┌────────────────────────────────────────────────────┐
    │ ▌ header bar + brand logo · TAG · NN               │
    │                                                    │
    │ NAME EVENT                          [logo event]   │
    │ TITRE / ACCROCHE (grande typo)                     │
    │ ──                                                 │
    │ DATE  jj/mm/aaaa    LIEU  Paris                    │
    │                                                    │
    │ AUDIENCE          ┌──── RECOMMANDATIONS ─────────┐ │
    │ ...               │ Positionnement               │ │
    │ TAILLE/PORTÉE     │ ...italic...                 │ │
    │ ...               │ Activations                  │ │
    │ FORMAT            │ ● item 1                     │ │
    │ ...               │   → sub                      │ │
    │ INFOS             │ ● item 2                     │ │
    │ ...               │ Site : ...                   │ │
    │ INTÉRÊTS          └──────────────────────────────┘ │
    │ ▸ ...                                              │
    │                                                    │
    │ ▌ ★ Highlight bottom strip                         │
    └────────────────────────────────────────────────────┘

Usage :
    event_fiche.render(slide, charte,
        name="<EVENT NAME>",
        title="ACCROCHE EN GRANDE TYPO",
        date="<dates>", lieu="<lieu>",
        audience="...", taille="...", format="...", infos="...",
        speakers="..." (optional),
        interets=["bullet 1", ...],
        positionnement="Positionner <marque> comme...",
        activations=[("Prise de parole", "keynote / panel"), ...],
        site="https://...",
        page_num=3,
        section_tag="<TAG>",
        logo_path=ch.asset(...) or None,
        brand_logo_path=ch.asset("logo/main.png"),
        highlight="Édition anniversaire 10 ans")
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, add_image, fit_image, right_align,
    para, run,
)
from layouts._header import draw as draw_header


def render(slide, ca, *,
           name: str,
           title: str,
           date: str,
           lieu: str,
           audience: str,
           taille: str,
           format: str,
           infos: str,
           interets: list[str],
           positionnement: str,
           activations: list[tuple[str, str | None]],
           site: str,
           page_num: int,
           section_tag: str | None = None,
           speakers: str | None = None,
           highlight: str | None = None,
           logo_path: str | None = None,
           brand_logo_path: str | None = None):
    """Render a single event card. See module docstring for layout.

    `brand_logo_path` falls back to ``charte.default("header_logo")`` when None.
    """
    # Auto-inject charte default header logo
    if brand_logo_path is None:
        brand_logo_path = ca.default("header_logo")

    # white background
    add_rect(slide, 0, 0, SLIDE_W_CM, SLIDE_H_CM, fill=ca.color("bg"))

    draw_header(slide, ca,
                page_num=page_num, section_tag=section_tag,
                logo_path=brand_logo_path)

    # --- event logo (top-right of title area) ---
    logo_box_w, logo_box_h = 5.5, 2.0
    logo_box_x = SLIDE_W_CM - 0.9 - logo_box_w
    logo_box_y = 1.55
    title_w = SLIDE_W_CM - 1.8 - (logo_box_w + 0.5 if logo_path else 0)

    if logo_path:
        pic = add_image(slide, logo_path, logo_box_x, logo_box_y, h_cm=logo_box_h)
        fit_image(pic, max_w_cm=logo_box_w, max_h_cm=logo_box_h)
        right_align(pic, slide_right_cm=SLIDE_W_CM - 0.9)

    # --- title block ---
    _, tf = add_text(slide, 0.9, 1.55, title_w, 2.0, margins=(0,0,0,0))
    p = para(tf, first=True, space_after=2)
    run(p, name.upper(), size=11, bold=True,
        color=ca.color("primary"), font=ca.font_primary)
    p = para(tf, line_spacing=1.05, space_after=2)
    run(p, title, size=20, bold=True,
        color=ca.color("text-strong"), font=ca.font_primary)

    # underline accent
    add_rect(slide, 0.9, 3.7, 2.8, 0.08, fill=ca.color("signature"))

    # --- meta bar (date / lieu) ---
    meta_y = 3.95
    _, tf = add_text(slide, 0.9, meta_y, SLIDE_W_CM - 1.8, 0.9, margins=(0,0,0,0))
    p = para(tf, first=True, line_spacing=1.2)
    run(p, "DATE  ",     size=8, bold=True, color=ca.color("muted"), font=ca.font_primary)
    run(p, date,         size=10, bold=True, color=ca.color("text"), font=ca.font_primary)
    run(p, "     LIEU  ", size=8, bold=True, color=ca.color("muted"), font=ca.font_primary)
    run(p, lieu,         size=10, bold=True, color=ca.color("text"), font=ca.font_primary)

    # --- columns ---
    col_left_x   = 0.9
    col_left_w   = 18.0
    col_right_x  = col_left_x + col_left_w + 0.6
    col_right_w  = SLIDE_W_CM - col_right_x - 0.9
    content_y    = 5.0
    content_h    = SLIDE_H_CM - content_y - 1.3

    # -- left column : facts --
    _, tf = add_text(slide, col_left_x, content_y, col_left_w, content_h,
                     margins=(0,0,0.2,0))

    def label_block(label, body, *, first=False):
        p = para(tf, first=first, space_before=0 if first else 6, space_after=2,
                 line_spacing=1.15)
        run(p, label, size=8.5, bold=True,
            color=ca.color("primary"), font=ca.font_primary)
        p2 = para(tf, space_before=0, space_after=0, line_spacing=1.3)
        run(p2, body, size=10, color=ca.color("text"), font=ca.font_primary)

    label_block("AUDIENCE",        audience, first=True)
    label_block("TAILLE / PORTÉE", taille)
    label_block("FORMAT",          format)
    label_block("INFOS",           infos)
    if speakers:
        label_block("SPEAKERS",    speakers)

    p = para(tf, space_before=8, space_after=3, line_spacing=1.15)
    run(p, "INTÉRÊTS STRATÉGIQUES", size=8.5, bold=True,
        color=ca.color("primary"), font=ca.font_primary)
    for item in interets:
        p = para(tf, space_before=0, space_after=1, line_spacing=1.25)
        run(p, "▸  ", size=10, color=ca.color("signature"), bold=True,
            font=ca.font_primary)
        run(p, item, size=10, color=ca.color("text"), font=ca.font_primary)

    # -- right column : recommandations panel --
    add_rect(slide, col_right_x, content_y, col_right_w, content_h,
             fill=ca.color("panel-mint"))
    add_rect(slide, col_right_x, content_y, 0.18, content_h,
             fill=ca.color("signature"))

    _, tf = add_text(slide, col_right_x + 0.5, content_y + 0.2,
                     col_right_w - 0.7, content_h - 0.3,
                     margins=(0.05, 0.1, 0.05, 0.1))

    p = para(tf, first=True, space_after=4)
    run(p, "RECOMMANDATIONS", size=9, bold=True,
        color=ca.color("primary-deep"), font=ca.font_primary)

    p = para(tf, space_before=2, space_after=2)
    run(p, "Positionnement", size=8.5, bold=True,
        color=ca.color("primary"), font=ca.font_primary)
    p = para(tf, space_before=0, space_after=6, line_spacing=1.3)
    run(p, positionnement, size=9.5, italic=True,
        color=ca.color("text"), font=ca.font_primary)

    p = para(tf, space_before=2, space_after=3)
    run(p, "Activations recommandées", size=8.5, bold=True,
        color=ca.color("primary"), font=ca.font_primary)
    for act_title, act_sub in activations:
        p = para(tf, space_before=2, space_after=0, line_spacing=1.2)
        run(p, "● ", size=9, color=ca.color("signature"), bold=True,
            font=ca.font_primary)
        run(p, act_title, size=9.5, bold=True,
            color=ca.color("text"), font=ca.font_primary)
        if act_sub:
            p = para(tf, space_before=0, space_after=2, line_spacing=1.25)
            run(p, "   → " + act_sub, size=9,
                color=ca.color("muted"), font=ca.font_primary)

    p = para(tf, space_before=8, space_after=0)
    run(p, "Site : ", size=8.5, bold=True,
        color=ca.color("muted"), font=ca.font_primary)
    run(p, site, size=8.5,
        color=ca.color("primary-deep"), font=ca.font_primary)

    # --- highlight strip (bottom) ---
    if highlight:
        h_y = SLIDE_H_CM - 1.25
        add_rect(slide, 0.9, h_y, SLIDE_W_CM - 1.8, 0.65,
                 fill=ca.color("panel-cream"))
        add_rect(slide, 0.9, h_y, 0.18, 0.65, fill=ca.color("signature"))
        _, tf = add_text(slide, 1.25, h_y, SLIDE_W_CM - 2.2, 0.65,
                         anchor="m", margins=(0.05, 0, 0.05, 0))
        p = para(tf, first=True)
        run(p, "★  ", size=10, color=ca.color("signature"), bold=True,
            font=ca.font_primary)
        run(p, highlight, size=9.5, bold=True,
            color=ca.color("primary-deep"), font=ca.font_primary)
