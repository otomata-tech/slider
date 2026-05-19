# Ajouter une nouvelle charte (marque cliente)

## Étapes

### 1. Sourcer la charte officielle

- **Couleurs** : scraper le CSS du site corporate (`curl -sL <site>/main.css | grep -oE '#[0-9a-f]{3,6}' | sort | uniq -c`). Les valeurs les plus fréquentes sont les couleurs primaires.
- **Polices** : `grep font-family <css>`. Vérifier sur Google Fonts si dispo.
- **Logos** : si un PPTX corporate traîne, extraire avec `slide-craft extract-pptx`.
- Idéalement le client fournit un PDF brand guidelines + dossier d'assets.

### 2. Créer le squelette

```bash
mkdir -p chartes/<nom>/assets/{logo,photo,fonts}
```

### 3. Écrire `tokens.json`

Source de vérité. Cf. `chartes/credit-agricole/tokens.json` pour le format complet.

Clés **obligatoires** pour que les layouts existants marchent :
`primary`, `primary-deep`, `signature`, `text`, `text-strong`, `muted`, `bg`, `rule`, `panel-mint`, `panel-cream`.

### 4. Dériver `tokens.py` et `tokens.css`

Conversions mécaniques :

```python
# tokens.py
from pptx.dml.color import RGBColor
PRIMARY = RGBColor(0x00, 0x89, 0x91)
# ...
FONT_PRIMARY = "Raleway"
```

```css
/* tokens.css */
:root {
  --primary:   #008991;
  --signature: #82B600;
  --font-primary: "Raleway", sans-serif;
}
```

(Pas obligatoire — la lib lit `tokens.json` directement. Mais utile pour les humains et l'HTML.)

### 5. Placer les assets

```
chartes/<nom>/assets/
├── logo/
│   ├── <nom>-logo.png|.svg      # principal
│   └── <nom>-logo-white.png     # version monochrome blanche (fonds sombres)
├── photo/
│   └── *.jpg
└── fonts/
    └── *.ttf
```

### 6. Installer les polices en système

Pour que LibreOffice rende le PPTX avec la bonne police, les TTFs doivent être installés au niveau OS.

**Linux**
```bash
mkdir -p ~/.fonts/<nom>
cp chartes/<nom>/assets/fonts/*.ttf ~/.fonts/<nom>/
fc-cache -f ~/.fonts/
fc-list | grep -i "<font>"
```

**macOS**
```bash
cp chartes/<nom>/assets/fonts/*.ttf ~/Library/Fonts/
# Pas de cache à reconstruire — détection automatique.
# Vérifier dans Font Book.app
```

**Windows**
Double-clic sur chaque `.ttf` → bouton "Installer" (ou installation pour tous les utilisateurs si admin).

### 7. Documenter

Créer `chartes/<nom>/README.md` :
- Sources (lien CSS scrapé, PDF brand book, …)
- Palette avec aperçus hex
- Notes spécifiques (variantes, contextes d'usage)

### 8. Valider

```bash
slide-craft new test-<nom> --charte=<nom>
# éditer data.py + build.py pour ajouter 1 cover + 1 fiche
slide-craft build decks/test-<nom>
```

Ouvrir le PDF. Si les couleurs ou la police diffèrent du brand book, corriger `tokens.json` et rebuilder.

## Conventions

- **Une charte = une marque**, pas une variante. Pour des variantes (par ex. La Fabrique by CA dérivant de CA), créer une charte enfant (`chartes/la-fabrique-by-ca/`) qui override certains tokens et hérite des assets.
- **Les chartes sont versionnées dans le repo** (`tokens.*` + petits assets). Les gros assets (photos HD, vidéos) peuvent rester hors repo si > 5 MB.
- **Ne jamais hardcoder une couleur dans un layout**. Si un layout a besoin d'une couleur que la charte n'expose pas, soit on ajoute le token, soit on dérive d'un existant.
