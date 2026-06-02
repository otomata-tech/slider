# slider — guide projet

Atelier pour produire des decks PowerPoint propres (PPTX + PDF) à partir de données structurées et d'une charte client.

Voir [`README.md`](./README.md) pour la vue d'ensemble.

## Principes

- **Charte = source de vérité.** Toute couleur / font dans un slide doit venir de `chartes/<marque>/tokens.*` — jamais de hex hardcodé dans un layout ou un build.
- **Données séparées du rendu.** `data.py` décrit le contenu, le layout choisit la composition, la charte fixe le look.
- **Python natif, pas de DSL.** Pas de YAML / JSON config intermédiaire. Le contenu est du Python (dicts) car a) `python-pptx` impose Python, b) l'agent écrit Python aussi facilement que YAML, c) signatures typées des `render()` = contrat lisible.
- **Livrable = PPTX.** Le PPTX est le seul livrable par défaut. Le PDF (`build --pdf`) et les PNG (`preview`) ne sont produits **qu'à la demande explicite de l'utilisateur**. `export_pdf` est opt-in (`SLIDER_PDF=1`). Ne jamais faire dépendre la pipeline de LibreOffice.
- **Self-contained.** Le repo est utilisable tel quel : `cd slider && claude` détecte le skill via `.claude/skills/deck → demo/` (symlink committé). Les thèmes clients sont des repos séparés clonés DANS `chartes/<client>/`.

## Stack

- `python-pptx` — construction du PPTX
- LibreOffice (`soffice`) — PPTX → PDF (optionnel, cf. `lib/pdf_export.py` ; retry sur profil isolé si la passe rapide échoue)
- `Pillow` — inspection d'images

Aucun service externe, aucun bundler.

## Skills du plugin

Le plugin `slider` expose 4 skills (famille cohérente, un verbe chacun) :

| Skill | Rôle |
|---|---|
| `install` | setup env (deps, LibreOffice, charte au chemin stable) |
| `deck` | créer / nettoyer / recréer un deck, ajouter masque, charts, depuis doc/pdf/pptx |
| `review` | lint de conformité charte d'un `.pptx` (CLI `slide-craft review`) |
| `theme` | créer / dériver / éditer une charte — y compris **ingest** d'un template client (mode natif, cf. plus bas) |

> **Skill ≠ CLI.** Le skill principal s'appelle **`deck`** ; le binaire moteur interne (que Claude appelle, jamais l'utilisateur) reste **`slide-craft`** (`demo/bin/slide-craft <cmd>`).

Règle : **un skill = un workflow** (pilotage), pas une primitive. Les primitives (un masque, un helper, un sous-format) vivent dans `deck`, pas dans un skill séparé — c'est pourquoi `chart_block` (charts) et le guide `from-document` (mémo→deck) sont DANS `deck`, pas des skills.

Câblage : `skills/<name>/SKILL.md` (réel) + symlink `.claude/skills/<name>` (dev in-repo). `deck` est le symlink `skills/deck → ../demo`.

## Chrome & composants PCDI

Charte `credit-agricole` = **système de design PCDI Capital Innovation** (kit juin 2026). Deux briques partagées :

- **`layouts/_header.py`** — chrome de page : `draw()` (wordmark+n°, mention « Usage Interne », filet noir, pied date+logo) et `title_block()` (eyebrow + titre CAPITALES + sous-titre vert). Tout masque de contenu appelle ces deux fonctions.
- **`layouts/_components.py`** — composants réutilisables du kit : `marker_list()` (listes « + » vertes / « – » rouges, terme-clé en gras), `stat_card()` (carte mint, chiffre vert), `pill()` (pastille mint / vert plein / contour).

Primitives ajoutées à `lib/pptx_helpers.py` : `add_round_rect`, `add_oval`, `set_hanging` (indent pendante), et `set_fill` désactive l'ombre (rendu plat).

