"""agenda_list — programme vertical avec créneaux horaires.

Visuel :
    ┌────────────────────────────────────────────────────┐
    │ ▌ header  brand · TAG · NN                          │
    │                                                    │
    │ TITRE PROGRAMME                                    │
    │ ──                                                 │
    │ accroche / lieu / date                             │
    │                                                    │
    │  09:00  ──  Accueil café                           │
    │              animation libre, présentation         │
    │                                                    │
    │  09:30  ──  Plénière d'ouverture                   │
    │              avec Sarah Doe                        │
    │                                                    │
    │  10:30  ──  Atelier 1 — innovation                 │
    │              ...                                   │
    └────────────────────────────────────────────────────┘
    Colonne horaire à gauche (couleur `primary`), liste verticale d'activités.

Usage :
    agenda_list.render(slide, charte,
        title="Programme de la journée",
        subtitle="<date> — <lieu>",
        items=[
            {"time": "09:00", "title": "Accueil café",
             "detail": "animation libre, présentation"},
            {"time": "09:30", "title": "Plénière d'ouverture",
             "detail": "avec Sarah Doe"},
            ...
        ],
        page_num=8,
        section_tag=None,
        brand_logo_path=ca.asset(...))
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text,
    para, run,
)
from layouts._header import draw as draw_header


def render(slide, ca, *,
           title: str,
           items: list[dict],
           page_num: int,
           subtitle: str | None = None,
           section_tag: str | None = None,
           brand_text: str | None = None,
           brand_logo_path: str | None = None):
    """Render an agenda / timeline slide.

    `brand_logo_path` falls back to ``charte.default("header_logo")`` when None.
    """
    if brand_logo_path is None:
        brand_logo_path = ca.default("header_logo")

    add_rect(slide, 0, 0, SLIDE_W_CM, SLIDE_H_CM, fill=ca.color("bg"))
    header_kwargs = {} if brand_text is None else {"brand_text": brand_text}
    draw_header(slide, ca, page_num=page_num, section_tag=section_tag,
                logo_path=brand_logo_path, **header_kwargs)

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
        list_y = 5.0
    else:
        list_y = 4.2

    # Vertical rail (left, `primary` thin line)
    rail_x = 4.5
    rail_top = list_y
    rail_bottom = SLIDE_H_CM - 1.5
    add_rect(slide, rail_x, rail_top, 0.04, rail_bottom - rail_top,
             fill=ca.color("primary"))

    # Each item: time on left, dot on rail, title+detail on right
    n = len(items)
    avail = rail_bottom - rail_top
    row_h = avail / max(n, 1)

    for i, item in enumerate(items):
        y = rail_top + i * row_h + 0.2

        # Time (left of rail)
        _, tf = add_text(slide, 0.9, y - 0.1, rail_x - 1.0, 0.8,
                         anchor="t", margins=(0, 0, 0, 0))
        p = para(tf, first=True, align="right", line_spacing=1.0)
        run(p, item.get("time", ""), size=14, bold=True,
            color=ca.color("primary-deep"), font=ca.font_primary)

        # Dot on the rail (small filled square, centered on rail)
        add_rect(slide, rail_x - 0.15, y + 0.1, 0.34, 0.34,
                 fill=ca.color("signature"))

        # Title + detail (right of rail)
        text_x = rail_x + 0.9
        text_w = SLIDE_W_CM - text_x - 0.9
        _, tf = add_text(slide, text_x, y - 0.1, text_w, row_h,
                         margins=(0, 0, 0, 0))
        p = para(tf, first=True, line_spacing=1.2, space_after=2)
        run(p, item.get("title", ""), size=13, bold=True,
            color=ca.color("text-strong"), font=ca.font_primary)
        if item.get("detail"):
            p = para(tf, line_spacing=1.3)
            run(p, item["detail"], size=10,
                color=ca.color("muted"), font=ca.font_primary)
