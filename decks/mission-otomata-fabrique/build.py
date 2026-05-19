"""Assemble the 3-slide corporate deck — Mission Otomata × La Fabrique by CA."""
from __future__ import annotations
import sys
from pathlib import Path

PROJECT = Path("/data/ark/la-fabrique-by-ca/code/slider")
sys.path.insert(0, str(PROJECT))

from lib.charte import Charte
from lib.deck import Deck
from layouts import cover_split, big_number, agenda_list

import data as D

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"


def main():
    ca = Charte.load("credit-agricole")
    deck = Deck(charte=ca)

    # 1. Cover
    deck.add(cover_split.render,
             brand_label="LA FABRIQUE BY CA",
             **D.COVER)

    # 2. KPI — 26 entretiens
    deck.add(big_number.render, **D.KPI_ENTRETIENS)

    # 3. Approche — 3 phases
    deck.add(agenda_list.render, **D.APPROCHE)

    pptx = deck.save_pptx(OUT / "deck.pptx")
    print(f"  PPTX → {pptx}  ({deck.pages} slides)")
    pdf = deck.export_pdf(pptx, OUT / "deck.pdf")
    print(f"  PDF  → {pdf}")


if __name__ == "__main__":
    main()