Assets de la charte CA (repo séparé `slider-credit-agricole`, cloné dans `chartes/credit-agricole/`) : `assets/logo/` = **identité CA** (ina, `la-fabrique`, `ca-capital-innovation`), `assets/portfolio/` = **47 logos sociétés** (content pour `logo_wall`, pas de l'identité), `assets/photo/`, `assets/fonts/` (Raleway).

## Bibliothèque de masques (`layouts/`)

Masques cohérents charte mais distincts. **Gabarits natifs PCDI** (kit) :

| Masque               | Identité                                                |
|----------------------|---------------------------------------------------------|
| `exec_summary`       | thèse + amorce + 2 axes en listes « + » (kit slide 16)  |
| `thesis_two_col`     | thèse 2 colonnes + rangée de stat-cards (kit slide 17)  |
| `company_zoom`       | logo + pastille reco + valo + description (kit slide 18)|
| `comparison_table`   | tableau : en-tête mint, indicateurs circulaires (s.12)  |
| `chart_block`        | graphique natif PPTX (bar/line/donut) en couleurs charte|

Masques génériques (reskinés PCDI automatiquement via `ca.color`) :

| Masque             | Identité                                                |
|--------------------|---------------------------------------------------------|
| `cover_split`      | couverture image+brand à gauche, titre à droite         |
| `section_divider`  | pleine page `primary-deep`, transition narrative        |
| `text_image`       | 50/50 photo + listes « + » (côté configurable)          |
| `event_fiche`      | fiche événement 2 cols : faits ‖ encart recos           |
| `image_full`       | photo plein cadre + titre overlay bas                   |
| `quote`            | citation centrée italique + accent                      |
| `portrait_grid`    | grille 2-5 col, photo + nom + rôle                      |
| `big_number`       | KPI géant pleine page                                   |
| `agenda_list`      | rail vertical horaire / activité / détail               |
| `kpi_grid` `logo_wall` `services_grid` `case_study` `comparison_columns` | masques pitch/B2B (v1.2.0) |

## Mode template-natif (ingest + NativeDeck)

Deuxième voie, **à privilégier quand le client a un VRAI template PPTX** : au lieu de reskiner les masques génériques (look d'un autre kit), on remplit les **propres masques du client** → fidélité maximale. Principe : *un thème n'est pas un nuancier, c'est le template préservé*.

- `slide-craft ingest <template.pptx> --name=<t>` (`lib/template.py`) → préserve `template.pptx` + `catalog.json` (layouts → placeholders avec **rôle déduit par type/position**, jamais par idx + signature + kind) + tokens dérivés du thème (clrScheme/fontScheme) + photos harvestées. Écrit dans le dossier thèmes user.
- `slide-craft catalog <t>` → digest des masques (rôles, capacité) pour CHOISIR un masque.
- `NativeDeck` (`lib/native.py`) : remplit PAR RÔLE (`title`/`eyebrow`/`subtitle`/`content` via `cells`|`items`|`number`/`picture` via `photo`|`icons`/`date`/`footer`), `fit_text` anti-débordement, matérialise date/footer non clonés par python-pptx, **avertit** si un champ n'a pas de cible (no silent fallback). `slide-craft new-native <deck> --theme=<t>` scaffolde ; `build`/`preview` réutilisent la tuyauterie standard.
- **Cible = un AGENT** : introspection (`catalog`) + API + jugement de l'agent pour choisir le masque — pas de DSL no-code ni d'autopilote heuristique. Guide [`demo/guides/07-template-native.md`](./demo/guides/07-template-native.md).
- Limite connue : la détection `subtitle` rate sur les masques à panneau gauche étroit (placeholder < 18 cm classé `content`) → sous-titre ignoré (averti). Cosmétique.

**Deux sous-modes** (détectés à l'ingest, `catalog.json#mode`) :
- `layouts` — le template a une **bibliothèque de masques** (ex. Egis, 59 layouts) → `NativeDeck` remplit les masques par rôle.
- `models` — le template **n'a pas de masques**, le design est **dessiné sur les slides** (ex. template Otomata) → `ModelDeck` (`lib/models.py`) **clone une slide-modèle + réécrit son texte par ancre** (images recopiées via rel remap, slides-sources retirées au save). `catalog` liste alors les slides-modèles + leurs ancres.

## Invocation du CLI (plugin installé vs dev)

Le CLI `slide-craft` **n'est jamais sur le `PATH`** côté skill, et `activate.sh` ne survit pas entre deux appels Bash (shells sans état). Les SKILL.md et guides appellent donc le binaire **par chemin absolu**, redéfini à chaque appel :

```bash
SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"
"$SC" list-layouts
```

- Plugin installé → `$CLAUDE_PLUGIN_ROOT` posé par Claude Code.
- Dev in-repo (`cd slider && claude`) → fallback `.` (cwd = racine du repo).

Le binaire s'auto-localise (`_common.py` dérive `PROJECT` via realpath) : aucune var d'env requise, `SLIDER_ROOT`/`activate.sh` ne sont qu'un confort pour un humain en terminal interactif. **Ne jamais écrire `slide-craft <cmd>` en cru dans un SKILL/guide** — ça suppose le PATH, qui n'existe pas quand le plugin tourne installé.

### Chartes clientes : où les cloner

Le plugin installé ne livre que `blank`. Une charte cliente se clone dans **`<workspace>/chartes/<nom>/`** (l'espace de travail de l'utilisateur, cf. ordre de recherche ci-dessous) — **jamais** dans le cache plugin (`$CLAUDE_PLUGIN_ROOT/chartes/`), qui est effacé à chaque `claude plugin update`.

## Découverte des chartes

`Charte.load(name)` cherche dans cet ordre :
1. `$PWD/chartes/` — override par deck (workspace courant)
2. `~/.local/share/slider/chartes/` (ou `$XDG_DATA_HOME/slider/chartes/`) — thèmes persistants par utilisateur, indépendants du cwd et **non effacés par `plugin update`**. **C'est ici qu'on clone les thèmes clients.**
3. `<engine>/chartes/` — built-in `blank` + thèmes clonés dans un repo de dev

`slide-craft list-chartes` itère ces chemins et dédupliqe par nom (premier-vu gagne).

## Decks

`slide-craft new mon-deck` scaffolde dans `$PWD/decks/mon-deck/`. Que ce soit lancé depuis le repo slider ou ailleurs (mission, sandbox), le cwd détermine où atterrissent les decks.

## Conventions

- **Slides 16:9 widescreen** : `339.9mm × 190.5mm` (= 33.867cm × 19.05cm = 1284.5px × 720px à 96 dpi)
- **Couleurs** : `ca.color("primary")`, `ca.color("signature")`, etc. — référence à `tokens.json`
- **Polices** : `ca.font_primary` (jamais une `font_name=` hardcodée comme `"Calibri"`)
- **Marge page** : 9mm standard
- **Assets auto-injectés** : les layouts lisent `ca.default("cover_photo")`, `ca.default("cover_logo")`, `ca.default("header_logo")` depuis `chartes/<nom>/tokens.json#defaults` si l'appelant ne les fournit pas. Un nouveau deck n'a pas à wirer les assets de marque dans son `build.py`.
- **Boucle de composition** : `layout-info <nom>` (signature exacte avant de remplir) → `lint <deck>` **avant** `build` (valide kwargs + chemins image, ne produit rien) → `build` (PPTX) → `preview`/`--pdf` seulement à la demande. Câblée dans le workflow du SKILL.md `deck`.

## Tâches courantes

### Mettre au propre un PPTX existant

Voir [`demo/guides/01-cleanup-existing.md`](./demo/guides/01-cleanup-existing.md). Résumé :
1. `slide-craft extract-pptx <source.pptx> /tmp/extracted/`
2. Identifier les masques utiles dans `slide-craft list-layouts`
3. Slugifier les assets uniques par slide (logos events, portraits) → `decks/<nom>/assets/`
4. `slide-craft new <nom>`, remplir `data.py`, composer `build.py`
5. `slide-craft build decks/<nom>`

### Composer un deck de zéro

Voir [`demo/guides/02-compose-new.md`](./demo/guides/02-compose-new.md).

### Ajouter un masque (layout)

Voir [`demo/guides/03-add-layout.md`](./demo/guides/03-add-layout.md).

### Ajouter une charte

Voir [`demo/guides/04-add-charte.md`](./demo/guides/04-add-charte.md).

### Refaire un deck dans le template d'un client (natif)

Voir [`demo/guides/07-template-native.md`](./demo/guides/07-template-native.md) : `ingest` le template → `catalog` → `new-native` → composer par rôle → `build`/`preview`.

## Layout API

Chaque masque est un module `layouts/<nom>.py` exposant :

```python
def render(slide, charte, *,
           param1: ...,
           param2: ...,
           page_num: int):
    ...
```

- `slide` et `charte` toujours positionnels en premier
- Tout le reste en kwargs après `*,`
- `page_num` auto-injecté par `Deck.add` si déclaré
- Pas de side effects en dehors du `slide` reçu

## Mémoire utilisateur (rappels)

- Pas de fichiers > 500 lignes
- Pas de fallbacks legacy — lever des erreurs propres
- Pas de markdown de compte-rendu automatique
