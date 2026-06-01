# Ajouter une nouvelle charte (marque cliente)

> **CLI** : `slide-craft <cmd>` ci-dessous = `"$SC" <cmd>` avec `SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"` (à redéfinir dans chaque appel Bash — cf. SKILL.md « Invocation du CLI »). Le binaire s'auto-localise, pas d'`activate.sh`.

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

**Seule source de vérité** du thème. Le moteur ne lit que ce fichier — pas de duplicate `.py` / `.css` à maintenir en parallèle. Cf. `chartes/blank/tokens.json` pour le format complet.

Clés **obligatoires** pour que les layouts existants marchent :
`primary`, `primary-deep`, `signature`, `text`, `text-strong`, `muted`, `bg`, `rule`, `panel-mint`, `panel-cream`.

### 4. Placer les assets

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

### 5. Installer les polices en système

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

### 6. Documenter

Créer `chartes/<nom>/README.md` :
- Sources (lien CSS scrapé, PDF brand book, …)
- Palette avec aperçus hex
- Notes spécifiques (variantes, contextes d'usage)

### 7. Valider

```bash
"$SC" new test-<nom> --charte=<nom>
# éditer data.py + build.py pour ajouter 1 cover + 1 fiche
"$SC" build decks/test-<nom>
```

Ouvrir le PDF. Si les couleurs ou la police diffèrent du brand book, corriger `tokens.json` et rebuilder.

## Conventions

- **Une charte = une marque**, pas une variante. Pour des variantes (sous-marque dérivant d'une charte mère), créer une charte enfant (`chartes/<variante>/`) qui réécrit certains tokens. **À noter** : il n'y a pas aujourd'hui de mécanisme d'héritage entre chartes — chaque `tokens.json` est autonome et complet.
- **Les chartes sont versionnées dans le repo** (`tokens.*` + petits assets). Les gros assets (photos HD, vidéos) peuvent rester hors repo si > 5 MB.
- **Ne jamais hardcoder une couleur dans un layout**. Si un layout a besoin d'une couleur que la charte n'expose pas, soit on ajoute le token, soit on dérive d'un existant.
