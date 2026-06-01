# Mettre au propre un PPTX existant

> **CLI** : `slide-craft <cmd>` ci-dessous = `"$SC" <cmd>` avec `SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"` (à redéfinir dans chaque appel Bash — cf. SKILL.md « Invocation du CLI »). Le binaire s'auto-localise, pas d'`activate.sh`.

L'utilisateur a une source PPTX (souvent générée par Gamma, exportée de Google Slides, ou bricolée) et veut qu'on **rebatisse un deck propre dans une charte client**, en conservant le contenu.

## Étapes

### 1. Localiser la source et identifier la charte

```bash
"$SC" list-chartes
```

Si la charte cible n'existe pas, suivre [`04-add-charte.md`](04-add-charte.md) avant.

### 2. Extraire texte + assets

```bash
"$SC" extract-pptx ~/Téléchargements/source.pptx /tmp/extracted/
```

Produit :
- `slides.txt` : texte par slide (à parcourir pour comprendre la structure)
- `media/*.png|.jpg` : toutes les images embarquées (logos events, illustrations, photos hero)
- `slides/*.xml` : XML brut par slide (debug si besoin)

### 3. Comprendre la structure

Lire `slides.txt`. Identifier :
- Slide(s) cover (titre principal, sous-titre, branding)
- Slide(s) divider (transitions de partie)
- Slides "fiche" ou "contenu" répétitives (souvent 80% du deck — un format à transformer en `data.py`)
- Slides spéciales (citation, KPI, conclusion)

### 4. Mapper aux layouts disponibles

```bash
"$SC" list-layouts
```

Choisir un masque par type. Si aucun ne convient (ex: timeline horizontale, comparaison 3 cols), créer le masque manquant avant — voir [`03-add-layout.md`](03-add-layout.md).

### 5. Identifier et renommer les assets

Pour les fiches répétitives, chaque slide a souvent une image-clé (logo d'événement, portrait, capture). Slugifier et copier dans le dossier deck :

```bash
mkdir -p decks/<nom>/assets/<type>/
cp /tmp/extracted/media/imageXX.png decks/<nom>/assets/<type>/<slug>.png
```

L'image-clé est généralement la **plus grosse** image unique à chaque slide (les pictogrammes communs apparaissent partout).

### 6. Scaffolder le deck

```bash
"$SC" new <nom> --charte=<charte>
```

### 7. Modéliser le contenu dans `data.py`

Convertir `slides.txt` en structure Python. Pour les benchmarks events, le pattern est `LIST_OF_DICTS = [...]` avec une dict par fiche. Toujours inclure une clé `slug` qui pointe vers l'asset image (logo de la fiche).

**Les assets de marque sont auto-injectés depuis la charte.** Tu ne passes `photo_path` / `logo_path` / `brand_logo_path` que si tu veux **override** le défaut. Les layouts (`cover_split`, `event_fiche`, etc.) lisent :
- `ca.default("cover_photo")` — photo hero de la couverture
- `ca.default("cover_logo")` — logo avec baseline en bas de cover
- `ca.default("header_logo")` — logo dans le bandeau supérieur des slides de contenu

déclarés dans `chartes/<nom>/tokens.json` section `defaults`. Si la charte ne les déclare pas, les layouts dégradent proprement (champs vides au lieu de planter).

### 8. Composer `build.py`

Garder court (~50-80 lignes). Boucler sur les données et appeler le layout adéquat. Auto-injection de `page_num` par `Deck.add()` ; auto-injection des assets de charte par les layouts.

Pour un benchmark events typique :
```python
ca = Charte.load("<charte>")
deck = Deck(charte=ca)
deck.add(cover_split.render, **COVER)             # photo + logo charte auto
for section_key, fiches in SECTIONS:
    deck.add(section_divider.render, **DIVIDERS[section_key])
    for fiche in fiches:
        kwargs = {k: v for k, v in fiche.items() if k != "slug"}
        deck.add(event_fiche.render,
                 section_tag=DIVIDERS[section_key]["tag"],
                 logo_path=str(LOGOS / f"{fiche['slug']}.png"),  # logo event
                 **kwargs)                                       # brand_logo_path auto
```

### 9. Builder

```bash
"$SC" build decks/<nom>
```

→ `out/deck.pptx` + `out/deck.pdf`.

### 10. Réviser

Ouvrir le PDF. Vérifier :
- Charte respectée (couleurs et fonts via `ca.color(...)` et `ca.font_primary`)
- Logos client en place
- Textes lisibles (pas d'overflow)
- Numérotation cohérente

Itérer sur `data.py` + `build.py` jusqu'à satisfaction. Ne pas modifier le PPTX généré directement — toujours rebuilder depuis la source.

## Pièges courants

- **Tout en monochrome** : oublié d'utiliser les accents secondaires. Faire varier `color("primary")` (corporate) et `color("signature")` (décoratif).
- **Police absente** : si le PPTX s'ouvre avec une font de fallback, vérifier que les TTFs de la charte sont installés en système (`fc-list | grep <font>`).
- **PDF qui diffère du PPTX** : pas censé arriver avec LibreOffice — si ça arrive, suspicion d'absence du module `libreoffice-impress`.
- **PPTX trop léger** (< 200K) : signe qu'on a oublié les assets visuels. Le rendu sera austère. Revoir étape 5.
