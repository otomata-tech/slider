"""Assemble le deck — Stratégie 2027 de La Fabrique by CA."""
from __future__ import annotations
import os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

SLIDER = Path(
    os.environ.get("CLAUDE_PLUGIN_ROOT")
    or os.environ.get("SLIDER_ROOT")
    or "/data/ark/la-fabrique-by-ca/code/slider"
)
sys.path.insert(0, str(SLIDER))
sys.path.insert(0, str(HERE))

from lib.charte import Charte
from lib.deck import Deck
from layouts import (
    cover_split, quote, section_divider, kpi_grid, chart_block,
    logo_wall, exec_summary, thesis_two_col, services_grid,
    comparison_columns, big_number,
)

import data

OUT = HERE / "out"


def main():
    ca = Charte.load("credit-agricole")
    deck = Deck(charte=ca)

    # Résolution des logos écosystème depuis la charte
    eco = dict(data.LOGO_ECOSYSTEME)
    eco["logos"] = [ca.asset(f"portfolio/{name}.png") for name in eco["logos"]]

    # 1 — Couverture
    deck.add(cover_split.render, **data.COVER)
    # 2 — Vision
    deck.add(quote.render, **data.QUOTE_VISION)

    # PARTIE 1 — Bilan
    deck.add(section_divider.render, **data.SEC_BILAN)
    deck.add(kpi_grid.render, **data.KPI_BILAN)
    deck.add(chart_block.render, **data.CHART_CROISSANCE)
    deck.add(logo_wall.render, **eco)

    # PARTIE 2 — Ambition
    deck.add(section_divider.render, **data.SEC_AMBITION)
    deck.add(exec_summary.render, **data.EXEC)
    deck.add(thesis_two_col.render, **data.THESE)
    deck.add(services_grid.render, **data.LEVIERS)

    # Feuille de route + objectif
    deck.add(comparison_columns.render, **data.HORIZONS)
    deck.add(big_number.render, **data.BIGNUM_2027)

    # Clôture
    deck.add(quote.render, **data.CLOSING)

    pptx = deck.save_pptx(OUT / "deck.pptx")
    print(f"PPTX → {pptx}  ({deck.pages} slides)")

    pdf = deck.export_pdf(pptx, OUT / "deck.pdf")
    if pdf:
        print(f"PDF  → {pdf}")


if __name__ == "__main__":
    main()
