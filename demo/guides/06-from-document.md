# Re-créer un deck à partir d'un document (mémo, note, doc)

> **CLI** : `slide-craft <cmd>` ci-dessous = `"$SC" <cmd>` avec `SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"` (à redéfinir dans chaque appel Bash — cf. SKILL.md « Invocation du CLI »).

L'utilisateur a un **document rédigé** (mémo d'investissement, note de cadrage, étude sectorielle — `.md`, `.docx`, ou un Google Doc collé) et veut le transformer en **deck structuré dans la charte**. Différent de `01-cleanup-existing` (qui part d'un *deck* existant) et de `05-from-pdf` (qui *recopie* une mise en page) : ici on **rédige la structure** à partir de prose.

## Principe

Un document linéaire n'a pas de slides. Le travail clé = **découper la narration en unités de slide** et **mapper chaque unité sur le bon gabarit**. C'est un acte de jugement éditorial, pas une conversion mécanique.

## Étapes

### 1. Lire et cartographier le document

Lire le document en entier. Identifier sa structure logique :
- La **thèse centrale** (la phrase que le dossier défend).
- Les **axes / parties** (2-4 blocs argumentatifs).
- Les **chiffres-clés** (valorisation, marché, ARR, ETP…).
- Les **comparaisons** (options, concurrents, scénarios).
- Les **cibles / sociétés** décrites en zoom.

### 2. Mapper les unités sur les gabarits PCDI

| Unité de contenu | Gabarit cible |
|---|---|
| Titre + thèse + contexte + 2 axes de synthèse | `exec_summary` |
| Démonstration en deux angles + chiffres | `thesis_two_col` (avec `stats`) |
| Comparaison d'options / concurrents | `comparison_table` (notes en `rating` 0-4) |
| Zoom sur une société / opportunité | `company_zoom` (reco + valo + description) |
| Une série de données (évolution, répartition) | `chart_block` (bar / line / donut) |
| Transition de partie | `section_divider` |
| Couverture | `cover_split` |

Voir les kwargs exacts : `slide-craft layout-info <nom>`.

### 3. Cadrer avec l'utilisateur avant de générer

Proposer un **plan de deck** (1 ligne par slide : gabarit + titre) et le faire valider. Ne pas inventer de chiffres : si le document ne donne pas une valeur, mettre un placeholder explicite (`00 M€`) plutôt qu'un nombre halluciné.

### 4. Scaffolder et modéliser

```bash
slide-craft new <nom> --charte=<charte>
```

Remplir `data.py` à partir du document (une structure par slide), puis composer `build.py` (un `deck.add(layout.render, **DATA)` par slide, dans l'ordre du plan validé).

### 5. Builder et réviser

```bash
slide-craft build decks/<nom>
```

Ouvrir le PDF, vérifier la densité (le kit veut des slides respirantes : 3-5 puces max, un chiffre par carte), ajuster, rebuilder.

## Garde-fous

- **Pas d'hallucination de données** : tout chiffre vient du document source ou reste un placeholder.
- **Découper, pas tout caser** : un mémo de 5 pages ne fait pas 5 slides — il fait souvent 8-12 slides courtes. Préférer plus de slides aérées que des slides denses.
- **Toujours via la charte** : titres en capitales (`title_block`), puces « + » (`marker_list`), couleurs `ca.color`.
