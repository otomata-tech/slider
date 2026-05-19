"""Assemble the team-building deck — vitrine de la bibliothèque de masques."""
from __future__ import annotations
import sys
from pathlib import Path

PROJECT = Path("/data/ark/la-fabrique-by-ca/code/slider")
sys.path.insert(0, str(PROJECT))

from lib.charte import Charte
from lib.deck import Deck
from layouts import (
    cover_split, section_divider,
    image_full, quote, portrait_grid, big_number, agenda_list, text_image,
)

import data as D

HERE = Path(__file__).resolve().parent
OUT  = HERE / "out"


def main():
    ca = Charte.load("credit-agricole")
    deck = Deck(charte=ca)

    # Shared brand assets
    siege_photo  = ca.asset("photo/ca-siege.jpg")
    ca_ina_logo  = ca.asset("logo/ca-ina-logo.png")
    ca_baseline  = ca.asset("logo/ca-logo-baseline.png")

    # 1. Cover
    deck.add(cover_split.render,
             brand_label="CRÉDIT AGRICOLE",
             photo_path=siege_photo,
             logo_path=ca_baseline,
             **D.COVER)

    # 2. Quote — ouverture narrative
    deck.add(quote.render, **D.QUOTE_INTRO)

    # 3. Agenda — programme
    deck.add(agenda_list.render, ca_logo_path=ca_ina_logo, **D.AGENDA)

    # 4. Portraits — animateurs
    deck.add(portrait_grid.render, ca_logo_path=ca_ina_logo, **D.PORTRAITS_GRID)

    # 5. Image hero — le lieu
    deck.add(image_full.render, photo_path=siege_photo, **D.IMAGE_HERO)

    # 6. KPI — chiffre marquant
    deck.add(big_number.render, **D.KPI_PARTICIPANTS)

    # 7. Atelier 1
    deck.add(text_image.render, photo_path=siege_photo, ca_logo_path=ca_ina_logo,
             **D.ATELIER_INNOVATION)

    # 8. Section divider — "Et après"
    deck.add(section_divider.render, **D.PERSPECTIVES)

    # 9. Engagements
    deck.add(text_image.render, photo_path=siege_photo, ca_logo_path=ca_ina_logo,
             **D.ENGAGEMENTS)

    # --- save + export ---
    pptx = deck.save_pptx(OUT / "deck.pptx")
    print(f"  PPTX → {pptx}  ({deck.pages} slides)")
    pdf = deck.export_pdf(pptx, OUT / "deck.pdf")
    print(f"  PDF  → {pdf}")


if __name__ == "__main__":
    main()
