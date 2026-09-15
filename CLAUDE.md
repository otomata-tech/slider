# slider — guide projet

Atelier pour produire des decks PowerPoint propres (PPTX, et PDF à la demande) à partir de données structurées et d'une charte client. Vue d'ensemble : [`README.md`](./README.md).

## Principes

- **Charte = source de vérité.** Toute couleur et toute police d'un slide vient de `chartes/<marque>/tokens.*` — jamais un hex en dur dans un masque ou un build.
- **Données séparées du rendu.** `data.py` décrit le contenu, le masque choisit la composition, la charte fixe le look.
- **Python natif, pas de DSL.** Pas de YAML ni de JSON intermédiaire : `python-pptx` impose Python, un agent l'écrit aussi facilement, et les signatures typées des `render()` font un contrat lisible.
- **Le livrable est le PPTX.** Le PDF (`build --pdf`) et les PNG (`preview`) ne sont produits **qu'à la demande explicite**. `export_pdf` est opt-in (`SLIDER_PDF=1`) : ne jamais faire dépendre la chaîne de LibreOffice.
- **Self-contained** : `cd slider && claude` détecte le skill via le symlink committé `.claude/skills/deck → demo/`.
- ⚠️ **Le dépôt moteur est PUBLIC : zéro contenu client.** Jamais de branding, d'asset ni de deck client ici. `decks/` est gitignoré, les previews (`layouts/previews/`) se rendent avec la charte `blank` et jamais avec un deck client, et les thèmes clients vivent dans des **dépôts privés séparés** clonés dans `chartes/<client>/`, ou sont distribués en zip. Auditer l'arbre **et l'historique** avant tout passage public.

## Stack

`python-pptx` (construction du PPTX) · `Pillow` (inspection d'images) · LibreOffice `soffice` en option pour le PDF (`lib/pdf_export.py`, retry sur profil isolé si la passe rapide échoue). Aucun service externe, aucun bundler.

## Skills du plugin

| Skill | Rôle |
|---|---|
| `install` | prépare l'environnement (dépendances, LibreOffice, charte à un chemin stable) |
| `deck` | créer / nettoyer / recréer un deck, ajouter masque, charts, depuis doc/pdf/pptx |
| `review` | lint de conformité d'un `.pptx` à sa charte |
| `theme` | créer / dériver / éditer une charte, y compris **ingest** d'un template client |

⚠️ **Skill ≠ CLI** : le skill s'appelle `deck`, le binaire moteur interne (appelé par Claude, jamais par l'utilisateur) reste `slide-craft`. Règle : **un skill = un workflow**, pas une primitive — un masque, un helper ou un sous-format vit dans `deck`, pas dans un skill à part. Câblage : `skills/<nom>/SKILL.md` + symlink `.claude/skills/<nom>`.

## Invocation du CLI

⚠️ **Le CLI n'est jamais sur le `PATH` côté skill**, et `activate.sh` ne survit pas d'un appel Bash à l'autre (shells sans état). Les SKILL.md et les guides appellent donc le binaire **par chemin absolu, redéfini à chaque appel** :

```bash
SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"
"$SC" list-layouts
```

Plugin installé → `$CLAUDE_PLUGIN_ROOT` est posé par Claude Code ; en dev in-repo, le repli `.` suffit. Le binaire s'auto-localise (`_common.py` dérive `PROJECT` via realpath) : aucune variable d'environnement n'est requise. **Ne jamais écrire `slide-craft <cmd>` en cru dans un SKILL ou un guide** — ça suppose un PATH qui n'existe pas.

## Chartes

`Charte.load(name)` cherche dans l'ordre : `$PWD/chartes/` (override par deck) → `~/.local/share/slider/chartes/` (ou `$XDG_DATA_HOME`) → `<engine>/chartes/` (le `blank` intégré et les thèmes clonés en dev). `slide-craft list-chartes` itère ces chemins, premier vu gagnant.

⚠️ **Une charte cliente se clone dans `<workspace>/chartes/<nom>/` ou dans le dossier utilisateur, jamais dans le cache du plugin** (`$CLAUDE_PLUGIN_ROOT/chartes/`), effacé à chaque `claude plugin update`.

