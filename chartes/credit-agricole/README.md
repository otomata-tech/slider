# Charte — Crédit Agricole

Tokens de marque pour le groupe Crédit Agricole. Source de vérité : [`tokens.json`](./tokens.json).

## Sources

- Couleurs extraites de `credit-agricole.com/assets/build/app-main-css.*.css` (mai 2026)
- Vert pomme `#82B600` = couleur signature historique (logo + accents)
- Sarcelle `#008991` = couleur corporate dominante actuelle
- Font : famille **Barlow** (déclinaisons Bold / Regular / Condensed) — disponible Google Fonts

## Utilisation

### HTML / CSS
```html
<link rel="stylesheet" href=".../chartes/credit-agricole/tokens.css">
```
Puis :
```css
.title { color: var(--ca-primary); font-family: var(--ca-font-primary); }
```

### Python (python-pptx)
```python
import sys; sys.path.insert(0, ".../chartes/credit-agricole")
import tokens as ca

shape.fill.fore_color.rgb = ca.PRIMARY
run.font.name = ca.FONT_PRIMARY
run.font.size = Pt(ca.SIZE_H1)
```

## Palette

| Token              | Hex      | Usage                                  |
|--------------------|----------|----------------------------------------|
| `primary`          | #008991  | Sarcelle CA — corporate dominant       |
| `primary-dark`     | #007178  | Hover, contraste                       |
| `primary-deep`     | #005860  | Fonds sombres, dividers                |
| `signature`        | #82B600  | Vert pomme — CTAs, highlights          |
| `signature-deep`   | #3D6D04  | Vert forêt — texte sur clair           |
| `accent-mint`      | #49CEAA  | Accent moderne, mise en avant          |
| `text`             | #2E3738  | Corps de texte                         |
| `muted`            | #676767  | Texte secondaire                       |
| `panel-mint`       | #E8F4EF  | Panneaux d'encart                      |

Liste complète dans [`tokens.json`](./tokens.json).

## Assets

- `assets/logo/` : logos officiels (SVG + PNG). **À fournir** — pas redistribuables.
- `assets/fonts/` : woff2 Barlow pour offline (à télécharger depuis Google Fonts).

## Variante "La Fabrique by CA"

L'incubateur CA (notre client direct) utilise la même palette + un identifiant propre. À documenter dans une charte enfant (`chartes/la-fabrique-by-ca/`) qui hérite des tokens CA + override logo / accent secondaire.

## TODO

- [ ] Ajouter logos officiels (SVG + PNG, monochrome blanc)
- [ ] Télécharger woff2 Barlow + Barlow Condensed
- [ ] Valider la palette avec un livrable client (pilote sur un deck existant)
- [ ] Documenter la variante La Fabrique by CA
