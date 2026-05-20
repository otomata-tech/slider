# slider

Moteur de production de decks PowerPoint propres (PPTX + PDF) à partir d'une **charte client** et d'une **bibliothèque de masques** (layouts) réutilisables.

Pas un framework — un atelier : tokens de marque + layouts + CLI qui sortent `deck.pptx` (+ `deck.pdf` si LibreOffice présent) à partir d'une structure de données Python.

## Démarrage (teammate, 2 min)

Pré-requis : [Claude Code](https://claude.ai/code) installé.

### Option A — Plugin Claude Code (recommandé)

```bash
claude plugin marketplace add otomata-tech/slider
claude plugin install slider@slider-dev
```

Les skills `install` et `slide-craft` sont alors disponibles dans toutes tes sessions. Pour mettre à jour : `claude plugin update slider`.

### Option B — Clone direct

```bash
git clone git@github.com:otomata-tech/slider.git
cd slider
claude
```

Les skills sont auto-détectés via `.claude/skills/`. Pour récupérer les updates : `git pull`.

### Ensuite, dans Claude

Dis *« installe slide-craft »*. Le skill `install` prend la main : il vérifie Python + `python-pptx` + `Pillow`, te propose d'installer LibreOffice (optionnel — pour l'export PDF), te demande si tu veux cloner un thème client (URL du repo) et active la CLI dans ton shell. Procédure manuelle de fallback dans [`INSTALL.md`](./INSTALL.md).

Une fois installé, tu peux dire à Claude :
- *« crée un deck de pitch en 5 slides, charte `<nom>` »*
- *« mets au propre ce pptx dans la charte `<nom>` »* (drop un fichier dans le chat)
- *« ajoute un masque XYZ »* ou *« ajoute un thème pour le client Z »*

Le skill `slide-craft` enchaîne avec les guides appropriés.

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

Les **thèmes clients** sont des repos séparés (un par marque) qu'on clone **directement dans** `chartes/<client>/`. Chaque thème contient juste `tokens.json` + `assets/`. Slider auto-détecte ce qu'il y a dans `chartes/`.

## CLI directe (sans Claude Code)

```bash
source demo/activate.sh

slide-craft list-chartes              # voit ce qu'il y a sous chartes/
slide-craft list-layouts              # 9 masques disponibles
slide-craft layout-info big_number    # kwargs d'un masque
slide-craft new mon-deck --charte=<nom>
                                      # → ./decks/mon-deck/
slide-craft build decks/mon-deck      # → out/deck.pptx (+ deck.pdf si soffice)
slide-craft build decks/mon-deck --no-pdf    # skip PDF même si soffice présent
```

Pour mettre au propre un PPTX existant : voir [`demo/guides/01-cleanup-existing.md`](./demo/guides/01-cleanup-existing.md).

## Ajouter un thème client

```bash
# 1. Fork le placeholder hors du repo slider
cp -r chartes/blank ../slider-<client>
# édite tokens.json, dépose logos/fonts dans assets/

# 2. Publie le thème dans son propre repo (privé)
cd ../slider-<client>
git init -b main && git add . && git commit -m "init: charte <client>"
gh repo create <org>/slider-<client> --private --source=. --push

# 3. Clone-le dans slider
cd ../slider
git clone git@github.com:<org>/slider-<client>.git chartes/<client>
```

Voir [`demo/guides/04-add-charte.md`](./demo/guides/04-add-charte.md).
