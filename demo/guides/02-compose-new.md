# Composer un deck à partir de zéro

L'utilisateur n'a pas de source — il veut un deck X dans une charte Y avec une structure narrative donnée.

## Étapes

### 1. Clarifier la commande

Demander/inférer :
- **Charte** : laquelle (`slide-craft list-chartes`) ? Si nouvelle, → [`04-add-charte.md`](04-add-charte.md).
- **Objectif** : à qui ça s'adresse, pour quoi (pitch, restitution, formation, etc.) ?
- **Volume** : nombre de slides cible (5, 15, 30) ?
- **Narration** : grandes parties / sections ?

### 2. Lister les masques dispo

```bash
slide-craft list-layouts
```

Et lire `layouts/README.md` pour voir les aperçus.

### 3. Tracer la séquence de slides

Faire un sommaire avant de coder, sous forme de liste :

```
1. cover_split        – titre principal
2. quote              – mise en bouche
3. section_divider    – "Partie 1 : Diagnostic"
4. two_columns        – problème vs opportunité
5. big_number         – KPI majeur
…
N. thank_you          – conclusion + contact
```

Si un masque manque pour ta narration, créer-le avant — voir [`03-add-layout.md`](03-add-layout.md). Ne **jamais** détourner un masque existant (ex: utiliser `event_fiche` pour autre chose qu'un event), ça pollue la bibliothèque.

### 4. Scaffolder

```bash
slide-craft new <nom> --charte=<charte>
```

### 5. Remplir `data.py`

Une clé par slide ou par lot homogène :

```python
CONTENT = {
    "cover": dict(title_lines=[...], ...),
    "quote_intro": dict(quote="...", author="..."),
    "section_1": dict(tag="DIAGNOSTIC", title="...", subtitle="..."),
    "kpi_1": dict(value="50+", label="..."),
    …
}
```

Plus `data.py` est plat (sans logique), plus c'est lisible.

### 6. Composer `build.py`

Une ligne par slide :

```python
deck.add(cover_split.render,      **CONTENT["cover"])
deck.add(quote.render,             **CONTENT["quote_intro"])
deck.add(section_divider.render,   **CONTENT["section_1"])
deck.add(big_number.render,        **CONTENT["kpi_1"])
…
```

### 7. Builder, réviser, itérer

```bash
slide-craft build decks/<nom>
```

Ouvrir le PDF. Quand ça part dans le mauvais sens (texte qui déborde, hiérarchie pas claire), **éditer `data.py` et rebuilder** — ne jamais bidouiller le PPTX généré directement.

## Conseils narratifs

- **Cover → ouverture → corps → fermeture**. Au moins un masque "calme" entre deux blocs denses (un quote, un big_number, un divider).
- **Une idée par slide**. Si une slide a plus de 30 mots, c'est trop.
- **Variez les masques**. Trois `event_fiche` à la suite c'est OK ; cinq c'est ennuyeux. Insérer un divider ou un quote.
- **La dernière slide n'est pas un thank_you mou** : c'est l'appel à l'action ou l'invitation au dialogue.
