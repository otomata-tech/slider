# Ajouter un nouveau masque (layout)

> **CLI** : `slide-craft <cmd>` ci-dessous = `"$SC" <cmd>` avec `SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"` (à redéfinir dans chaque appel Bash — cf. SKILL.md « Invocation du CLI »). Le binaire s'auto-localise, pas d'`activate.sh`.

Quand aucun layout existant ne couvre un type de slide qu'on veut produire (timeline, comparaison 3-cols, citation centrée, KPI grand format, etc.), on crée un nouveau masque.

## Étapes

### 1. Choisir un nom

Style `snake_case`, descriptif :
- `quote` (citation centrée)
- `big_number` (KPI / chiffre central)
- `two_columns` (texte libre 2 cols)
- `timeline_horizontal`
- `compare_three`

Vérifier qu'il n'existe pas déjà : `slide-craft list-layouts`.

### 2. Croquer le visuel

Dans la docstring du module, ASCII art simple :

```
┌────────────────────────────────────────────────┐
│                                                │
│           « citation principale en             │
│            grand, italique, centrée »          │
│                                                │
│                — auteur, fonction              │
│                                                │
└────────────────────────────────────────────────┘
fond cream, signature accent en filet
```

### 3. Implémenter `render(slide, ca, *, ...)`

Fichier `layouts/<nom>.py`. Squelette :

```python
"""<nom> — <résumé d'une phrase>.

<ASCII art>

Usage :
    <nom>.render(slide, charte,
        param1=...,
        param2=...)
"""
from __future__ import annotations

from lib.pptx_helpers import (
    SLIDE_W_CM, SLIDE_H_CM,
    add_rect, add_text, add_image, para, run,
)


def render(slide, ca, *,
           param1: str,
           param2: str,
           page_num: int):
    """Render <nom> slide. See module docstring."""
    add_rect(slide, 0, 0, SLIDE_W_CM, SLIDE_H_CM, fill=ca.color("bg"))
    # ... composition
```

**Règles strictes** :
- Toutes les couleurs via `ca.color("<key>")` — jamais de `RGBColor(...)` hardcodé.
- Toutes les fonts via `ca.font_primary` (ou `ca.font_condensed` si besoin).
- Tailles depuis `ca.token_size("h1")` quand pertinent.
- Header standard si récurrent : `from layouts._header import draw; draw(slide, ca, page_num=...)`.
- Pas d'état global, pas de side effects en dehors du `slide` reçu.

### 4. Tester

Mini-deck d'essai :

```python
from lib.charte import Charte
from lib.deck import Deck
from layouts import <nom>

ca = Charte.load("blank")
deck = Deck(ca)
deck.add(<nom>.render, param1="test", param2="test", page_num=1)
deck.save_pptx("/tmp/test.pptx")
deck.export_pdf("/tmp/test.pptx", "/tmp/test.pdf")
```

### 5. Ajouter un preview au catalogue

```python
import fitz
doc = fitz.open("/tmp/test.pdf")
doc[0].get_pixmap(dpi=120).save("layouts/previews/<nom>.png")
```

### 6. Documenter dans `layouts/README.md`

Ajouter une section avec image, signature, usage.

### 7. Tester avec un vrai deck

Ajouter une slide de ce nouveau type au deck `ca-events-strategiques` (ou un autre) pour valider l'intégration.

## Conventions de signature

- `slide` et `ca` (charte) en positionnels — toujours les deux premiers.
- Tout le reste en kwargs (`*,` après).
- `page_num` est auto-injecté par `Deck.add` si le layout le déclare.
- Pas de défaut sur les paramètres essentiels (titres, contenus). Optionnels uniquement pour les ornements.
- Une `render` ne dépasse pas ~200 lignes. Sinon, c'est sans doute deux masques différents.
