# blank — placeholder charte

Charte neutre (bleu royal + ambre, Inter) servant de point de départ pour créer une charte client.

## Pour créer une nouvelle charte

```bash
cp -r chartes/blank chartes/<client>
```

Puis éditer `chartes/<client>/tokens.json` :
- Mettre à jour `name`, `label`, `source`
- Remplacer les couleurs (au minimum : `primary`, `signature`, `text`)
- Pointer la police primaire vers la font du client
- Déposer logos / photos / fonts dans `assets/`
- Renseigner `defaults.cover_photo`, `defaults.cover_logo`, `defaults.header_logo`

Pour distribuer la charte d'un client séparément du moteur slider, créer un repo dédié `slider-<client>` qui ne contient **que** son dossier `chartes/<client>/`. Voir `INSTALL.md` à la racine du moteur pour la résolution multi-chemin via `SLIDER_THEMES_PATH`.
