---
name: install
description: "Pilote l'install de slide-craft (Python deps + LibreOffice optionnel + polices) et propose, si l'utilisateur le souhaite, de cloner un thème client à partir d'une URL de repo. Utiliser quand l'utilisateur dit 'installe slide-craft', 'setup slider', 'configure cet environnement', 'aide-moi à démarrer'."
---

# install

Met en place l'environnement d'exécution de slide-craft. Le moteur est déjà présent (sinon ce skill ne serait pas chargé) — il vit soit dans le plugin installé (`$CLAUDE_PLUGIN_ROOT`), soit dans le repo cloné en dev. Reste à installer : les deps Python, LibreOffice (optionnel, pour le PDF), éventuellement un thème client, et à câbler le poste de travail de l'utilisateur.

## Localiser le moteur et le CLI

Le binaire n'est **pas sur le `PATH`**. Appelle-le par chemin absolu, redéfini dans **chaque** appel Bash (les shells ne partagent pas d'état) :

```bash
SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"
```

- Plugin installé → `$CLAUDE_PLUGIN_ROOT` est posé par Claude Code.
- Dev in-repo (`cd slider && claude`) → fallback `.` (cwd = racine du repo).

Le binaire s'auto-localise (realpath) ; **pas besoin de `source activate.sh`** pour que Claude l'utilise. `activate.sh` n'est qu'un confort pour un humain qui tape des commandes dans un terminal interactif persistant.

## Principes

- **Aucun thème n'est codé en dur ici.** Si l'utilisateur veut un thème, il fournit l'URL d'un repo de thème (privé OK).
- **La charte se clone dans le dossier thèmes stable de l'utilisateur, jamais dans le cache plugin.** Le moteur cherche les chartes dans cet ordre : `$PWD/chartes/` (override par deck) → `~/.local/share/slider/chartes/` (thèmes persistants par utilisateur) → `<moteur>/chartes/` (built-in `blank`). Le cache plugin (`$CLAUDE_PLUGIN_ROOT`) est **effacé à chaque `claude plugin update`** → tout thème cloné dedans serait perdu. Donc on clone dans **`~/.local/share/slider/chartes/<nom>/`** : indépendant du cwd, survit aux updates.
- **Demander avant toute action qui touche le système** (install OS, copie de fonts dans `~/.fonts/` ou `~/Library/Fonts/`, modification de `~/.bashrc`/`~/.zshrc`).
- **Pas de sudo silencieux** : sur Linux desktop, `pkexec` après confirmation explicite. En sandbox (ex: Cowork), il n'y a généralement ni sudo ni apt → ne pas tenter, voir étape 4.
- **Détecter avant d'agir** : ne pas réinstaller ce qui est déjà là. Annoncer l'état détecté avant toute action.

## Procédure

### 1. État courant

Inventorier et reporter à l'utilisateur :

```bash
SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"
python3 -c "import pptx, PIL" 2>&1 && echo "✓ python-pptx + Pillow" || echo "✗ deps Python manquantes"
python3 -c "import fitz" 2>&1 && echo "✓ PyMuPDF (extract-pdf)" || echo "✗ PyMuPDF manquant"
which soffice >/dev/null 2>&1 && echo "✓ LibreOffice présent (PDF activé)" || echo "✗ LibreOffice absent (PDF désactivé, PPTX seul)"
"$SC" list-chartes 2>/dev/null || echo "(CLI pas encore opérationnel — deps à installer)"
uname -s
```

### 2. Définir l'espace de travail

Demander où l'utilisateur veut que vivent ses decks et ses chartes. Par défaut, proposer un dossier dédié et stable (il survit aux mises à jour du plugin) :

```bash
mkdir -p ~/slides && cd ~/slides
```

C'est depuis ce dossier que les commandes `new` / `build` seront lancées (le cwd détermine où atterrissent `decks/` et où sont cherchées les `chartes/`).

### 3. Python deps (obligatoire)

Si `python-pptx`, `Pillow` ou `PyMuPDF` manquent :

```bash
pip install --user --break-system-packages python-pptx Pillow PyMuPDF
```

