"""Contenu du deck — Stratégie 2027 de La Fabrique by CA.

Deck de démonstration (chiffres illustratifs) pour montrer le rendu charte
Crédit Agricole / PCDI. Le contenu décrit l'ambition d'un incubateur-
accélérateur corporate à horizon 2027.
"""
from __future__ import annotations

# ── Couverture ───────────────────────────────────────────────────────────
COVER = dict(
    brand_label="LA FABRIQUE BY CA",
    eyebrow="PLAN STRATÉGIQUE · 2025 — 2027",
    photo_caption="« Faire émerger les champions de la finance et de l'assurance de demain. »",
    title_lines=["Stratégie 2027", "Bâtir le studio", "d'innovation du Groupe"],
    subtitle_lines=["L'incubateur-accélérateur du Crédit Agricole",
                    "passe à l'échelle."],
    accroche=["De l'accompagnement de startups à la",
              "fabrique de relais de croissance Groupe."],
    signoff="Comité stratégique · Juin 2026",
)

# ── Vision / ouverture ───────────────────────────────────────────────────
QUOTE_VISION = dict(
    text="Une grande banque ne se réinvente pas seule. "
         "Elle s'entoure de ceux qui la bousculent.",
    author="Vision La Fabrique",
    role="Programme 2025 — 2027",
)

# ── PARTIE 1 — Bilan ───────────────────────────────────────────────────────
SEC_BILAN = dict(
    tag="PARTIE 1 — BILAN",
    title="NOTRE POINT DE DÉPART",
    subtitle="Cinq ans d'accompagnement, un actif rare au sein du Groupe.",
)

KPI_BILAN = dict(
    title="La Fabrique en chiffres",
    subtitle="Depuis le lancement du programme",
    items=[
        {"value": "120+", "label": "startups\naccompagnées"},
        {"value": "38",   "label": "POC menés avec\nles métiers CA"},
        {"value": "€210M","label": "levés par\nles alumni"},
        {"value": "14",   "label": "entités du\nGroupe partenaires"},
        {"value": "72%",  "label": "de startups\nencore actives"},
    ],
    footnote="Chiffres illustratifs — deck de démonstration.",
    section_tag="BILAN",
)

CHART_CROISSANCE = dict(
    title="Une cadence d'accompagnement qui s'accélère",
    subtitle="Startups entrées en programme, par promotion annuelle",
    categories=["2021", "2022", "2023", "2024", "2025"],
    series=[("Startups accompagnées", [12, 18, 24, 31, 38])],
    kind="bar",
    section_tag="BILAN",
)

LOGO_ECOSYSTEME = dict(
    title="Un écosystème déjà dense",
    subtitle="Métiers du Groupe, fonds d'investissement et partenaires de place",
    section_tag="ÉCOSYSTÈME",
    logos=[
        "ca-cib", "ca-indosuez", "ca-assurances", "amundi", "caceis",
        "ca-transitions-energies", "demeter", "capagro", "rgreen", "turenne-groupe",
        "france-digitale", "france-fintech", "finance-innovation", "paris-and-co", "axeleo-capital",
    ],
    cols=5,
)

# ── PARTIE 2 — Ambition 2027 ───────────────────────────────────────────────
SEC_AMBITION = dict(
    tag="PARTIE 2 — AMBITION",
    title="CE QUE NOUS VOULONS DEVENIR EN 2027",
    subtitle="Passer du soutien aux startups à la production de valeur pour le Groupe.",
)

EXEC = dict(
    title="La Fabrique devient le studio d'innovation du Groupe",
    intro="Le marché ne récompense plus l'incubation pour l'incubation. La valeur "
          "naît de l'industrialisation : transformer une rencontre startup–métier "
          "en revenu, en gain de productivité ou en nouveau produit. Notre ambition "
          "2027 est de devenir le bras armé de cette transformation.",
    axes=[
        {"heading": "Ce que nous arrêtons",
         "items": [
             "L'accompagnement sans débouché métier identifié",
             "Les POC qui ne franchissent jamais le stade pilote",
             "Une mesure d'impact en nombre de startups",
         ]},
        {"heading": "Ce que nous industrialisons",
         "items": [
             "Le passage POC → déploiement à l'échelle",
             "La prise de participation sur les pépites stratégiques",
             "Une mesure d'impact en valeur créée pour le Groupe",
         ]},
    ],
    section_tag="THÈSE 2027",
)

THESE = dict(
    title="DEUX CONVICTIONS POUR 2027",
    subtitle="L'innovation utile se mesure à son adoption par les métiers.",
    left={"heading": "Proximité métier",
          "items": [
              "Un sponsor métier engagé pour chaque cohorte",
              "Des défis posés par les entités, pas par la mode",
              "Un budget de déploiement réservé dès le POC",
          ]},
    right={"heading": "Discipline d'investisseur",
           "items": [
               "Sélection resserrée : moins de startups, mieux suivies",
               "Co-investissement avec les fonds du Groupe",
               "Sortie ou industrialisation à 18 mois maximum",
           ]},
    stats=[("3 → 1", "ratio sélectivité"),
           ("18 mois", "horizon de décision"),
           ("100%", "cohortes sponsorisées métier")],
    section_tag="THÈSE 2027",
)

LEVIERS = dict(
    title="Quatre leviers d'exécution",
    subtitle="Le programme 2027 articulé en capacités",
    items=[
        {"title": "Venture Studio",
         "description": "Construire des startups from scratch sur les besoins non couverts du Groupe."},
        {"title": "Scale-up Lab",
         "description": "Industrialiser les POC à fort potentiel vers un déploiement multi-entités."},
        {"title": "Corporate Venture",
         "description": "Prendre des participations minoritaires aux côtés des fonds du Groupe."},
        {"title": "Talent & Culture",
         "description": "Diffuser les méthodes startup auprès des équipes métiers et dirigeants."},
    ],
    section_tag="LEVIERS",
)

HORIZONS = dict(
    title="Une trajectoire en trois temps",
    subtitle="Du recentrage 2025 au régime de croisière 2027",
    columns=[
        {"header": "Recentrer", "era": "2025",
         "items": ["Resserrer la sélection",
                   "Sponsor métier obligatoire",
                   "Refondre la mesure d'impact"]},
        {"header": "Industrialiser", "era": "2026",
         "items": ["Lancer le Scale-up Lab",
                   "Premier véhicule de co-investissement",
                   "3 déploiements multi-entités"]},
        {"header": "Passer à l'échelle", "era": "2027",
         "items": ["Venture Studio en régime",
                   "10 industrialisations / an",
                   "Modèle réplicable aux Caisses"],
         "highlight": True},
    ],
    section_tag="FEUILLE DE ROUTE",
)

BIGNUM_2027 = dict(
    value="€50M",
    label="de valeur créée pour le Groupe d'ici 2027",
    context="Revenus, gains de productivité et plus-values cumulés — objectif phare du plan.",
    eyebrow="L'OBJECTIF 2027",
)

# ── Clôture ─────────────────────────────────────────────────────────────────
CLOSING = dict(
    text="Nous ne cherchons plus à accompagner plus de startups. "
         "Nous cherchons à en faire des relais de croissance pour le Groupe.",
    author="La Fabrique by CA",
    role="Ouvrons le dialogue — Comité stratégique 2027",
)
