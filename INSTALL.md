# Installation

Slide-craft est multi-plateforme (Linux, macOS, Windows). Trois choses à installer : **Python deps**, **LibreOffice**, et le **symlink du skill**.

---

## 1. Cloner le projet

```bash
git clone <repo-url> ~/dev/slide-craft   # ou autre chemin de ton choix
cd ~/dev/slide-craft
```

---

## 2. Python deps

Python 3.11+ requis (3.13 testé).

```bash
pip install --user python-pptx PyMuPDF Pillow
```

Ou via un venv si tu préfères :

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install python-pptx PyMuPDF Pillow
```

---

## 3. LibreOffice (rendu PPTX → PDF)

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

## 4. Polices des chartes

Les chartes embarquent leurs polices dans `chartes/<nom>/assets/fonts/`. Pour que LibreOffice les utilise au rendu, elles doivent être installées au niveau OS.

### Linux

```bash
mkdir -p ~/.fonts/<charte>
cp chartes/<charte>/assets/fonts/*.ttf ~/.fonts/<charte>/
fc-cache -f ~/.fonts/
```

### macOS

```bash
cp chartes/<charte>/assets/fonts/*.ttf ~/Library/Fonts/
```

Pas de cache à reconstruire.

### Windows

Double-clic sur chaque `.ttf` → "Installer". Ou clic droit → "Installer pour tous les utilisateurs" (admin).

---

## 5. Installer le skill pour Claude Code

```bash
# Linux + macOS
ln -s "$PWD/demo-skill" ~/.claude/skills/slide-craft

# Windows (PowerShell admin)
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\slide-craft" -Target "$PWD\demo-skill"
```

Claude Code détecte le skill au prochain démarrage de session. Vérifie avec `/help` ou en lançant une session — `slide-craft` doit apparaître dans la liste.

---

## 6. CLI accessible depuis le terminal

L'étape 5 installe le skill **pour Claude Code**. Pour pouvoir taper `slide-craft` **toi-même au terminal**, il faut un deuxième lien dans un dossier qui est dans ton `$PATH`.

### Linux

```bash
mkdir -p ~/.local/bin
ln -s "$PWD/demo-skill/scripts/slide-craft" ~/.local/bin/slide-craft
```

`~/.local/bin/` est dans le PATH par défaut sur la plupart des distros.

### macOS

`~/.local/bin/` n'est **pas** dans le PATH par défaut. Deux options :

**Option A — ajouter `~/.local/bin/` au PATH** (recommandé, plus propre) :
```bash
mkdir -p ~/.local/bin
ln -s "$PWD/demo-skill/scripts/slide-craft" ~/.local/bin/slide-craft
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Option B — utiliser un dossier déjà dans le PATH** :
```bash
# Apple Silicon (M1/M2/M3) :
ln -s "$PWD/demo-skill/scripts/slide-craft" /opt/homebrew/bin/slide-craft

# Mac Intel :
sudo ln -s "$PWD/demo-skill/scripts/slide-craft" /usr/local/bin/slide-craft
```

### Windows

Ajouter `<repo>/demo-skill/scripts/` à `PATH` (Système → Variables d'environnement).

### Vérification

```bash
which slide-craft        # doit pointer vers le symlink
slide-craft help         # doit afficher l'aide
```

---

## 7. Test

```bash
slide-craft help
slide-craft list-chartes
slide-craft list-layouts
```

Si tu vois la liste des chartes (credit-agricole) et des masques (cover_split, section_divider, event_fiche), tout est bon.

Pour un test bout-en-bout :

```bash
slide-craft build decks/ca-events-strategiques
# → decks/ca-events-strategiques/out/deck.pptx + deck.pdf
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