Proposer un venv si l'utilisateur préfère un environnement isolé. Si `pip` est absent (sandbox restreint), le signaler : sans deps Python, le moteur ne tourne pas — c'est bloquant, remonter à l'utilisateur.

### 4. Thème client (optionnel)

Demander :

> Veux-tu installer un thème client maintenant ? Si oui, donne-moi l'URL git du repo de thème (un repo qui contient `tokens.json` + `assets/` à la racine).

Si **oui** — cloner dans le dossier thèmes stable, **pas** dans le cache plugin :

```bash
mkdir -p ~/.local/share/slider/chartes
git clone <URL> ~/.local/share/slider/chartes/<nom>
```

Où `<nom>` se déduit du repo (ex: `git@github.com:org/slider-<client>.git` → `chartes/<client>/`). Confirmer si ambigu. Le thème est alors trouvé depuis n'importe quel cwd et survit aux `plugin update`. Si le repo est privé, l'utilisateur doit avoir un accès git configuré (clé SSH / token) — en sandbox Cowork, vérifier que `git` et l'auth sont disponibles, sinon proposer un dépôt des fichiers du thème par un autre canal.

Si le thème embarque des polices (`chartes/<nom>/assets/fonts/*.ttf`), proposer de les installer côté OS (étape 6).

Si **non** : le thème `blank` (générique) est livré avec le moteur, on continue avec.

### 5. LibreOffice (optionnel — export PDF)

Sans LibreOffice, `build` produit le `.pptx` seul (canonique). Avec, il sort aussi le PDF de livraison.

- **Desktop Linux/macOS** et l'utilisateur veut le PDF → proposer l'install :

  | OS | Commande |
  |---|---|
  | Linux (Debian/Ubuntu) | `pkexec apt install libreoffice-impress libreoffice-writer` |
  | macOS | `brew install --cask libreoffice` |
  | Windows | https://www.libreoffice.org/download/ |

  ⚠️ Sur Linux, `libreoffice-core` seul ne suffit pas — sans `-impress`, la conversion PDF échoue silencieusement.

- **Sandbox sans apt/sudo (ex: Cowork)** : ne pas tenter d'installer. Annoncer clairement : « PDF désactivé dans cet environnement, je livre le PPTX éditable ; ouvre-le dans PowerPoint pour exporter un PDF si besoin. » C'est un mode dégradé attendu, pas une erreur.

### 6. Polices du thème (optionnel — rendu PDF fidèle)

Pertinent uniquement si un thème a été installé ET LibreOffice présent. Sans ça, LibreOffice substitue les polices au rendu PDF.

| OS | Commande |
|---|---|
| Linux | `cp ~/.local/share/slider/chartes/<nom>/assets/fonts/*.ttf ~/.fonts/ && fc-cache -f ~/.fonts/` |
| macOS | `cp ~/.local/share/slider/chartes/<nom>/assets/fonts/*.ttf ~/Library/Fonts/` |
| Windows | double-clic sur chaque `.ttf` → "Installer" |

### 7. Sanity check

Depuis l'espace de travail :

```bash
SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"
"$SC" list-chartes
```

Doit lister au moins `blank` + le thème installé (s'il y en a un, parce qu'on est dans le dossier qui contient `chartes/<nom>/`).

## Résumé à donner en fin d'install

- Python deps : ✓ / ✗
- LibreOffice : ✓ (PDF activé) / ✗ (PPTX seul)
- Thème(s) : liste, ou "aucun thème client (juste `blank`)"
- Espace de travail : `<chemin>` (lancer `new` / `build` depuis là)

Puis les 3 commandes utiles pour démarrer (rappeler qu'il faut redéfinir `SC` à chaque appel Bash) :

```bash
SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"
"$SC" list-layouts                 # voir les masques disponibles
"$SC" new mon-deck --charte=<nom>  # créer un deck
"$SC" build decks/mon-deck         # → PPTX (livrable) ; ajoute --pdf pour un PDF
```

Et pointer vers le skill `deck` pour la suite (composition, mise au propre d'un PPTX existant, etc.).
