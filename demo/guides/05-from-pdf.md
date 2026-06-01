# Re-créer un deck à partir d'un PDF source

> **CLI** : `slide-craft <cmd>` ci-dessous = `"$SC" <cmd>` avec `SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"` (à redéfinir dans chaque appel Bash — cf. SKILL.md « Invocation du CLI »). Le binaire s'auto-localise, pas d'`activate.sh`.

Workflow pour transformer un PDF (export PowerPoint, Keynote, deck designer…) en un deck PPTX propre dans la charte cible. Variante de [`01-cleanup-existing.md`](./01-cleanup-existing.md) adaptée au PDF.

## Pré-requis

- `PyMuPDF` (`pip install --user --break-system-packages PyMuPDF` ; module `fitz`).
- Le PDF source en local.

## Étapes

### 1. Extraire

```bash
"$SC" extract-pdf <source.pdf> <dest-dir>
```

Produit :

```
<dest-dir>/
├── source.pdf            # copie de l'original
├── pages.txt             # texte de chaque page (lecture humaine)
├── manifest.json         # structure complète : par page, text blocks + image bboxes
└── media/
    ├── page-01-img-01.png
    ├── page-01-img-02.jpeg
    └── ...
```

### 2. Inventaire mental

Ouvre `pages.txt` pour avoir une vue d'ensemble (textes, titres, ordre). Ouvre `manifest.json` pour repérer comment les images sont distribuées (combien par page, leurs bboxes).

Identifie pour chaque page :
- **Type de slide** : cover, divider, fiche événement, KPI, portrait grid, image_full, quote, agenda, text_image
- **Images-clés** : logo de marque ? photo hero ? icônes décoratives à ignorer ?
- **Hiérarchie texte** : titre / sous-titre / accroche / bullets

### 3. Choisir le mapping page → layout

Pour chaque page source, décide d'un layout cible parmi ceux dispos (`slide-craft list-layouts`). Si rien ne colle, soit tu adaptes (réorganises le contenu) soit tu ajoutes un nouveau masque (→ [`03-add-layout.md`](./03-add-layout.md)).

Pattern courant pour un deck pitch :
- p.1 (cover) → `cover_split`
- p.2-3 (intro stats) → `big_number` ou `text_image`
- p.4 (division) → `section_divider`
- p.5-N (contenu) → `text_image` / `event_fiche` / `portrait_grid`
- p.N+1 (citation) → `quote`
- p.last (call-to-action) → `image_full` ou `cover_split`

### 4. Scaffolder le deck cible

```bash
"$SC" new <nom> --charte=<charte>
```

### 5. Modéliser `data.py`

Recopie le texte de `pages.txt` dans une structure Python par slide. Référence les images extraites par chemin relatif (depuis le deck, vers `<dest-dir>/media/`).

```python
SLIDES = [
    {
        "layout":  "cover_split",
        "data": {
            "brand_label":   "ACME",
            "eyebrow":       "DECK PITCH · 2026",
            "photo_path":    "../<dest-dir>/media/page-01-img-02.jpeg",
            "title_lines":   ["Empowering you to", "offer financial", "services."],
            "subtitle_lines":["The Powerhouse of", "Banking Experience"],
            "logo_path":     "../<dest-dir>/media/page-01-img-01.png",
            "signoff":       "Présenté par Rinse Jacobs · 2024",
        },
    },
    {
        "layout":  "big_number",
        "data": {
            "value":   "€1.4B",
            "label":   "Valuation",
            "context": "700+ employés · 250+ partenaires live · 5M+ comptes",
            "eyebrow": "EN UN CHIFFRE",
        },
    },
    # ...
]
```

### 6. Composer `build.py`

```python
from lib.charte import Charte
from lib.deck   import Deck
from layouts    import cover_split, big_number, section_divider, text_image, quote
from data       import SLIDES

LAYOUT_MAP = {
    "cover_split":     cover_split.render,
    "big_number":      big_number.render,
    "section_divider": section_divider.render,
    "text_image":      text_image.render,
    "quote":           quote.render,
}

def main():
    deck = Deck(Charte.load("<charte>"))
    for slide in SLIDES:
        deck.add(LAYOUT_MAP[slide["layout"]], **slide["data"])
    deck.save_pptx("out/deck.pptx")
    deck.export_pdf("out/deck.pdf")

if __name__ == "__main__":
    main()
```

### 7. Builder + comparer

```bash
"$SC" build decks/<nom>
```

Ouvre côte-à-côte `source.pdf` (l'original) et `out/deck.pdf` (la version charte). Note les écarts visuels (image cropée, hiérarchie texte différente, ordre des bullets) et corrige `data.py` itérativement.

## Pièges et règles

- **Toutes les images extraites ne sont pas utiles**. Souvent il y a 5-10× plus d'images dans le PDF (icônes, fonds, motifs décoratifs) que ce qu'un layout propre reprend. Sélectionne — ne wire pas tout.
- **Les bboxes te disent où l'image vivait dans la slide source**, pas où la mettre dans la slide cible. Le layout choisi impose sa propre composition. La bbox est un indice (image était grande et centrée → c'est probablement une photo hero ; image petite en coin → probablement un logo de section).
- **Le texte de `pages.txt` est dans l'ordre de lecture brut** — pas forcément l'ordre visuel. Vérifie sur `manifest.json` (bboxes) si tu doutes.
- **Les pages de transition / dividers** ont souvent peu de texte mais une grande image — les router vers `section_divider` ou `image_full`.
- **Si la charte source diffère beaucoup de la cible** (police, couleurs, ratio), ne cherche pas à reproduire à l'identique. Tu transposes — le contenu reste, la forme adopte la cible.

## Output canonique

Comme pour les autres workflows : `out/deck.pptx` + `out/deck.pdf`. PPTX éditable dans PowerPoint, PDF pour livraison.
