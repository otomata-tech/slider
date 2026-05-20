"""case_study — étude de cas client (intro + 3 features).

Visuel :
    ┌────────────────────────────────────────────────────┐
    │ ▌ header  brand · TAG · NN                          │
    │                                                     │
    │  Case study: <NAME>                  [client_logo]  │
    │  Accroche en grande typo                            │
    │  ──                                                 │
    │                                                     │
    │  <Intro paragraphe descriptif sur la mission, le    │
    │   challenge, l'approche...>                         │
    │                                                     │
    │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐│
    │  │ Feature 1    │ │ Feature 2    │ │ Feature 3    ││
    │  │ ──           │ │ ──           │ │ ──           ││
    │  │ Description  │ │ Description  │ │ Description  ││
    │  │ détaillée    │ │ détaillée    │ │ détaillée    ││
    │  └──────────────┘ └──────────────┘ └──────────────┘│
    │                                                     │
    └────────────────────────────────────────────────────┘
    Header `Case study:` en `muted`, nom en `primary-deep`. Logo client
    optionnel top-right. Features en cards `panel-mint`.

Usage :
    case_study.render(slide, charte,
        name="Finom",
        title="Financial solutions for entrepreneurs and freelancers",
        intro="Finom offers accounting, financial management, and banking "
              "functions in a single mobile-first platform. The company was "
              "looking for an innovative banking partner to provide financial "
              "solutions...",
        features=[
            {"title": "Account opening in 48h",
             "description": "Customers can open a bank account with a German "
                            "IBAN within 48 hours"},
            {"title": "Benefits and features",
             "description": "Finom's customers can enjoy benefits and features "
                            "such as 3% cashback, free physical and virtual..."},
            {"title": "Digital Banking",
             "description": "Finom is leveraging Solaris' banking license to "
                            "offer business accounts and Visa debit cards..."},
        ],
        client_logo_path="media/finom-logo.png",        # optionnel
        page_num=12,
        section_tag="CASE STUDIES")
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, add_image, fit_image, right_align, para, run,
)
from layouts._header import draw as draw_header


def render(slide, ca, *,
           name: str,
           title: str,
           intro: str,
           features: list[dict],
           page_num: int,
           client_logo_path: str | None = None,
           section_tag: str | None = None,
           brand_logo_path: str | None = None):
    if brand_logo_path is None:
        brand_logo_path = ca.default("header_logo")

    add_rect(slide, 0, 0, SLIDE_W_CM, SLIDE_H_CM, fill=ca.color("bg"))
    draw_header(slide, ca, page_num=page_num, section_tag=section_tag,
                logo_path=brand_logo_path)

    # --- eyebrow "Case study:"
    _, tf = add_text(slide, 0.9, 1.7, SLIDE_W_CM - 6.0, 0.7)
    p = para(tf, first=True)
    run(p, "CASE STUDY", size=10, bold=True,
        color=ca.color("muted"), font=ca.font_primary)

    # --- name
    _, tf = add_text(slide, 0.9, 2.3, SLIDE_W_CM - 6.0, 1.5)
    p = para(tf, first=True)
    run(p, name, size=int(ca.token_size("h1")), bold=True,
        color=ca.color("primary-deep"), font=ca.font_primary)

    # --- title (accroche)
    _, tf = add_text(slide, 0.9, 3.9, SLIDE_W_CM - 6.0, 1.0)
    p = para(tf, first=True)
    run(p, title, size=14,
        color=ca.color("text-strong"), font=ca.font_primary)

    add_rect(slide, 0.9, 5.0, 2.8, 0.08, fill=ca.color("signature"))

    # --- client logo top-right
    if client_logo_path:
        pic = add_image(slide, client_logo_path, SLIDE_W_CM - 5.5, 1.7,
                        h_cm=2.0)
        if pic is not None:
            fit_image(pic, max_w_cm=4.5, max_h_cm=2.0)
            right_align(pic, slide_right_cm=SLIDE_W_CM - 0.9)

    # --- intro paragraph
    _, tf = add_text(slide, 0.9, 5.6, SLIDE_W_CM - 1.8, 2.5)
    p = para(tf, first=True)
    run(p, intro, size=11,
        color=ca.color("text"), font=ca.font_primary)

    # --- features grid (3 cards in a row by default)
    if not features:
        return
    n = min(len(features), 4)
    margin_x = 0.9
    gutter   = 0.4
    avail_w  = SLIDE_W_CM - 2 * margin_x - gutter * (n - 1)
    card_w   = avail_w / n
    card_y   = 8.5
    card_h   = SLIDE_H_CM - card_y - 1.2

    for idx, feat in enumerate(features[:n]):
        x = margin_x + idx * (card_w + gutter)
        add_rect(slide, x, card_y, card_w, card_h, fill=ca.color("panel-mint"))
        add_rect(slide, x, card_y, card_w, 0.1, fill=ca.color("signature"))

        inner_x = x + 0.3
        inner_w = card_w - 0.6

        # title
        _, tf = add_text(slide, inner_x, card_y + 0.4, inner_w, 1.2)
        p = para(tf, first=True)
        run(p, feat["title"], size=12, bold=True,
            color=ca.color("primary-deep"), font=ca.font_primary)

        # underline
        add_rect(slide, inner_x, card_y + 1.6, 1.2, 0.06,
                 fill=ca.color("signature"))

        # description
        _, tf = add_text(slide, inner_x, card_y + 1.9, inner_w, card_h - 2.2)
        p = para(tf, first=True)
        run(p, feat.get("description", ""), size=10,
            color=ca.color("text"), font=ca.font_primary)
