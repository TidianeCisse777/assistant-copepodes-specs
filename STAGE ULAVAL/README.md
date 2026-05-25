# STAGE ULAVAL

Ce dossier contient le corpus métier complet du stage : use cases, capacités, contraintes et documents RAG scientifiques. Il sert de source de vérité métier historique pour construire l'assistant copépodes.

## Rôle dans le repo

Les fichiers de ce dossier décrivent ce que l'assistant doit faire, pourquoi il doit le faire et quelles règles il doit respecter. Ils sont plus détaillés que les documents de synthèse dans `docs/`.

Le runtime cible n'est pas ici. Ces documents alimentent l'implémentation dans IDEA.

## Structure

| Chemin | Rôle |
|---|---|
| `USE CASE/` | Use cases complets : scénarios utilisateur et critères d'acceptation |
| `Agent/Spec de L'agent/` | Capacités et contraintes agent |
| `Agent/Ressources scientifiques/Document RAG/` | Corpus RAG utilisé par l'assistant |
| `ANALYSE EXIGENCE/` | Espace local d'analyse d'exigences, peut être vide |
| `Analyse sur les données/` | Espace local d'analyse de données, peut être vide |

## Documents RAG

Les documents dans `Agent/Ressources scientifiques/Document RAG/` sont structurés pour l'indexation RAG :

- chunks séparés par `---` ;
- titres formulés comme des questions ;
- lignes `Mots-clés : ...` ;
- tableaux courts ;
- règles opérationnelles explicites.

## Attention aux termes historiques

Certains anciens libellés peuvent encore refléter l'historique du projet ou des formulations héritées. Les décisions actuelles sont :

- l'identité cible est `Assistant graphique copépodes` ;
- le runtime cible est IDEA ;
- OBIS n'est pas une source autorisée dans le prompt cible ;
- OGSL et Bio-ORACLE sont les sources complémentaires à intégrer pour le contexte environnemental ;
- les IDs EcoTaxa/EcoPart cités dans les probes sont des exemples de données explorées, pas des constantes du système final.

En cas de conflit, suivre `docs/CONTEXT.md`, `PLAN.md`, `TOOLS_SPEC.js` et `TEST_SCENARIOS.md`.
