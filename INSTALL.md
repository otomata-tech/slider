# Installation

Slider est multi-plateforme (Linux, macOS, Windows). Trois choses à installer : **le moteur**, **un (ou plusieurs) thèmes clients**, et **les pré-requis système** (LibreOffice + Python).

L'architecture est en 3 couches indépendantes (voir [`README.md`](./README.md)) :
- **engine** : `otomata-tech/slider` (ce repo)
- **thème** : `otomata-tech/slider-<client>` (1 repo par client)
- **decks** : dans la mission (`<mission>/decks/<nom>/`)

---

## 1. Cloner le moteur

```bash
git clone git@github.com:otomata-tech/slider.git ~/dev/slider
cd ~/dev/slider
```

## 2. Cloner les thèmes clients

```bash
git clone git@github.com:otomata-tech/slider-credit-agricole.git ~/dev/slider-credit-agricole
# (et autres thèmes ultérieurement)

# Exposer les thèmes à slider — chemin vers les `chartes/`
echo 'export SLIDER_THEMES_PATH="$HOME/dev/slider-credit-agricole/chartes"' >> ~/.zshrc
# (Pour plusieurs thèmes, séparer par ':'  ex: "/path/a/chartes:/path/b/chartes")
source ~/.zshrc
```

---

## 3. Python deps

Python 3.11+ requis (3.13 / 3.14 testés).

```bash
pip install --user --break-system-packages python-pptx PyMuPDF Pillow
```

Ou via un venv si tu préfères :

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install python-pptx PyMuPDF Pillow
```

---

## 4. LibreOffice (rendu PPTX → PDF)

Le pipeline utilise LibreOffice en mode headless pour convertir le PPTX en PDF. Indispensable même si tu n'as pas l'app ouverte.

### Linux (Ubuntu/Debian)

```bash
sudo apt install libreoffice-impress libreoffice-writer
```

> **Important** : `libreoffice-core` seul ne suffit pas. Sans `-impress`, la conversion échoue silencieusement avec `Error: source file could not be loaded`.

### macOS

```bash
brew install --cask libreoffice
```

Le binaire est dans `/Applications/LibreOffice.app/Contents/MacOS/soffice`. Le module `lib/pdf_export.py` le trouve automatiquement.

### Windows

[Télécharger LibreOffice](https://www.libreoffice.org/download/) et installer. Le binaire `C:\Program Files\LibreOffice\program\soffice.exe` est détecté automatiquement.

---

## 5. Polices des chartes

Chaque thème embarque ses polices dans `<theme>/chartes/<nom>/assets/fonts/`. Pour que LibreOffice les utilise au rendu, elles doivent être installées au niveau OS.

### Linux

```bash
mkdir -p ~/.fonts/<nom>
cp ~/dev/slider-<client>/chartes/<nom>/assets/fonts/*.ttf ~/.fonts/<nom>/
fc-cache -f ~/.fonts/
```

### macOS

```bash
cp ~/dev/slider-<client>/chartes/<nom>/assets/fonts/*.ttf ~/Library/Fonts/
```

Pas de cache à reconstruire.

### Windows

Double-clic sur chaque `.ttf` → "Installer". Ou clic droit → "Installer pour tous les utilisateurs" (admin).

---

## 6. Installer le skill Claude Code + la CLI

Un seul script installe les deux (skill scoped à la mission + CLI mission-scoped) :

```bash
cd ~/dev/slider
./demo/install.sh
```

Effet :
- **Skill** → `<cwd>/.claude/skills/slide-craft` (Claude Code le détecte quand il tourne ici)
- **CLI** → `<repo>/demo/bin/slide-craft`

Pour avoir `slide-craft` dans le shell sans préfixe, soit utiliser `source demo/activate.sh` (scope session), soit symlinker manuellement :

### Linux

```bash
mkdir -p ~/.local/bin
ln -s "$PWD/demo/bin/slide-craft" ~/.local/bin/slide-craft
```

`~/.local/bin/` est dans le PATH par défaut sur la plupart des distros.

### macOS

`~/.local/bin/` n'est **pas** dans le PATH par défaut. Deux options :

**Option A — ajouter `~/.local/bin/` au PATH** (recommandé) :
```bash
mkdir -p ~/.local/bin
ln -s "$PWD/demo/bin/slide-craft" ~/.local/bin/slide-craft
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Option B — utiliser un dossier déjà dans le PATH** :
```bash
# Apple Silicon (M1/M2/M3) :
ln -s "$PWD/demo/bin/slide-craft" /opt/homebrew/bin/slide-craft

# Mac Intel :
sudo ln -s "$PWD/demo-skill/scripts/slide-craft" /usr/local/bin/slide-craft
```

### Windows

Ajouter `<repo>/demo/bin/` à `PATH` (Système → Variables d'environnement).

### Vérification

```bash
which slide-craft        # doit pointer vers le symlink
slide-craft help         # doit afficher l'aide
```

---

## 7. Test

```bash
cd <ta-mission>
source ~/dev/slider/demo/activate.sh
slide-craft list-chartes
slide-craft list-layouts
```

Si `list-chartes` montre `credit-agricole` (via SLIDER_THEMES_PATH) + `blank` (built-in), et `list-layouts` montre les 9 masques, tout est bon.

Pour un test bout-en-bout, scaffolder un mini-deck :

```bash
slide-craft new test-deck --charte=credit-agricole
# → ./decks/test-deck/
slide-craft build decks/test-deck
# → ./decks/test-deck/out/deck.pptx + deck.pdf
```

---

## Pré-requis Python explicites

| Lib | Usage |
|-----|-------|
| `python-pptx` | construction du PPTX |
| `PyMuPDF` (`fitz`) | rendu PDF → PNG (previews) |
| `Pillow` | inspection d'images (dimensions, format) |

Pas de framework lourd. Aucune dépendance sur des services externes (pas d'API, pas de cloud).

---

## Désinstaller

```bash
# Skill
rm ~/.claude/skills/slide-craft

# CLI
rm ~/.local/bin/slide-craft

# Fonts (optionnel — peut servir à d'autres apps)
rm -rf ~/.fonts/<charte>      # Linux
rm ~/Library/Fonts/<charte>*  # macOS

# LibreOffice : laisse-le, utile pour d'autres choses
```

Le projet lui-même reste où il est — tu peux le supprimer manuellement si plus utilisé.
