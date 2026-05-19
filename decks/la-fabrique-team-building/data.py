"""Team-building La Fabrique by CA — contenu fictif de démonstration.

Sert d'exemple-vitrine pour montrer 6 nouveaux masques (image_full, quote,
portrait_grid, big_number, agenda_list, text_image) en action sur un deck
narratif court (~9 slides).
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
PORTRAITS = HERE / "assets" / "portraits"


COVER = dict(
    eyebrow="JOURNÉE COLLECTIVE · 2026",
    title_lines=["Team building", "Fabrique"],
    subtitle_lines=["Cohésion et", "élan partagé."],
    accroche=["140 personnes — un seul cap.",
              "26 août 2026 · Roland Garros."],
    photo_caption="« Agir chaque jour dans votre intérêt et celui de la société. »",
    signoff="Présenté par La Fabrique by CA · 2026",
)

QUOTE_INTRO = dict(
    text=("Une équipe se reconnait moins à ce qu'elle dit "
          "qu'à ce qu'elle traverse ensemble."),
    author="René Char",
    role="Poète",
)

AGENDA = dict(
    title="Programme de la journée",
    subtitle="Roland Garros — 26 août 2026",
    items=[
        {"time": "09:00", "title": "Accueil café",
         "detail": "Émargement, badges, photo de groupe."},
        {"time": "09:30", "title": "Plénière d'ouverture",
         "detail": "Sarah Bernheim — vision et ambition 2027."},
        {"time": "10:30", "title": "Atelier 1 — Innovation",
         "detail": "5 sous-groupes, restitution flash 14h."},
        {"time": "12:30", "title": "Déjeuner cocktail",
         "detail": "Roof-top — networking inter-équipes."},
        {"time": "14:00", "title": "Atelier 2 — Cohésion",
         "detail": "Activités physiques et créatives."},
        {"time": "17:00", "title": "Clôture & cocktail",
         "detail": "Synthèse et célébration."},
    ],
)

PORTRAITS_GRID = dict(
    title="L'équipe d'animation",
    subtitle="Cinq facilitateurs pour orchestrer la journée.",
    people=[
        {"photo": str(PORTRAITS / "marie-durand.png"),
         "name": "Marie Durand", "role": "Coach exécutive"},
        {"photo": str(PORTRAITS / "paul-martin.png"),
         "name": "Paul Martin", "role": "Facilitateur"},
        {"photo": str(PORTRAITS / "sarah-kone.png"),
         "name": "Sarah Koné", "role": "Animatrice"},
        {"photo": str(PORTRAITS / "louis-rey.png"),
         "name": "Louis Rey", "role": "Photographe"},
        {"photo": str(PORTRAITS / "anna-cherif.png"),
         "name": "Anna Chérif", "role": "Logistique"},
    ],
)

IMAGE_HERO = dict(
    eyebrow="LE LIEU",
    title="Roland Garros, hors saison.",
    subtitle="Un cadre iconique pour une journée hors du temps.",
)

KPI_PARTICIPANTS = dict(
    eyebrow="EN UN CHIFFRE",
    value="140+",
    label="participantes et participants",
    context="Toutes équipes Fabrique réunies — première édition à cette échelle.",
)

ATELIER_INNOVATION = dict(
    eyebrow="ATELIER 1",
    title="Innovation collective.",
    intro=("Cinq sous-groupes thématiques, un défi commun : "
           "imaginer la Fabrique de 2030."),
    bullets=[
        "Format : 90 minutes de divergence + 30 minutes de convergence",
        "Restitution en plénière, vote du jury Comex",
        "3 idées sélectionnées poursuivront en mode POC à Q4",
    ],
    photo_side="left",
)

PERSPECTIVES = dict(
    tag="ET APRÈS",
    title="Trois engagements pour faire durer.",
    subtitle="Pour transformer la journée en mouvement.",
)

ENGAGEMENTS = dict(
    eyebrow="SUITES",
    title="Trois engagements collectifs.",
    intro=("Pour que le souffle de la journée s'inscrive dans la durée, "
           "trois rendez-vous structurants à venir."),
    bullets=[
        "Rituel mensuel d'équipe « Fabrique du mois » à partir de septembre",
        "Pilote des 3 idées POC validées au Comex de novembre",
        "Bilan & 2e édition team-building en septembre 2027",
    ],
    photo_side="right",
)
