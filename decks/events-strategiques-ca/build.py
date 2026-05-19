"""Assemble the Events Stratégiques deck."""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
sys.path.insert(0, str(PROJECT))
sys.path.insert(0, str(HERE))

from lib.charte import Charte
from lib.deck import Deck
from layouts import cover_split, section_divider, event_fiche

from data import COVER, DIVIDERS, SECTIONS

OUT = HERE / "out"
LOGOS = HERE / "assets" / "event-logos"


def _logo(slug: str) -> str | None:
    path = LOGOS / f"{slug}.png"
    return str(path) if path.exists() else None


def main():
    ca = Charte.load("credit-agricole")
    deck = Deck(charte=ca)

    # Cover + dividers + 25 event fiches. Brand assets (cover photo, cover
    # baseline logo, header logo) are auto-injected by the layouts from the
    # charte's `defaults` section. We only pass per-event logos explicitly.
    deck.add(cover_split.render, **COVER)

    for section_key, fiches in SECTIONS:
        deck.add(section_divider.render, **DIVIDERS[section_key])
        section_tag = DIVIDERS[section_key]["tag"]
        for fiche in fiches:
            slug = fiche["slug"]
            kwargs = {k: v for k, v in fiche.items() if k != "slug"}
            deck.add(
                event_fiche.render,
                section_tag=section_tag,
                logo_path=_logo(slug),
                **kwargs,
            )

    pptx = deck.save_pptx(OUT / "deck.pptx")
    print(f"PPTX → {pptx}  ({deck.pages} slides)")

    pdf = deck.export_pdf(pptx, OUT / "deck.pdf")
    print(f"PDF  → {pdf}")


if __name__ == "__main__":
    main()
