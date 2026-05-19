"""Contenu du deck — Team Building Crédit Agricole 2026.

Chaque entrée correspond aux kwargs d'un layout (`slide-craft list-layouts`).
"""

COVER = dict(
    brand_label="CRÉDIT AGRICOLE",
    eyebrow="TEAM BUILDING · ÉDITION 2026",
    photo_path=None,
    photo_caption=None,
    title_lines=["Cap sur", "Annecy."],
    subtitle_lines=["Trois jours pour", "souder l'équipe."],
    accroche=["48 collaborateurs — 3 journées —",
              "1 objectif commun : se retrouver."],
    logo_path=None,
    signoff="Organisé par La Fabrique by CA · Juin 2026",
)

PROGRAMME = dict(
    tag="PROGRAMME",
    title="LE FIL ROUGE DE CES 3 JOURS",
    subtitle="Une montée en intensité : connaissance → coopération → célébration.",
)

JOUR_1 = dict(
    name="JOUR 1 · JEUDI 11 JUIN",
    title="Arrivée & briser la glace.",
    date="11 juin 2026",
    lieu="Imperial Palace, Annecy",
    audience="48 collaborateurs",
    taille="6 équipes de 8",
    format="Après-midi + soirée",
    infos="Transfert en autocar depuis Paris-Gare-de-Lyon. Check-in 14h00.",
    interets=[
        "Casser les silos entre pôles (Produit, Tech, Ops, Sales).",
        "Donner un cadre informel aux nouveaux arrivants du semestre.",
        "Poser les bases d'une intelligence collective opérationnelle.",
    ],
    positionnement="« Apprendre à se connaître avant d'apprendre à travailler ensemble. »",
    activations=[
        ("15h — Atelier 'Speed-meet'",
         "Pairing tournant de 5 min, mélange volontaire des équipes."),
        ("17h — Marche commentée au bord du lac",
         "Mini-groupes de 4, thématiques tirées au sort."),
        ("20h — Dîner d'ouverture",
         "Plan de table conçu pour maximiser les rencontres inter-équipes."),
    ],
    site="lafabrique.ca / teambuilding-2026",
    section_tag="PROGRAMME",
    highlight="Objectif fin J1 : chacun a échangé au moins 5 min avec 20 collègues.",
)

JOUR_2 = dict(
    name="JOUR 2 · VENDREDI 12 JUIN",
    title="Construire ensemble.",
    date="12 juin 2026",
    lieu="Plateau du Semnoz",
    audience="6 équipes mixtes",
    taille="8 personnes / équipe",
    format="Journée pleine outdoor",
    infos="Transfert minibus 8h30. Météo plan B : salle de séminaire Imperial.",
    interets=[
        "Mettre en situation de coopération sous contrainte.",
        "Faire émerger des leaderships informels au-delà des hiérarchies.",
        "Produire un livrable d'équipe — concret, présenté en plénière.",
    ],
    positionnement="« On ne fait pas équipe en parlant d'équipe — on la fait en faisant. »",
    activations=[
        ("10h — Course d'orientation collaborative",
         "Balises à valider à 8, scoring d'équipe."),
        ("14h — Atelier 'Design ton projet'",
         "Pitcher une initiative interne en 4 h, format 'shark tank' bienveillant."),
        ("18h — Restitution publique",
         "5 min par équipe, vote des pairs + jury Comex."),
    ],
    site="lafabrique.ca / teambuilding-2026",
    section_tag="PROGRAMME",
    highlight="Livrable J2 : 6 pitchs vidéo archivés sur l'intranet, l'un sera retenu pour Q3.",
)

JOUR_3 = dict(
    name="JOUR 3 · SAMEDI 13 JUIN",
    title="Célébrer & embarquer.",
    date="13 juin 2026",
    lieu="Imperial Palace + retour Paris",
    audience="48 collaborateurs + direction",
    taille="Plénière",
    format="Matinée + transfert",
    infos="Check-out 11h. Train retour 14h42 — arrivée Paris 18h30.",
    interets=[
        "Sceller les engagements pris la veille — en public, avec sponsor Comex.",
        "Recueillir un feedback à chaud, qualitatif et quantitatif.",
        "Sortir avec une énergie pour les 6 prochains mois.",
    ],
    positionnement="« On ne repart pas avec des souvenirs — on repart avec des chantiers. »",
    activations=[
        ("9h — Cercle de clôture",
         "Tour de table : un mot, un engagement, un remerciement."),
        ("10h30 — Annonce des sponsors Comex",
         "Chaque projet retenu reçoit un parrain et un budget d'amorçage."),
        ("11h30 — Photo collective + cadeau souvenir",
         "Livre photo personnalisé envoyé sous 15 jours."),
    ],
    site="lafabrique.ca / teambuilding-2026",
    section_tag="PROGRAMME",
    highlight="NPS cible post-événement : > 70 (mesuré à J+7 et J+90).",
)
