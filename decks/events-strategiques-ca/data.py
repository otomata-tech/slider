"""Content for the Events Stratégiques deck — Crédit Agricole.

Structure :
    1× cover_split        — couverture deck
    3× section_divider    — France / Europe / Influence
    25× event_fiche       — une fiche par événement

Les fiches sont décrites dans events/{france,europe,influence}.py.
"""

from events import FRANCE, EUROPE, INFLUENCE


COVER = dict(
    brand_label="CRÉDIT AGRICOLE",
    eyebrow="BENCHMARK 2026",
    photo_path=None,
    photo_caption=None,
    title_lines=[
        "Événements",
        "stratégiques",
    ],
    subtitle_lines=["Capter l’attention des décideurs"],
    accroche=[
        "25 rendez-vous prioritaires en France, en Europe et dans",
        "les cercles d’influence — notoriété, business, leadership.",
    ],
    logo_path=None,
    signoff="Préparé pour le Crédit Agricole · 2026",
)


DIVIDERS = {
    "france": dict(
        tag="FRANCE",
        title="Les événements majeurs en France",
        subtitle="Leviers de notoriété & business : innovation, entrepreneuriat et grand public.",
    ),
    "europe": dict(
        tag="EUROPE",
        title="Les événements européens majeurs",
        subtitle="Leviers d’expansion internationale : scale-up, capital-risque, écosystèmes tech globaux.",
    ),
    "influence": dict(
        tag="INFLUENCE",
        title="Les événements d’influence",
        subtitle="Affaires publiques, clusters et cercles fermés — légitimité long terme.",
    ),
}


SECTIONS = [
    ("france",    FRANCE),
    ("europe",    EUROPE),
    ("influence", INFLUENCE),
]
