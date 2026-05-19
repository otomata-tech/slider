# Installation

Slider est multi-plateforme (Linux, macOS, Windows). Le modèle d'install est **un dossier = une instance prête à l'emploi** : on clone slider, on clone le(s) thème(s) dedans, on est bon.

---

## 1. Cloner le moteur + un (ou plusieurs) thèmes

```bash
git clone git@github.com:otomata-tech/slider.git
git clone git@github.com:otomata-tech/slider-credit-agricole.git slider/chartes/credit-agricole
# (autres thèmes plus tard, même pattern : clone DANS slider/chartes/<name>/)
cd slider
```

Le `.gitignore` du moteur ignore tout `chartes/*` sauf `chartes/blank/`, donc les thèmes restent indépendants de l'historique de slider.

---

## 2. Python deps (obligatoire)

Python 3.11+ requis.

```bash
pip install --user --break-system-packages python-pptx Pillow
```

Ou via un venv :

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install python-pptx Pillow
```

---

## 3. LibreOffice (optionnel — uniquement pour l'export PDF)

Sans LibreOffice, `slide-craft build` produit le `.pptx` seul. Avec, il sort aussi le PDF. Tu peux l'ajouter plus tard sans rien changer d'autre.

### Linux (Ubuntu/Debian)

```bash
sudo apt install libreoffice-impress libreoffice-writer
```

> **Important** : `libreoffice-core` seul ne suffit pas. Sans `-impress`, la conversion échoue silencieusement.

### macOS

```bash
brew install --cask libreoffice
```

### Windows

[Télécharger LibreOffice](https://www.libreoffice.org/download/) et installer.

---

## 4. Polices des chartes (optionnel — pour un rendu fidèle)

Si tu utilises LibreOffice pour le PDF, installe les polices du thème côté OS pour qu'elles soient utilisées au rendu.

### Linux

```bash
cp chartes/credit-agricole/assets/fonts/*.ttf ~/.fonts/
fc-cache -f ~/.fonts/
```

### macOS

```bash
cp chartes/credit-agricole/assets/fonts/*.ttf ~/Library/Fonts/
```

### Windows

Double-clic sur chaque `.ttf` → "Installer".

---

## 5. Activer la CLI dans le shell

```bash
cd slider
source demo/activate.sh
```

Active `slide-craft` comme commande pour la durée de la session. Pour persister, ajoute `source ~/dev/slider/demo/activate.sh` à ton `~/.zshrc` ou `~/.bashrc`.

---

## 6. Test

```bash
slide-craft list-chartes      # doit montrer blank + credit-agricole
slide-craft list-layouts      # 9 masques disponibles
slide-craft new test-deck --charte=credit-agricole
slide-craft build decks/test-deck
# → decks/test-deck/out/deck.pptx (+ deck.pdf si LibreOffice installé)
```

---

## 7. Avec Claude Code

Le repo slider est self-contained comme projet Claude Code :

```bash
cd slider
claude
```

Le skill `slide-craft` est auto-détecté via `slider/.claude/skills/slide-craft → demo/` (symlink committé dans le repo).

---

## Pré-requis Python

| Lib | Usage |
|-----|-------|
| `python-pptx` | construction du PPTX (obligatoire) |
| `Pillow` | inspection d'images (dimensions, format) |

Pas de framework lourd. Aucune dépendance sur des services externes.

---

## Désinstaller

```bash
rm -rf slider                   # un dossier, tout est dedans
rm -rf ~/.fonts/Raleway*        # Linux — optionnel
rm ~/Library/Fonts/Raleway*     # macOS — optionnel
# LibreOffice : laisse-le, utile pour d'autres choses
```
