# slider — guide projet

Atelier pour produire des decks PowerPoint propres (PPTX + PDF) à partir de données structurées et d'une charte client.

Voir [`README.md`](./README.md) pour la vue d'ensemble.

## Principes

- **Charte = source de vérité.** Toute couleur / font dans un slide doit venir de `chartes/<marque>/tokens.*` — jamais de hex hardcodé dans un layout ou un build.
- **Données séparées du rendu.** `data.py` décrit le contenu, le layout choisit la composition, la charte fixe le look.
- **Pipeline iso PPTX → PDF.** Le PPTX est la source canonique. LibreOffice headless le convertit en PDF — c'est ce que PowerPoint affichera en l'ouvrant.
- **Skill cloisonné par défaut.** L'install via `demo/install.sh` reste dans la mission (`<mission>/.claude/skills/` + `demo/bin/`), pas dans les dossiers home globaux.
- **Engine ≠ thèmes ≠ decks.** Ce repo est le **moteur** uniquement. Les chartes clients vivent dans des repos séparés (`otomata-tech/slider-<client>`) et sont découvertes via `SLIDER_THEMES_PATH`. Les decks (livrables) vivent dans la mission, jamais ici.

## Stack

- `python-pptx` — construction du PPTX
- LibreOffice (`soffice`) — PPTX → PDF (avec retry sur profil isolé si la passe rapide échoue, cf. `lib/pdf_export.py`)
- PyMuPDF (`fitz`) — inspection / previews PDF à la demande (pas dans le pipeline de build)
- `Pillow` — inspection d'images

Aucun service externe, aucun bundler.

## Bibliothèque de masques (`layouts/`)

9 masques cohérents charte mais distincts visuellement :

| Masque             | Identité                                                |
|--------------------|---------------------------------------------------------|
| `cover_split`      | couverture image+brand à gauche, titre à droite         |
| `section_divider`  | pleine page sarcelle deep, transition narrative         |
| `event_fiche`      | fiche événement 2 cols : faits ‖ encart recos           |
| `image_full`       | photo plein cadre + titre overlay bas                   |
| `quote`            | citation centrée italique, fond crème + accent          |
| `portrait_grid`    | grille 2-5 col, photo + nom + rôle                      |
| `big_number`       | KPI géant (~180pt) sarcelle deep sur crème              |
| `agenda_list`      | rail vertical horaire / activité / détail               |
| `text_image`       | 50/50 photo + bullets (côté configurable)               |

## Découverte des chartes

`Charte.load(name)` cherche dans cet ordre :
1. Chemins dans `$SLIDER_THEMES_PATH` (séparés par `:`) — pour les thèmes clients externes (`slider-<client>` repos)
2. `$PWD/chartes/` — pour les overrides mission-locales
3. `<engine>/chartes/` — built-ins de l'engine (`blank` seulement, comme placeholder)

`slide-craft list-chartes` itère ces chemins et dédupliqe par nom (premier-vu gagne, matche la priorité de `load`).

## Decks (livrables — hors engine)

Le moteur ne contient **pas** de decks. Quand un user/Claude lance `slide-craft new mon-deck`, le scaffold va dans `$PWD/decks/mon-deck/`. Les decks existants pour cette mission sont dans `<mission>/decks/` (`<la-fabrique-by-ca>/decks/`).

## Conventions

- **Slides 16:9 widescreen** : `339.9mm × 190.5mm` (= 33.867cm × 19.05cm = 1284.5px × 720px à 96 dpi)
- **Couleurs** : `ca.color("primary")`, `ca.color("signature")`, etc. — référence à `tokens.json`
- **Polices** : `ca.font_primary` (jamais une `font_name=` hardcodée comme `"Calibri"`)
- **Marge page** : 9mm standard
- **Assets auto-injectés** : les layouts lisent `ca.default("cover_photo")`, `ca.default("cover_logo")`, `ca.default("header_logo")` depuis `chartes/<nom>/tokens.json#defaults` si l'appelant ne les fournit pas. Un nouveau deck n'a pas à wirer les assets de marque dans son `build.py`.

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
