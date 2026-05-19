# slider

Moteur de production de decks PowerPoint propres (PPTX + PDF) à partir d'une **charte client** et d'une **bibliothèque de masques** (layouts) réutilisables.

Pas un framework — un atelier : tokens de marque + layouts + CLI qui sortent `deck.pptx` + `deck.pdf` à partir d'une structure de données Python.

## Architecture en 3 couches

```
┌──────────────────────────────┐
│  Engine (ce repo)            │   slider — code + masques + charte blank
│  - lib/ layouts/ demo/       │   public-ish, réutilisable client à client
│  - chartes/blank/            │
└──────────────────────────────┘
                ▲
                │ SLIDER_THEMES_PATH
                │
┌──────────────────────────────┐
│  Thèmes clients              │   slider-<client> — un repo par marque
│  chartes/<client>/           │   privé, partageable au client
│  + tokens.json + assets      │   ex: otomata-tech/slider-credit-agricole
└──────────────────────────────┘
                ▲
                │ $PWD
                │
┌──────────────────────────────┐
│  Decks (livrables)           │   dans la mission qui les produit
│  <mission>/decks/<nom>/      │   ex: <la-fabrique>/decks/mon-bench/
│  data.py + build.py + out/   │   data + assemblage + sorties
└──────────────────────────────┘
```

L'engine ne dépend de rien. Un thème ne dépend que de l'engine (sans code). Un deck dépend des deux et vit dans la mission.

## Structure du repo

```
slider/
├── lib/                  code Python importable
│   ├── pptx_helpers.py   primitives bas niveau
│   ├── charte.py         Charte.load() + résolution multi-chemin
│   ├── deck.py           Deck() + add(layout) + save + export
│   └── pdf_export.py     PPTX → soffice → PDF (avec isolation profil LO)
│
├── layouts/              bibliothèque de masques (9 actuellement)
│   ├── cover_split.py    section_divider.py    event_fiche.py
│   ├── image_full.py     quote.py              portrait_grid.py
│   └── big_number.py     agenda_list.py        text_image.py
│
├── chartes/
│   └── blank/            charte placeholder (à copier pour un nouveau client)
│
└── demo/                 SKILL + CLI
    ├── SKILL.md          manifest skill Claude Code
    ├── scripts/          CLI (slide-craft new / build / extract-pptx)
    ├── guides/           workflows pas-à-pas
    ├── install.sh        crée les symlinks (mission-scoped)
    └── activate.sh       active la CLI dans la session shell
```

## Installation

### A. Le moteur (slider)

```bash
git clone git@github.com:otomata-tech/slider.git ~/dev/slider
cd ~/dev/slider
./demo/install.sh           # symlinks dans <cwd>/.claude/skills/ + demo/bin/
```

### B. Un thème client

```bash
git clone git@github.com:otomata-tech/slider-credit-agricole.git ~/dev/slider-credit-agricole
echo 'export SLIDER_THEMES_PATH="$HOME/dev/slider-credit-agricole/chartes"' >> ~/.zshrc

# Polices à déposer pour LibreOffice
cp ~/dev/slider-credit-agricole/chartes/credit-agricole/assets/fonts/Raleway*.ttf \
   ~/Library/Fonts/                # macOS
# (Linux : ~/.fonts/ puis fc-cache -f ~/.fonts/)
```

### C. Pré-requis système

- Python 3.11+ avec `python-pptx`, `PyMuPDF`, `Pillow`
- LibreOffice :
  - macOS : `brew install --cask libreoffice`
  - Linux : `apt install libreoffice-impress libreoffice-writer`

Détails complets dans [`INSTALL.md`](./INSTALL.md).

## Workflow type

```bash
cd <ta-mission>
source ~/dev/slider/demo/activate.sh

slide-craft list-chartes              # voit les thèmes via SLIDER_THEMES_PATH
slide-craft list-layouts              # 9 masques disponibles
slide-craft new mon-deck --charte=credit-agricole
                                      # → ./decks/mon-deck/ dans cwd
slide-craft build decks/mon-deck      # → out/deck.pptx + out/deck.pdf
```

Pour mettre au propre un PPTX existant : voir [`demo/guides/01-cleanup-existing.md`](./demo/guides/01-cleanup-existing.md).

## Ajouter un nouveau client

```bash
# 1. Fork le placeholder
cp -r chartes/blank ../slider-<client>/chartes/<client>
# édite tokens.json, dépose logos/fonts dans assets/

# 2. Publie le thème dans son propre repo
cd ../slider-<client>
git init -b main && git add . && git commit -m "init: charte <client>"
gh repo create otomata-tech/slider-<client> --private --source=. --push
```

Voir [`demo/guides/04-add-charte.md`](./demo/guides/04-add-charte.md).
