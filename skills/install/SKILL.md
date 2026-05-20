---
name: install
description: "Pilote l'install de slide-craft (Python deps + LibreOffice optionnel + polices) et propose, si l'utilisateur le souhaite, de cloner un thème client à partir d'une URL de repo. Utiliser quand l'utilisateur dit 'installe slide-craft', 'setup slider', 'configure cet environnement', 'aide-moi à démarrer'."
---

# install

Pilote l'install end-to-end de slide-craft depuis le repo courant. Le moteur est déjà cloné (sinon ce skill ne serait pas chargé). Reste à mettre en place : Python deps, LibreOffice (optionnel), CLI dans le shell, et éventuellement un thème client.

## Principes

- **Aucun thème n'est codé en dur ici.** Si l'utilisateur veut un thème, il fournit l'URL d'un repo de thème (privé OK). Le clone va dans `chartes/<nom>/`.
- **Demander avant toute action qui touche le système** (install OS, copie de fonts dans `~/.fonts/` ou `~/Library/Fonts/`, modification de `~/.bashrc`/`~/.zshrc`).
- **Pas de sudo silencieux** : sur Linux, utiliser `pkexec` après confirmation explicite.
- **Détecter avant d'agir** : ne pas réinstaller ce qui est déjà là. Annoncer l'état détecté avant de proposer une action.

## Procédure

### 1. État courant

Inventorier rapidement et reporter à l'utilisateur :

```bash
python3 -c "import pptx, PIL" 2>&1 && echo "✓ python-pptx + Pillow" || echo "✗ deps Python manquantes"
which soffice >/dev/null 2>&1 && echo "✓ LibreOffice présent" || echo "✗ LibreOffice absent (PDF désactivé)"
ls chartes/ 2>/dev/null
uname -s
```

### 2. Python deps (obligatoire)

Si `python-pptx` ou `Pillow` manquent :

```bash
pip install --user --break-system-packages python-pptx Pillow
```

Proposer un venv si l'utilisateur préfère un environnement isolé.

### 3. Thème client (optionnel)

Demander :

> Veux-tu installer un thème client maintenant ? Si oui, donne-moi l'URL git du repo de thème (placeholder : un repo qui contient `tokens.json` + `assets/` à la racine).

Si **oui** :

```bash
git clone <URL> chartes/<nom>
```

Où `<nom>` se déduit du repo (ex: `git@github.com:org/slider-<client>.git` → `chartes/<client>/`). Confirmer le nom avec l'utilisateur si ambigu.

Si le thème embarque des polices (`chartes/<nom>/assets/fonts/*.ttf`), proposer de les installer côté OS (voir étape 5).

Si **non** : passer à l'étape suivante. Le thème `blank` (générique) est livré avec le moteur.

### 4. LibreOffice (optionnel — pour l'export PDF)

Sans LibreOffice, `slide-craft build` produit le `.pptx` seul. Avec, il sort aussi le PDF.

Si absent, demander si l'utilisateur veut l'installer. Si oui, selon l'OS :

| OS | Commande |
|---|---|
| Linux (Debian/Ubuntu) | `pkexec apt install libreoffice-impress libreoffice-writer` |
| macOS | `brew install --cask libreoffice` |
| Windows | rediriger vers https://www.libreoffice.org/download/ |

⚠️ Sur Linux, `libreoffice-core` seul ne suffit pas — sans `-impress`, la conversion PDF échoue silencieusement.

### 5. Polices du thème (optionnel — rendu fidèle PDF)

Uniquement pertinent si un thème a été installé ET si LibreOffice est présent. Sans ça, LibreOffice substitue les polices au rendu PDF.

| OS | Commande |
|---|---|
| Linux | `cp chartes/<nom>/assets/fonts/*.ttf ~/.fonts/ && fc-cache -f ~/.fonts/` |
| macOS | `cp chartes/<nom>/assets/fonts/*.ttf ~/Library/Fonts/` |
| Windows | double-clic sur chaque `.ttf` → "Installer" |

### 6. Activer la CLI

```bash
source demo/activate.sh
```

Active `slide-craft` pour la session courante (PATH + `SLIDER_ROOT`). Proposer à l'utilisateur d'ajouter cette ligne à `~/.bashrc` ou `~/.zshrc` pour persister — **demander avant de modifier le shell rc**.

### 7. Sanity check

```bash
bash -c "source demo/activate.sh && slide-craft list-chartes"
```

Doit lister au moins `blank` + le thème installé (s'il y en a un).

## Résumé à donner en fin d'install

Annoncer l'état final :

- Python deps : ✓ / ✗
- LibreOffice : ✓ / ✗ (PDF activé / désactivé)
- Thème(s) : liste, ou "aucun thème client (juste `blank`)"
- CLI active : ✓

Puis donner les 3 commandes utiles pour démarrer :

```bash
slide-craft list-layouts          # voir les masques disponibles
slide-craft new mon-deck          # créer un deck (ajoute --charte=<nom> si thème installé)
slide-craft build decks/mon-deck  # produire le PPTX (+ PDF si LibreOffice)
```

Et pointer vers le skill `slide-craft` pour la suite (composition d'un deck, mise au propre d'un PPTX existant, etc.).
