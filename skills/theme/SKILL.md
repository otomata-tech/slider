---
name: theme
description: "Crée ou édite un thème (charte) slider. Import depuis un support de marque, en DEUX modes : `ingest` (recommandé quand la source est un VRAI template PPTX avec ses masques) PRÉSERVE le template entier + catalogue ses layouts + dérive les tokens ; `extract-charte` (repli) ne relève que couleurs/polices d'un brand book sans masques. Ou créer un thème de zéro. Utiliser quand l'utilisateur dit 'crée une charte', 'crée un thème depuis ce pptx', 'importe le template du client X', 'extrais le thème de ce deck', 'édite le thème'."
argument-hint: "[<source.pptx> --name=<theme>]"
---

# theme

Crée ou édite un **thème** (charte). Point clé : **un thème n'est pas un
nuancier**. Si la source est un vrai template (master + slideLayouts), le thème
doit le **préserver en entier** — c'est lui qui porte le look (géométrie, décor,
styles), pas quelques tokens. Réduire un template à des couleurs/polices fait
perdre tout ce qui rend une slide « à la marque » (bonnes couleurs, mais mise en
page d'un autre kit).

Deux voies : **dériver d'un support de marque** (procédure ci-dessous) ou **créer
de zéro** un `tokens.json` à la main → guide
[`../../demo/guides/04-add-charte.md`](../../demo/guides/04-add-charte.md).

## Invocation du CLI

```bash
SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"
```
(à redéfinir dans chaque appel Bash — cf. le skill `deck`.)

## Choisir le mode

- **`theme`** (ici) : source → **thème** (template préservé + tokens). On produit une *marque réutilisable*.
- **`deck`** : source → **un deck** dans un thème *existant*. Si l'utilisateur veut juste refaire un deck, ce n'est pas ce skill.

Sinon, pour un import : la source a-t-elle des masques PowerPoint (slideLayouts) ?

```bash
"$SC" extract-pptx <source.pptx> /tmp/probe/ >/dev/null   # ou inspecter
python3 -c "from pptx import Presentation; p=Presentation('<source.pptx>'); \
print(sum(len(m.slide_layouts) for m in p.slide_masters), 'layouts')"
```

- **≥ ~5 layouts nommés → `ingest`** (mode template-natif, recommandé). On garde le template.
- **Pas de masques (brand book, export plat, PDF→PPTX) → `extract-charte`** (repli nuancier).

## Mode A — `ingest` (template préservé) ⟵ par défaut pour un template

```bash
"$SC" ingest <source.pptx> --name=<theme>     # → ~/.local/share/slider/chartes/<theme>/
```

Produit, dans `<theme>/` :
- **`template.pptx`** — le template du client, conservé tel quel (master + slideLayouts intacts).
- **`catalog.json`** — chaque layout → ses placeholders avec **rôle déduit** (title / eyebrow / subtitle / content / picture / number / footnote / footer) + une **signature** (nb de zones de contenu, photos, etc.) + un `kind` indicatif (cover / section / grid-N / list / statement / agenda / end).
- **`tokens.json`** — palette (clrScheme) + police (fontScheme) du thème, en métadonnée pour recolorer icônes / cadrer images.
- **`assets/photo/`** — photos du template (jpeg/png, wdp converti si `convert` dispo).

### Vérifier l'import

```bash
"$SC" catalog <theme>            # masques + rôles + capacité (lecture agent)
ls <theme>/                      # template.pptx + catalog.json + tokens.json + assets/
```

Contrôler : le nombre de layouts correspond au template, les rôles des placeholders
sont plausibles (un `title` par layout, des `content` dans la bande centrale,
`picture` repérées), la palette tokens contient bien les couleurs de marque.

### Construire un deck dans ce thème (template-natif)

On **remplit les layouts du thème par RÔLE** (jamais par idx — les variantes
renumérotent), via `NativeDeck`. Scaffold : `slide-craft new-native <deck> --theme=<theme>`,
puis `build` / `preview`. Détails : guide
[`../../demo/guides/07-template-native.md`](../../demo/guides/07-template-native.md).

> Affiner ensuite `tokens.json` (rôles `primary`/`signature`, variantes) reste
> utile pour les icônes/images, mais le rendu vient du template préservé.

## Mode B — `extract-charte` (repli : brand book sans masques)

Quand il n'y a pas de template à préserver — uniquement relever les couleurs/polices :

```bash
"$SC" extract-charte <source.pptx> --name=<theme>               # classe couleurs/polices
"$SC" extract-charte <source.pptx> --name=<theme> --out=<dir>   # écrit un squelette tokens.json
```

Puis raffiner `tokens.json` à la main (rôles `primary`/`signature`/accents depuis
`_palette_brute`, `type-scale`, `defaults`), ajouter logos/photos/fonts dans
`assets/`. Dans ce mode, la géométrie viendra des layouts Python génériques de
slider (pas du client) — c'est un pis-aller esthétique, à réserver aux cas sans
template.

## Limites

- `ingest` lit le thème PPTX résolu (clrScheme) : il récupère la vraie palette même
  quand les runs n'ont que des couleurs de thème — là où `extract-charte` ne voit
  que des gris. Préférer `ingest` dès qu'il y a des masques.
- Le mapping tokens d'`ingest` (primary/signature) est heuristique — raffinable,
  mais secondaire puisque le look vient du template.
- `kind` du catalogue est indicatif : un agent choisit le layout final avec jugement.
