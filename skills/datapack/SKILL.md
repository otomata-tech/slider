---
name: datapack
description: Produire un datapack Excel (.xlsx) à la charte d'un client — tableaux financiers (P&L, bilan, KPIs, contrôles) mis en forme par le moteur, jamais à la main. À charger dès qu'on demande un datapack, un databook, un onglet Excel « au format » ou de mettre des tableaux Excel à la charte.
---

# Datapack Excel à la charte

Tu décris le contenu en JSON, le moteur fait **toute** la forme : police, couleurs, bordures, formats de nombre, formules de variation, colonne Source, contrôles. Tu n'écris jamais de mise en forme toi-même (ni openpyxl, ni style de cellule) : si la charte ne permet pas un rendu, dis-le plutôt que de le bricoler.

Le CLI s'appelle **par chemin absolu, redéfini à chaque appel** :

```bash
SC="${CLAUDE_PLUGIN_ROOT:-.}/demo/bin/slide-craft"
"$SC" datapack --describe --charte=<charte>     # types de lignes, formats, sources, fonctions autorisés
"$SC" datapack spec.json --charte=<charte> --check
"$SC" datapack spec.json --charte=<charte> -o datapack.xlsx
```

## La boucle

1. `--describe` : lis ce que la charte autorise. Les **sources** et les **fonctions Excel** sont des listes fermées.
2. Écris `spec.json` (modèle : `exemples/compte-de-resultat.json`).
3. `--check` jusqu'à `✓ conforme` : chaque erreur dit l'onglet, la ligne et quoi corriger.
4. Rends le `.xlsx`. Excel recalcule les formules à l'ouverture.

## La spec

```json
{"sheets": [{
  "name": "P&L", "title": "Projet X | Compte de résultat", "unit": "€ en milliers",
  "columns": [{"kind": "value", "period": "24", "header": "FY24"},
              {"kind": "value", "period": "25", "header": "FY25"},
              {"kind": "gap"},
              {"kind": "var", "header": "Var.", "from": "24", "to": "25"},
              {"kind": "note", "header": "Note"}],
  "groups": [{"from": "24", "to": "25", "text": "Historique"}],
  "rows": [
    {"kind": "band", "label": "Chiffre d'affaires", "key": "ca", "values": [1000, 1100], "source": "Comptabilité", "var": "pct"},
    {"kind": "line", "label": "Achats", "key": "ach", "values": [-400, -450], "source": "Comptabilité", "var": "pct"},
    {"kind": "subtotal", "label": "Marge brute", "key": "mb", "values": "={ca}+{ach}", "var": "pct"}
  ]}]}
```

- **Colonnes** : `value` (une période), `var` (variation `from` → `to` ; `force_abs: true` pour un écart en valeur), `gap` (colonne vide), `note`.
- **Lignes** : `kind` parmi ceux de la charte (`--describe`), plus `spacer`, `dots`, `footnote`, `text`. `values` est une liste (une valeur par colonne `value`, texte permis : « n.c. ») ou **une** formule appliquée à toutes les périodes. `var` : `pct`, `pp`, `abs`, `cagr` (avec `years` sur la colonne). `format`, `indent`, `note` facultatifs.
- **Formules** : jamais de référence de cellule en dur. `{clé}` même période, `{clé@25}` période fixée, `{Onglet!clé}` autre onglet, même période. Seules les fonctions de la charte passent (sous-total : `{a}+{b}` ou `SUM`).
- **Sources** : uniquement un libellé de la liste de la charte, sur les lignes saisies (pas sur les formules).
- **Contrôles** : une ligne `check` (écart attendu nul) s'allume si l'écart dépasse la tolérance.

## Ce que tu ne fais pas

- Retoucher le `.xlsx` après rendu (styles, fusions, colonnes) : on corrige la spec, ou la charte si la règle change.
- Inventer une source, un type de ligne ou une fonction : ce qui manque se demande à qui tient la charte.
