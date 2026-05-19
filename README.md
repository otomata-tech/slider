# slider

Produit des decks PowerPoint propres (PPTX + PDF) à partir d'une **charte client** et d'une **bibliothèque de masques** (layouts) réutilisables.

Pas un framework — un atelier : tokens de marque + layouts + scripts qui sortent `deck.pptx` + `deck.pdf` à partir d'une structure de données Python.

## Structure

```
slider/
├── chartes/              kits de marque (un dossier par marque)
│   └── credit-agricole/  tokens.json + .css + .py + assets (logos, fonts, photo)
│
├── layouts/              bibliothèque de masques de slides
│   ├── README.md         catalogue avec previews PNG
│   ├── cover_split.py
│   ├── section_divider.py
│   └── event_fiche.py
│
├── lib/                  code Python importable
│   ├── pptx_helpers.py   primitives bas niveau
│   ├── charte.py         Charte.load("credit-agricole")
│   ├── deck.py           Deck() + add(layout) + save + export
│   └── pdf_export.py     PPTX → soffice → PDF → PNG previews
│
├── decks/                decks concrets (data + outputs)
│   └── ca-events-strategiques/
│       ├── data.py
│       ├── build.py
│       └── out/          deck.pptx + deck.pdf
│
└── demo/                 ZONE D'INSTALL (cloisonnée)
    ├── SKILL.md          manifest skill Claude Code
    ├── scripts/          CLI (slide-craft, list-chartes, build-deck, …)
    ├── guides/           workflows pas-à-pas
    ├── install.sh        crée les symlinks (mission-scoped)
    ├── uninstall.sh
    └── activate.sh       active la CLI dans la session shell
```

## Installation cloisonnée (par défaut)

```bash
./demo/install.sh
source demo/activate.sh
slide-craft list-chartes
```

Ne touche pas à `~/.claude/skills/` ni `~/.local/bin/`. Tout est confiné à la mission :

- **Skill Claude Code** → `<mission>/.claude/skills/slide-craft` (détecté quand Claude tourne dans la mission)
- **CLI** → `demo/bin/slide-craft` (ajouté au `PATH` via `activate.sh`)

Pour installer en global (utilisable hors mission), voir [`INSTALL.md`](./INSTALL.md).

## Workflow type

```bash
slide-craft list-chartes
slide-craft list-layouts
slide-craft new mon-deck --charte=credit-agricole
# édite decks/mon-deck/data.py + build.py
slide-craft build decks/mon-deck
```

Sortie : `decks/mon-deck/out/deck.pptx` + `deck.pdf`.

Pour mettre au propre un PPTX existant : [`demo/guides/01-cleanup-existing.md`](./demo/guides/01-cleanup-existing.md).

## Pré-requis

- Python 3.11+ avec `python-pptx`, `PyMuPDF`, `Pillow`
- LibreOffice (rendu PPTX → PDF) — `libreoffice-impress` + `libreoffice-writer` (Linux) ou `brew install --cask libreoffice` (macOS)
- Polices de la charte installées système (voir `chartes/<nom>/README.md`)

Détails dans [`INSTALL.md`](./INSTALL.md).

## Decks existants

- [`decks/ca-events-strategiques`](./decks/ca-events-strategiques/) — Benchmark 29 événements stratégiques pour Crédit Agricole (mai 2026).
