
## 1. Données (FAIT)

C’est la priorité absolue.

Tu dois clarifier :

- quelles données existent ;
    
- où elles sont stockées ;
    
- formats : CSV, NetCDF, images, JSON, Excel, sorties de modèles ;
    
- volume ;
    
- fréquence de mise à jour ;
    
- qualité des données ;
    
- données manquantes / aberrantes ;
    
- étapes actuelles de nettoyage ;
    
- qui comprend vraiment chaque donnée.
    

Pourquoi c’est prioritaire : dans une architecture IDEA, l’assistant dépend directement des **instructions + données + outils + environnement de calcul**. Si les données sont floues, tout le reste devient fragile. Le papier IDEA insiste justement sur l’accès aux données, aux outils analytiques et à l’environnement de calcul comme cœur du système.

## 2. Workflows actuels  ( FAIT )

Avant les use cases formels, cartographie le chemin réel :

**image / fichier brut → nettoyage → extraction → modèle → simulation → graphique → interprétation scientifique**

À documenter :

- qui fait chaque étape ;
    
- avec quel outil ;
    
- combien de temps ça prend ;
    
- quelles étapes sont manuelles ;
    
- où il y a des frictions ;
    
- où il y a des erreurs fréquentes ;
    
- quelles étapes sont déjà automatisées.
    

C’est ici que tu identifies la vraie valeur du projet.

## 3. Use cases prioritaires  (FAIT)

Ensuite seulement, transforme les workflows en use cases.

Priorité aux use cases qui combinent :

- forte fréquence ;
    
- forte douleur ;
    
- forte valeur scientifique ;
    
- faisabilité technique raisonnable.
    

Exemples possibles :

- importer un fichier d’imagerie ;
    
- nettoyer les mesures aberrantes ;
    
- lancer une simulation Compupod ;
    
- générer un graphique scientifique ;
    
- comparer deux scénarios ;
    
- expliquer un résultat.
    

Le piège serait de lister trop de use cases. Pour une V1, vise 2 ou 3 use cases centraux maximum.

## 4. Utilisateurs et rôles  (FAIT)

Clarifie qui va utiliser l’assistant :

- professeur / chercheur ;
    
- étudiant gradué ;
    
- stagiaire ;
    
- technicien ;
    
- collaborateur externe.
    

Pour chaque rôle :

- ce qu’il sait déjà faire ;
    
- ce qu’il ne veut plus faire manuellement ;
    
- ce qu’il doit vérifier ;
    
- le niveau de confiance attendu envers l’agent.
    

C’est important parce que l’IDEA montré dans l’article reste utile surtout si l’utilisateur peut repérer les erreurs et corriger l’assistant. Les auteurs soulignent que les résultats importants doivent être vérifiés.

## 5. Sorties attendues (PAS FAIT)

Définis précisément ce que l’agent doit produire :

- graphiques ;
    
- tableaux ;
    
- fichiers nettoyés ;
    
- scripts Python ;
    
- rapports courts ;
    
- diagnostics textuels ;
    
- logs d’exécution ;
    
- comparaison de scénarios.
    

Pour chaque sortie, précise :

- format ;
    
- niveau de détail ;
    
- unités ;
    
- conventions scientifiques ;
    
- qualité attendue ;
    
- exemple d’une bonne sortie.
    

## 6. Outils, scripts et modèles existants  (PAS FAIT)

Tu dois inventorier :

- scripts Python/R/Matlab existants ;
    
- notebooks ;
    
- modèle Compupod ;
    
- pipelines d’imagerie ;
    
- fonctions de nettoyage ;
    
- fonctions de visualisation ;
    
- GitHub du projet ;
    
- dépendances ;
    
- commandes pour lancer les simulations.
    

Dans ton objectif de stage, les trois blocs importants sont justement : extraction/parsing des données, exécution de code/simulation, puis génération de graphiques et diagnostic.

## 7. Contraintes techniques  (PAS FAIT)

À traiter ensuite :

- environnement local ou serveur ;
    
- Docker ou non ;
    
- accès GPU/CPU ;
    
- stockage ;
    
- sécurité ;
    
- accès Internet ;
    
- confidentialité des données ;
    
- droits d’écriture ;
    
- librairies autorisées ;
    
- temps maximal d’exécution.
    

C’est stratégique : un agent qui exécute du code peut être puissant, mais il faut cadrer où il a le droit de lire, écrire et lancer des scripts.

## 8. Critères de validation  (PAS FAIT)

Définis comment on saura que l’assistant fonctionne.

Exemples :

- même résultat qu’un script humain de référence ;
    
- graphique conforme à un exemple validé ;
    
- simulation lancée sans erreur ;
    
- valeurs numériques dans une tolérance définie ;
    
- code reproductible ;
    
- logs consultables ;
    
- résultat validé par un chercheur.
    

Sans critères de validation, tu risques de construire une démo impressionnante mais scientifiquement peu fiable.

