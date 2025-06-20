# But de ce repository

De base, ce repository est un **clone** de ce repertoire git:

```
https://github.com/ror-community/ror-records
```

Dans ce github, vous pouvez retrouver l'ensemble des **releases** de ror.org, avec pour chaque release, le contenu **json** des oragnisations **ajoutées** et **modifiées**. 

L'objectif est de créer pour chaque release, la transformation des json au format rdf. Ensuite, à partir de là, de créer un commit et un push automatique qui permettrait de merge l'ensemble des organisations vers le github. Le fait de faire un push séparé par release nous permettra donc de mettre des tags correspondant au nom de la release, et de faire un git diff pour voir l'historique des organisations modifiées ou ajoutées.

En résumé:

1. Passage de json à ttl
2. Commit and push par release
3. Git diff pour voir les modifications

## Problèmes

Parmi les choses auquelles il fallait s'attendre, il y avait la structure du json en fonction des différentes releases. En effet, au cours de son développement, ror a changé plusieurs fois l'architecture de son json, rendant le travail directement plus compliqué, car le template et le code n'est pas adapté à chaque structure. Il va sans doute falloir récupérer chaque version de structure, pour ensuite adapter le code en fonction de cela. En ce qui concerne les tests pour vérifier cela, voici ce que j'ai fais : 

```
1. Test sur v1.0/01912nj27.json
    --> erreur d'argument, car structure différente

2. Test sur structure similaire à celle du dernier dump disponible (v1.66-2025-05-20-ror-data.json)
    --> test sur fichier v1.66/00b3mhg89.json
        -> erreur d'argument, car structure différente
    --> test sur fichier v1.66/v1/00b3mhg89.json
        -> bonne sortie dans folder_to_push
```

Ce que nous allons essayer de faire, c'est de faire une détection de la version utilisée. En effet, à cette adresse, ror explique les différentes structures json utilisées au cours de leur développement.

```
https://github.com/ror-community/ror-schema?tab=readme-ov-file
https://ror.readme.io/docs/schema-versions
```

Il reste maintenant à savoir à quelle version notre fichier json appartient. Il est aussi possible de faire une vérication de notre json à l'aide de ces commandes:

```
jsonschema -i test.json ror_schema_v2_0.json // obsolète avec jsonschema
check-jsonschema --schemafile test.json ror_schema_v2_0.json // dernière version
```

## Ce qui a été fait et problèmes survenus

La procédure pour arriver à notre fin est la suivante:

- récupération des structures json sur https://github.com/ror-community/ror-schema?tab=readme-ov-file
- création de **detect_version_json.py** pour trouver version de chaque json (**1.0**, **2.0**, **2.1**)
- création de 3 templates (**template_1_0**, **template_2_0**, **template_2_1**)
- **template_to_try.py** pour associer mes json à leur bon template
    - si aucune version correspond, **test** des json avec template
- **create_rdf_file.py** pour transformer json en rdf
    - si aucune version correspond, **rien** ne peut se faire donc erreur critique

Ceci vient régler la première partie du problèmes pour faire la transformation des json en rdf. Il manque maintenant la partie de commit et push automatique vers github.

‼️ Warning ‼️ Subyt écrase pour le moment les fichiers en double, ce qui veut dire qu'il y a normalement **64'000** files qui sont ajoutées et modifiées parmi toutes les releases. Cependant, dans le dossier de sortie, il n'y en a que **34'000**. Cela s'explique car il y a environ **30'000** files qui sont modifiées, donc comme subyt réécrit le json par dessus, cela ne tient pas en considération les anciens json.

Le problème sera résolu au moment de la partie commit & push sur github, car une fois push, les files seront supprimées du dossier en question, et il n'y aura **pas de doublon, ni de fichier effacé**.