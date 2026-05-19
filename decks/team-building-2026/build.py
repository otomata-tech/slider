"""Assemble le deck Team Building 2026 (5 slides)."""
from __future__ import annotations
import sys
from pathlib import Path

PROJECT = Path("/data/ark/la-fabrique-by-ca/code/slider")
sys.path.insert(0, str(PROJECT))

from lib.charte import Charte
from lib.deck import Deck
from layouts import cover_split, section_divider, event_fiche

from data import COVER, PROGRAMME, JOUR_1, JOUR_2, JOUR_3

HERE = Path(__file__).resolve().parent
OUT  = HERE / "out"


def main():
    ca = Charte.load("credit-agricole")
    deck = Deck(charte=ca)

    # 1 — couverture
    cover_kwargs = {**COVER,
                    "photo_path":    ca.asset("photo/ca-siege.jpg"),
                    "photo_caption": "« Un esprit collectif au service de chacun. »",
                    "logo_path":     ca.asset("logo/ca-logo-baseline.png")}
    deck.add(cover_split.render, **cover_kwargs)

    # 2 — section divider : programme
    deck.add(section_divider.render, **PROGRAMME)

    # 3-4-5 — fiches jour
    for jour in (JOUR_1, JOUR_2, JOUR_3):
        deck.add(event_fiche.render,
                 ca_logo_path=ca.asset("logo/ca-ina-logo.png"),
                 **jour)

    pptx = deck.save_pptx(OUT / "deck.pptx")
    print(f"PPTX → {pptx}  ({deck.pages} slides)")

    pdf = deck.export_pdf(pptx, OUT / "deck.pdf")
    print(f"PDF  → {pdf}")


if __name__ == "__main__":
    main()