`slide-craft new mon-deck` scaffolde dans `$PWD/decks/mon-deck/` : c'est le cwd qui décide où atterrissent les decks.

## Mode template-natif (ingest, NativeDeck, ModelDeck)

Deuxième voie, **à privilégier quand le client a un vrai template PPTX** : au lieu de reskiner les masques génériques, on remplit les **propres masques du client**. Un thème n'est pas un nuancier, c'est le template préservé.

- `slide-craft ingest <template.pptx> --name=<t>` (`lib/template.py`) préserve le template et écrit un `catalog.json` (masques → placeholders, **rôle déduit par type et position**, jamais par idx), les tokens dérivés du thème et les photos récoltées.
- `slide-craft catalog <t>` rend le digest des masques (rôles, capacité) pour en **choisir** un ; `new-native` scaffolde ; `build` et `preview` réutilisent la tuyauterie standard.
- `NativeDeck` (`lib/native.py`) remplit **par rôle**, avec `fit_text` anti-débordement, et **avertit** si un champ n'a pas de cible — aucun repli silencieux.
- Deux sous-modes détectés à l'ingest (`catalog.json#mode`) : `layouts` (le template a une bibliothèque de masques → `NativeDeck`) et `models` (pas de masques, le design est dessiné sur les slides → `ModelDeck`, `lib/models.py`, qui clone une slide-modèle et réécrit son texte par ancre).
- ⚠️ **Piège vu deux fois** : une charte ingérée ne se compose **jamais** avec le kit de masques génériques — on reprend la palette et on perd tout le design du template. Un `catalog` qui n'affiche qu'un masque ne veut pas dire « template pauvre », il veut dire mode natif. Router : `catalog.json` présent → `NativeDeck`/`ModelDeck` ; charte tokens-only → kit générique.
- Limite connue : la détection `subtitle` rate sur les masques à panneau gauche étroit (placeholder < 18 cm classé `content`) ; le sous-titre est ignoré, avec avertissement.

Guide : [`demo/guides/07-template-native.md`](./demo/guides/07-template-native.md).

## Conventions

- **Slides 16:9** : `339,9 mm × 190,5 mm`. Marge de page : 9 mm.
- Couleurs par `ca.color("…")` et polices par `ca.font_primary` — jamais de `font_name="Calibri"` en dur.
- **Assets auto-injectés** : les masques lisent `ca.default("cover_photo")`, `("cover_logo")`, `("header_logo")` depuis `tokens.json#defaults` si l'appelant ne les fournit pas — un nouveau deck n'a pas à câbler les assets de marque dans son `build.py`.
- **Boucle de composition** : `doctor <charte>` → `layout-info <nom>` (la signature exacte avant de remplir) → `lint <deck>` → `build` → `preview` ou `--pdf` seulement à la demande.
- **`lint` rend pour de vrai** : il valide les kwargs et les chemins d'image, puis rend chaque slide dans une présentation jetable (il attrape les tokens de couleur ou d'échelle manquants, les assets, les bugs de masque). Un `✓ conforme` garantit que le `build` passera.
- **`doctor <charte>`** scanne les littéraux `color()` / `token_size()` des masques et liste ce que la charte ne fournit pas. Indispensable après un `ingest` : une charte dérivée d'un template manque souvent des tokens du kit générique.
- **API d'un masque** : `layouts/<nom>.py` expose `render(slide, charte, *, …, page_num: int)` — `slide` et `charte` positionnels en premier, tout le reste en kwargs, `page_num` auto-injecté par `Deck.add` s'il est déclaré, aucun effet de bord hors du `slide` reçu. La liste des masques se lit par `slide-craft list-layouts`, pas ici.

## Guides

`demo/guides/` : `01-cleanup-existing.md` (mettre au propre un PPTX existant) · `02-compose-new.md` (composer de zéro) · `03-add-layout.md` (ajouter un masque) · `04-add-charte.md` (ajouter une charte) · `07-template-native.md` (refaire un deck dans le template du client).
