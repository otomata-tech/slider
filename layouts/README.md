# Bibliothèque de masques (layouts)

Catalogue des slides disponibles pour assembler un deck via `lib.deck.Deck`. Chaque masque = un module Python avec une fonction `render(slide, charte, **kwargs)`.

## Comment utiliser un masque

```python
from lib.charte import Charte
from lib.deck import Deck
from layouts import cover_split, section_divider, event_fiche

deck = Deck(Charte.load("credit-agricole"))
deck.add(cover_split.render, brand_label="...", title_lines=[...], ...)
deck.add(section_divider.render, tag="FRANCE", title="...", subtitle="...")
deck.add(event_fiche.render, name="...", title="...", ...)
deck.save_pptx("out/deck.pptx")
deck.export_pdf("out/deck.pptx", "out/deck.pdf")
```

`page_num` est auto-injecté par `Deck.add()`. Les autres arguments sont décrits dans le docstring de chaque module.

---

## Masques disponibles

### `cover_split` — couverture deux colonnes

![cover_split](./previews/cover_split.png)

**Usage** : page de garde. Image + brand à gauche, titre + accroche à droite.

**Signature** :
```python
cover_split.render(slide, charte, *,
    brand_label: str,                   # ex: "CRÉDIT AGRICOLE"
    eyebrow: str,                       # ex: "BENCHMARK · 2026 — 2027"
    photo_path: str | None,             # photo carrée gauche (peut être None)
    photo_caption: str | None,          # citation italique sous la photo
    title_lines: list[str],             # titre principal (1-3 lignes)
    subtitle_lines: list[str],          # sous-titre vert pomme (1-2 lignes)
    accroche: list[str],                # 1-2 lignes d'accroche
    logo_path: str | None,              # logo client bas-droit
    signoff: str)                       # mention bas-droite
```

---

### `section_divider` — séparateur de section pleine page

![section_divider](./previews/section_divider.png)

**Usage** : introduire une partie. Fond sarcelle foncé, eyebrow + titre + sous-titre, n° de page.

**Signature** :
```python
section_divider.render(slide, charte, *,
    tag: str,                           # ex: "FRANCE"
    title: str,                         # ex: "LES ÉVÉNEMENTS MAJEURS EN FRANCE"
    subtitle: str,
    page_num: int)                      # auto-injecté par Deck.add
```

---

### `event_fiche` — fiche événement détaillée

![event_fiche](./previews/event_fiche.png)

**Usage** : un événement / un partenaire / une opportunité. Header + bloc titre (avec logo event optionnel), date/lieu, deux colonnes (faits | recommandations), highlight bas.

**Signature** :
```python
event_fiche.render(slide, charte, *,
    name: str,                          # surtitre "CHANGENOW"
    title: str,                         # accroche grande typo
    date: str, lieu: str,
    audience: str, taille: str, format: str, infos: str,
    interets: list[str],                # 3-6 bullets
    positionnement: str,                # italique
    activations: list[tuple[str, str|None]],  # [(titre, sub), …]
    site: str,
    page_num: int,                      # auto-injecté
    section_tag: str | None = None,     # "FRANCE" | "EUROPE" | "INFLUENCE"
    speakers: str | None = None,
    highlight: str | None = None,       # bandeau étoilé bas
    logo_path: str | None = None,       # logo event top-right
    ca_logo_path: str | None = None)    # logo CA dans le header
```

---

## Créer un nouveau masque

1. Créer `layouts/mon_masque.py` avec une fonction `render(slide, ca, *, ...)`.
2. Docstring obligatoire : ASCII art du visuel + signature complète + cas d'usage.
3. N'utiliser que :
   - `lib.pptx_helpers` pour les primitives (set_fill, add_text, add_image, …)
   - `ca.color("...")`, `ca.font_primary`, `ca.token_size("...")` pour la charte
   - Jamais de couleur/font hardcodée
4. Si le masque a besoin du header standard, importer `layouts._header.draw`.
5. Ajouter un preview PNG dans `previews/<slug>.png` (export depuis le deck CA si pertinent).
6. Documenter ici (titre + image + signature + usage).

## Conventions

- Tous les sizes en cm dans les helpers (`add_text(slide, x, y, w, h)`).
- Slide standard 16:9 widescreen : `33.867 × 19.05 cm` (constantes `SLIDE_W_CM`, `SLIDE_H_CM`).
- Marges page standard : 0.9 cm.
- Une fonction `render` ne dépend que de `slide`, `ca` (`Charte`), et de ses kwargs. Pas d'état global.
