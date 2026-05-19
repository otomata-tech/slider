"""Build the Crédit Agricole 'Événements stratégiques' deck.

This file is just an assembly script: it composes existing layouts (from
`layouts/`) with data (from `data.py`) under the CA charte.
"""
from __future__ import annotations

import os, sys
from pathlib import Path

# project root on path (so `lib`, `layouts` are importable)
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from lib.charte import Charte
from lib.deck import Deck
from layouts import cover_split, section_divider, event_fiche

from data import EVENTS

HERE = Path(__file__).resolve().parent
OUT  = HERE / "out"
ASSETS_LOGOS = HERE / "assets" / "event-logos"

SECTION_LABEL = {
    "fr":         ("FRANCE",    "LES ÉVÉNEMENTS MAJEURS EN FRANCE",
                   "Leviers de notoriété & business — innovation, entrepreneuriat et grand public."),
    "eu":         ("EUROPE",    "LES ÉVÉNEMENTS EUROPÉENS MAJEURS",
                   "Leviers de notoriété & business — dimension internationale."),
    "influence":  ("INFLUENCE", "LES ÉVÉNEMENTS « INFLUENCE »",
                   "Leviers d'influence — affaires publiques, clusters et cercles fermés."),
}


def event_logo_path(slug: str | None) -> str | None:
    if not slug:
        return None
    for ext in ("png", "jpg", "jpeg", "svg"):
        p = ASSETS_LOGOS / f"{slug}.{ext}"
        if p.exists():
            return str(p)
    return None


def main():
    ca = Charte.load("credit-agricole")
    deck = Deck(charte=ca)

    # --- cover ---
    deck.add(cover_split.render,
             brand_label="CRÉDIT AGRICOLE",
             eyebrow="BENCHMARK · 2026 — 2027",
             photo_path=ca.asset("photo/ca-siege.jpg"),
             photo_caption="« Agir chaque jour dans votre intérêt et celui de la société. »",
             title_lines=["Événements", "stratégiques."],
             subtitle_lines=["Capter l'attention", "des décideurs."],
             accroche=["26 rendez-vous incontournables —",
                       "France · Europe · Cercles d'influence."],
             logo_path=ca.asset("logo/ca-logo-baseline.png"),
             signoff="Présenté par La Fabrique by CA · 2026")

    # --- sections + events ---
    current = None
    for ev in EVENTS:
        if ev["section"] != current:
            current = ev["section"]
            tag, title, subtitle = SECTION_LABEL[current]
            deck.add(section_divider.render,
                     tag=tag, title=title, subtitle=subtitle)

        tag, _, _ = SECTION_LABEL[ev["section"]]
        deck.add(event_fiche.render,
                 name=ev["name"], title=ev["title"],
                 date=ev["date"], lieu=ev["lieu"],
                 audience=ev["audience"], taille=ev["taille"],
                 format=ev["format"], infos=ev["infos"],
                 speakers=ev.get("speakers"),
                 interets=ev["interets"],
                 positionnement=ev["positionnement"],
                 activations=ev["activations"],
                 site=ev["site"],
                 section_tag=tag,
                 logo_path=event_logo_path(ev.get("slug")),
                 ca_logo_path=ca.asset("logo/ca-ina-logo.png"),
                 highlight=ev.get("highlight"))

    # --- save + export ---
    pptx_path = deck.save_pptx(OUT / "deck.pptx")
    print(f"  PPTX → {pptx_path}  ({deck.pages} slides)")

    pdf_path = deck.export_pdf(pptx_path, OUT / "deck.pdf")
    print(f"  PDF  → {pdf_path}")


if __name__ == "__main__":
    main()
