---
name: theme
description: "Crée ou édite un thème (charte) : tokens.json + assets. Soit de zéro, soit dérivé d'un PPTX corporate / brand book (couleurs dominantes, polices, logos). Utiliser quand l'utilisateur dit 'crée une charte', 'crée une charte depuis ce pptx', 'extrais le thème de ce deck', 'fais un thème pour le client X', 'édite le thème', 'ajoute une couleur à la charte'."
argument-hint: "[<source.pptx> --name=<theme>]"
---

# theme

Crée ou édite un **thème** (charte) : la palette, les polices, les assets qui
définissent le look. Deux voies :

- **De zéro** : scaffolder un `chartes/<name>/tokens.json` et le remplir à la main
  → suivre le guide [`../../demo/guides/04-add-charte.md`](../../demo/guides/04-add-charte.md).
- **Dérivé d'un support de marque** (PPTX corporate, template client, brand book
  en PPTX) → procédure ci-dessous (`extract-charte`).

## Invocation du CLI

```bash
SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"
```
(à redéfinir dans chaque appel Bash — cf. le skill `deck`.)

## Distinction avec les autres skills

- **`theme`** (ici) : source → **thème** (tokens + assets). On produit une *charte réutilisable*.
- **`deck`** (`from-pdf` / `cleanup-existing`) : source → **un deck** dans une charte *déjà existante*.

Si l'utilisateur veut juste refaire UN deck, ce n'est pas ce skill → `deck`.

## Procédure

### 1. Classer couleurs et polices de la source

```bash
"$SC" extract-charte <source.pptx> --name=<theme>
```

Affiche les couleurs dominantes (par fréquence d'usage) avec un **rôle probable**
(bg clair / text sombre / couleur de marque saturée / neutre) et les polices.
Lire ce classement : c'est la matière première.

### 2. Écrire le squelette

```bash
"$SC" extract-charte <source.pptx> --name=<theme> --out=<engine>/chartes
```

Écrit `chartes/<theme>/tokens.json` (squelette : `primary`, `text`, `bg`, etc.
assignés par heuristique + `_palette_brute` = toutes les couleurs vues).

> Destination : le dossier thèmes stable (`~/.local/share/slider/chartes`) pour
> un usage persistant, ou `chartes/` du moteur en dev.

### 3. Raffiner les rôles (jugement)

L'heuristique propose ; toi tu **valides et complètes** en éditant `tokens.json` :
- Vérifier `primary` (la couleur de marque dominante) et ajouter ses variantes
  (`primary-dark`, `primary-deep`) si la marque en a.
- Promouvoir depuis `_palette_brute` les **accents** (signature, mint, alert…) et
  les supprimer du tableau brut une fois assignés.
- Compléter `type-scale`, `radii`, `spacing`, `defaults` (cf. une charte
  existante comme référence, ex. `credit-agricole`).
- Renseigner `label`, `source`, `notes`.

Ne jamais laisser le squelette tel quel : c'est un point de départ, pas une charte.

### 4. Ajouter les assets

Extraire logos / photos de la source :
```bash
"$SC" extract-pptx <source.pptx> /tmp/brand/
```
Repérer les logos (images petites, récurrentes) et les ranger dans
`chartes/<theme>/assets/logo/`, `assets/photo/`, `assets/fonts/`. Câbler les
chemins dans `tokens.json#defaults` (`cover_logo`, `header_logo`, `cover_photo`).

Si la marque impose une police propriétaire, déposer les `.ttf` dans
`assets/fonts/` et ajuster `fonts.primary.local_files`.

### 5. Vérifier

```bash
"$SC" list-chartes                       # le thème apparaît
"$SC" new test-<theme> --charte=<theme>  # scaffold de contrôle
"$SC" build decks/test-<theme>           # rendu — ouvrir le PDF
```

Itérer sur `tokens.json` jusqu'à un rendu fidèle à la marque source.

## Limites

- `extract-charte` lit les couleurs/polices **explicites** du PPTX (runs + aplats),
  pas un thème PowerPoint non résolu ni un PDF. Pour un brand book PDF, demander
  un export PPTX ou relever les hex à la main.
- L'affectation des rôles est une **heuristique** (luminance/saturation) : toujours
  valider visuellement à l'étape 5.
