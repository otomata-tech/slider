---
name: slide-craft
description: "Produit des decks PowerPoint propres (PPTX + PDF) à partir d'une charte client, en composant des masques (layouts) réutilisables. Accepte aussi un PDF en source (extraction texte + images + layout). Utiliser quand l'utilisateur dit 'mets au propre ce pptx ou ce pdf', 'crée un benchmark', 'fais un deck X dans la charte Y'."
argument-hint: "[cleanup <source.pptx|pdf> | new <nom> --charte=<charte> | build <deck-dir> | list-layouts | list-chartes]"
---

# slide-craft

Atelier pour fabriquer des decks 16:9 (PPTX éditable + PDF de livraison) qui respectent strictement une charte de marque. PowerPoint est le format canonique : python-pptx construit, LibreOffice exporte en PDF — ce qui garantit que le PDF montre exactement ce que verra l'ouverture dans PowerPoint.

## Invocation du CLI (à lire en premier)

Le CLI `slide-craft` **n'est pas sur le `PATH`** quand le plugin tourne installé, et `source activate.sh` **ne survit pas** d'un appel Bash à l'autre (chaque appel est un shell neuf, sans état). Donc : **appelle toujours le binaire par chemin absolu**, et redéfinis-le dans **chaque** appel Bash :

```bash
SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"
"$SC" list-layouts
```

- **Plugin installé** : `$CLAUDE_PLUGIN_ROOT` est posé par Claude Code → pointe vers le moteur.
- **Dev in-repo** (`cd slider && claude`) : `$CLAUDE_PLUGIN_ROOT` non défini → fallback `.` = racine du repo (cwd).

Le binaire s'auto-localise (realpath) : pas besoin de `SLIDER_ROOT` ni d'`activate.sh`. `activate.sh` ne sert qu'à un humain en shell interactif. Dans les guides ci-dessous, `slide-craft <cmd>` est un raccourci de lecture pour `"$SC" <cmd>`.

## Composants

- **Chartes** (`chartes/<nom>/`) : tokens (couleurs, fonts, scale) + assets (logos, photos, fonts). Source de vérité pour le look. Tokens en JSON + Python + CSS.
- **Layouts** (`layouts/<nom>.py`) : bibliothèque de masques (cover, divider, fiche event, …). Chacun = une fonction `render(slide, charte, **kwargs)`. Catalogue avec aperçus dans `layouts/README.md`.
- **Lib** (`lib/`) : `Charte.load(name)`, `Deck()`, `pptx_to_pdf()`.
- **Decks** (`decks/<nom>/`) : data + assembleur + outputs. Instance d'un deck concret.

## Quand appeler ce skill

L'utilisateur veut :
- **Mettre au propre un pptx existant** → workflow [`guides/01-cleanup-existing.md`](guides/01-cleanup-existing.md)
- **Créer un deck à partir de zéro** → workflow [`guides/02-compose-new.md`](guides/02-compose-new.md)
- **Ajouter un nouveau type de slide** → workflow [`guides/03-add-layout.md`](guides/03-add-layout.md)
- **Ajouter une charte client** → workflow [`guides/04-add-charte.md`](guides/04-add-charte.md)
- **Re-créer un deck à partir d'un PDF source** → workflow [`guides/05-from-pdf.md`](guides/05-from-pdf.md)

## Conventions à respecter

1. **Jamais de couleur ou font hardcodée** dans un layout ou un build script. Toujours via `ca.color("primary")`, `ca.font_primary`, `ca.token_size("h1")`. Si la valeur manque dans la charte, l'ajouter à `tokens.json` plutôt que la hardcoder.
2. **Slides au format 16:9** : `33.867 × 19.05 cm` (constantes `lib.pptx_helpers.SLIDE_W_CM/H_CM`).
3. **`data.py` décrit le contenu, `build.py` assemble**. Le contenu et la composition restent séparés.
4. **Trois sorties par deck** : `out/deck.pptx` (éditable), `out/deck.pdf` (livraison). Le viewer interactif n'est pas systématique.

## Outils en ligne de commande

Tous les scripts sont sous `scripts/`. Appel par chemin absolu (cf. « Invocation du CLI ») — `SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"` :

```bash
"$SC" list-layouts                          # catalogue des masques
"$SC" list-chartes                          # marques dispo
"$SC" extract-pptx <source.pptx> <dest>     # texte + assets d'un pptx
"$SC" extract-pdf <source.pdf> <dest>       # texte + images + bboxes d'un pdf
"$SC" new <nom> --charte=<name>             # scaffold d'un nouveau deck
"$SC" build <deck-dir>                      # build.py + export PDF
```

## Workflow standard

Voir `guides/` pour les 4 recettes complètes. Aperçu général :

1. **Comprendre** : charte cible ? Contenu source ? Layouts adéquats ?
2. **Scaffolder** : `slide-craft new` crée la structure `data.py` + `build.py`.
3. **Modéliser** : remplir `data.py` (manuellement ou via extraction).
4. **Composer** : éditer `build.py` pour orchestrer les `deck.add(layout, ...)`.
5. **Builder** : `slide-craft build` → PPTX + PDF.
6. **Réviser** : ouvrir le PDF, ajuster, rebuilder.

## Pré-requis système

- **Python 3** avec `python-pptx`, `PyMuPDF` (`fitz`), `Pillow`.
- **LibreOffice** avec `libreoffice-impress` (sans Impress, la conversion PDF échoue silencieusement avec "source file could not be loaded").
- **Polices** : la charte peut bundler ses TTFs sous `assets/fonts/`. Pour le rendu, installer en système : `cp assets/fonts/*.ttf ~/.fonts/ && fc-cache -f`.
