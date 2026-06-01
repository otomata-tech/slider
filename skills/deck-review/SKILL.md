---
name: deck-review
description: "Audite un deck PowerPoint (.pptx) ou PDF contre une charte : couleurs hors-palette, polices hors-charte, titres non capitalisés, puces non conformes, contraste. Produit un rapport priorisé et propose des correctifs. Utiliser quand l'utilisateur dit 'relis ce deck', 'est-ce à la charte ?', 'audite ces slides', 'vérifie la conformité', 'lint ce pptx'."
argument-hint: "<deck.pptx|pdf> [--charte=<name>]"
---

# deck-review

Lint de conformité charte d'un deck existant. Sert le principe **« charte = source de vérité »** : transforme « est-ce bien à la charte ? » en check reproductible, puis propose des correctifs.

## Invocation du CLI

```bash
SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"
```
(à redéfinir dans chaque appel Bash — cf. le skill `slide-craft`, section « Invocation du CLI ».)

## Quand appeler ce skill

L'utilisateur a un deck **déjà fait** et veut savoir s'il respecte une charte (souvent `credit-agricole`), avant livraison ou après un import Gamma / Google Slides / PowerPoint manuel.

## Procédure

### 1. Identifier la charte de référence

Si l'utilisateur ne la précise pas, demander (ou déduire du contexte mission). Lister les chartes dispo :
```bash
"$SC" list-chartes
```

### 2. Lancer l'audit déterministe

Le deck doit être un `.pptx`. Si c'est un **PDF**, le convertir d'abord n'est pas fiable — demander la source PPTX, ou au minimum auditer visuellement (cf. étape 4).

```bash
"$SC" review <deck.pptx> --charte=<name>
```

Le script vérifie et reporte, par slide :
- **Couleurs hors-palette** : tout hex (texte ou aplat) absent des `tokens.json#colors`.
- **Polices hors-charte** : toute police hors `fonts.primary.family` + fallbacks.
- **Titres non capitalisés** : run ≥ 18pt dont le texte n'est pas en CAPITALES (le kit PCDI veut les titres en capitales).
- **Puces non conformes** : paragraphes démarrant par `•`, `▸`, `-`, `*`… (le kit impose le marqueur « + » vert / « – » rouge).

Exit code 0 = conforme, 1 = dérives détectées.

### 3. Interpréter et prioriser

Le script liste les **faits** ; le skill apporte le **jugement** :
- **Bloquant** : couleurs/polices hors-charte (cassent l'identité visuelle).
- **Important** : titres non-CAPS, puces rondes (signature PCDI).
- **À vérifier** : un hex très proche d'un token (ex. `#008991` vs `#008D7F`) = sans doute un ancien deck à re-skinner, pas une faute de fond.

Restituer un rapport court, priorisé, décidable — pas un dump.

### 4. Audit visuel complémentaire (optionnel)

Pour ce que le lint ne voit pas (chrome manquant, hiérarchie, densité, alignements), rendre le deck en PNG et inspecter :
```bash
"$SC" build <deck-dir>     # si on a les sources ; sinon convertir le pptx en pdf via LibreOffice
pdftoppm -png -r 90 <deck.pdf> /tmp/page
```
Puis lire les images et signaler : chrome PCDI absent, titres sans sous-titre vert, slides trop denses, etc.

### 5. Proposer des correctifs

Selon ce que veut l'utilisateur :
- **Rapport seul** : s'arrêter là.
- **Re-skin** : si le deck a des sources slide-craft, corriger `data.py`/`build.py` (couleurs via `ca.color`, titres `.upper()`, puces « + » via `marker_list`) et rebuilder.
- **Reconstruction** : si le deck est un import externe (Gamma…), basculer sur le skill `slide-craft` guide `01-cleanup-existing` pour le refaire propre dans la charte.

Ne jamais « corriger » en hardcodant un hex : toujours passer par un token de charte (ajouter le token si manquant).

## Limites

- Le lint lit le PPTX via python-pptx : il voit les couleurs/polices **explicites** sur les runs et aplats, pas celles héritées d'un thème PowerPoint ou d'un master non résolu.
- Le contraste AA et les alignements fins relèvent de l'audit visuel (étape 4).
