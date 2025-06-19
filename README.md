# But de ce repository

De base, ce repository est un **clone** de ce repertoire git:

```
https://github.com/ror-community/ror-records
```

Dans ce github, vous pouvez retrouver l'ensemble des **releases** de ror.org, avec pour chaque release, le contenu **json** des oragnisations **ajoutées** et **modifiées**. 

L'objectif est de créer pour chaque release, la transformation des json au format rdf. Ensuite, à partir de là, de créer un commit et un push automatique qui permettrait de merge l'ensemble des organisations vers le github. Le fait de faire un push séparé par release nous permettra donc de mettre des tags correspondant au nom de la release, et de faire un git diff pour voir l'historique des organisations modifiées ou ajoutées.

En résumé:

1 - Passage de json à ttl
2 - Commit and push par release
3 - Git diff pour voir les modifications



