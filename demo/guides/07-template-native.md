# Workflow — deck en mode template-natif

Refaire un deck **fidèle au template d'un client** en remplissant les **propres
masques** du client (pas les layouts Python génériques du kit). C'est l'inverse
du mode classique : ici le look vient du template préservé, pas d'une charte de
tokens.

> Public : un **agent** pilote tout ça. Pas de no-code, pas d'autopilote — l'agent
> lit le catalogue, **choisit les masques avec jugement**, compose, rend, regarde,
> corrige. La boucle de feedback (preview) EST le contrôle qualité.

## 0. Pré-requis : un thème ingéré

Si le client a un template PPTX (ses masques), l'ingérer une fois :

```bash
slide-craft ingest "<Template Client>.pptx" --name=<client>
```

→ crée `~/.local/share/slider/chartes/<client>/` : `template.pptx` (préservé),
`catalog.json` (masques + rôles), `tokens.json`, `assets/photo/`.
(Détails : skill `charte-extract`, mode `ingest`.)

## 1. Voir les masques disponibles — CHOISIR

```bash
slide-craft catalog <client>
```

Liste les masques groupés par `kind` (cover / section / grid-N / list-or-text /
statement / agenda / end…), avec leur **capacité** (nb de zones `content`, images)
et les **rôles** présents (title / eyebrow / subtitle). **Lis-le et choisis** quel
masque convient à chaque slide de ton contenu — c'est ton jugement, pas une règle.

Les rôles remplissables : `title`, `eyebrow`, `subtitle`, `content`
(via `cells` = une cellule par colonne/bloc · `items` = une liste dans une box ·
`number` = gros numéro), `picture` (via `photo` plein cadre · `icons` centrées),
`date`, `footer`.

## 2. Scaffolder puis composer

```bash
slide-craft new-native <deck> --theme=<client>
```

Édite le `build.py` généré : un `deck.add(<masque>, …)` par slide. Remplis **par
rôle** (jamais par idx). Exemples :

```python
deck = NativeDeck("<client>")
deck.add(deck.pick(kind="cover"), title="…", eyebrow="…", date="…")
deck.add("Title + Txt [4 columns]", title="…", subtitle="…",
         cells=[("LLM","…"), ("MCP","…"), ("Pont","…"), ("Logiciel","…")])
deck.add("Chapter A [Dark pict]", eyebrow="Partie 01", title="Contexte",
         number="01", photo=str(HERE/"assets/photo/hdphoto1.png"))
deck.add("Title + Text list", title="…", items=[("Nom","desc"), …])
deck.save(OUT/"deck.pptx"); deck.export_pdf(str(OUT/"deck.pptx"), str(OUT/"deck.pdf"))
```

Garanties de `NativeDeck.add` :
- remplit le placeholder du bon **rôle** (robuste aux variantes +IMG) ;
- **fit_text** : le texte rétrécit pour ne jamais déborder ;
- **matérialise** date/footer si le masque les a mais que python-pptx ne les clone pas ;
- **avertit** (`[NativeDeck] … champ sans cible`) si tu passes un champ que le masque
  n'a pas — pas de perte silencieuse ;
- retire les cadres image et zones de contenu **laissés vides**.

## 3. Rendre, regarder, corriger

```bash
slide-craft build   <deck>     # PPTX + PDF
slide-craft preview <deck>     # PNG par slide + planche-contact
```

**Regarde la planche-contact**, slide par slide : bon masque ? bons placeholders
remplis ? pas de débordement, pas de cadre gris, pas de zone vide ? Ajuste le
`build.py`, rebuild. C'est cette boucle qui fait la qualité.

## Choisir le masque : repères

- **cover** → `kind=cover` (titre + eyebrow ; photo si le masque en a une).
- **séparateur de partie** → `kind=section` : photo plein cadre + gros `number` + titre.
- **N points de même niveau** → `kind=grid-N` (`cells`) ; +IMG pour une icône par cellule.
- **catalogue / énumération** → `list-or-text` (`items`).
- **message fort** → `statement` (titre court + eyebrow).
- **clôture / contact** → `end`.

Si aucun masque ne colle, c'est un signal : soit reformuler le contenu, soit
l'ingest a raté un masque (vérifier `catalog`).
