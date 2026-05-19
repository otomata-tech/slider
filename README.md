# slider

Moteur de production de decks PowerPoint propres (PPTX + PDF) à partir d'une **charte client** et d'une **bibliothèque de masques** (layouts) réutilisables.

Pas un framework — un atelier : tokens de marque + layouts + CLI qui sortent `deck.pptx` (+ `deck.pdf` si LibreOffice présent) à partir d'une structure de données Python.

## Architecture

```
slider/                                     ← ce repo (le moteur)
├── lib/                  code importable
├── layouts/              9 masques (cover_split, event_fiche, ...)
├── chartes/
│   ├── blank/            placeholder générique (tracké)
│   └── <client>/         thèmes clients clonés ici (gitignored)
├── demo/                 SKILL Claude Code + CLI slide-craft
└── decks/                decks produits (un dossier par deck)
```

Les **thèmes clients** sont des repos séparés (`otomata-tech/slider-<client>`) qu'on clone **directement dans** `chartes/<client>/`. Chaque thème contient juste `tokens.json` + `assets/`. Slider auto-détecte ce qu'il y a dans `chartes/`.

## Installation

```bash
git clone git@github.com:otomata-tech/slider.git
git clone git@github.com:otomata-tech/slider-credit-agricole.git slider/chartes/credit-agricole
cd slider

# Python deps (obligatoire)
pip install --user python-pptx Pillow

# (Optionnel) LibreOffice pour l'export PDF
#   macOS : brew install --cask libreoffice
#   Linux : apt install libreoffice-impress libreoffice-writer

# (Optionnel) Polices du thème pour le rendu LO
cp chartes/credit-agricole/assets/fonts/Raleway*.ttf ~/Library/Fonts/   # macOS
# cp chartes/credit-agricole/assets/fonts/Raleway*.ttf ~/.fonts/         # Linux
# fc-cache -f ~/.fonts/                                                   # Linux

source demo/activate.sh
```

Détails dans [`INSTALL.md`](./INSTALL.md).

## Workflow type

```bash
cd slider
source demo/activate.sh

slide-craft list-chartes              # voit ce qu'il y a sous chartes/
slide-craft list-layouts              # 9 masques disponibles
slide-craft layout-info big_number    # kwargs d'un masque
slide-craft new mon-deck --charte=credit-agricole
                                      # → ./decks/mon-deck/
slide-craft build decks/mon-deck      # → out/deck.pptx (+ deck.pdf si soffice)
slide-craft build decks/mon-deck --no-pdf    # skip PDF même si soffice présent
```

Avec Claude Code : `cd slider && claude` — le skill `slide-craft` est auto-détecté (présent en `.claude/skills/slide-craft → demo/`).

Pour mettre au propre un PPTX existant : voir [`demo/guides/01-cleanup-existing.md`](./demo/guides/01-cleanup-existing.md).

## Ajouter un nouveau client

```bash
# 1. Fork le placeholder hors du repo slider
cp -r chartes/blank ../slider-<client>
# édite tokens.json, dépose logos/fonts dans assets/

# 2. Publie le thème dans son propre repo (privé)
cd ../slider-<client>
git init -b main && git add . && git commit -m "init: charte <client>"
gh repo create otomata-tech/slider-<client> --private --source=. --push

# 3. Clone-le dans slider
cd ../slider
git clone git@github.com:otomata-tech/slider-<client>.git chartes/<client>
```

Voir [`demo/guides/04-add-charte.md`](./demo/guides/04-add-charte.md).
