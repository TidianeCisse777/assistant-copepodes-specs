# Guide du dépôt

## Résumé en une phrase

Ce dépôt prépare l'adaptation d'IDEA en assistant graphique pour données de copépodes : il rassemble les règles métier, les documents RAG, les contrats de tools, les scénarios de test et les preuves d'accès aux données.

## Problème traité

Les chercheurs NeoLab manipulent des sources hétérogènes : EcoTaxa, EcoPart, CTD, données labo et futures sources environnementales. Produire un graphique fiable demande de connaître les colonnes, les unités, les statuts de validation, les jointures et les limites techniques.

Ce dépôt réduit cette friction en documentant précisément :

- ce que l'assistant doit faire ;
- ce qu'il doit refuser ;
- quelles données existent ;
- comment les colonnes s'interprètent ;
- comment les sources peuvent être jointes ;
- comment vérifier que le comportement agent est correct.

## Ce que le dépôt n'est pas

Ce dépôt n'est pas le serveur FastAPI final, ni l'interface utilisateur finale, ni le fork IDEA complet. Il ne doit pas devenir un entrepôt de données brutes.

Le runtime cible vit dans IDEA. Les fichiers de ce dépôt servent à alimenter cette implémentation : prompts, RAG, tools, scénarios et décisions.

## Utilisateurs visés

Le produit final vise des professeurs et étudiants qui travaillent sur les copépodes marins. Le dépôt, lui, vise surtout :

- la personne qui implémente l'agent dans IDEA ;
- la personne qui maintient les documents RAG ;
- la personne qui vérifie les scénarios de test ;
- la personne qui doit comprendre pourquoi une source ou une colonne est utilisée.

## Périmètre fonctionnel cible

L'assistant doit :

- inspecter des fichiers chargés par l'utilisateur ;
- reconnaître les colonnes et leurs rôles ;
- consulter un corpus RAG court et fiable ;
- accéder à des sources en ligne seulement quand le mode source est activé ;
- préparer des tables de travail dérivées sans modifier les données brutes ;
- produire des graphiques statiques ou artefacts techniques ;
- documenter les colonnes, filtres, unités, méthodes et limites.

L'assistant ne doit pas :

- interpréter biologiquement les résultats ;
- inventer des valeurs ;
- supposer une source disponible sans preuve ;
- hardcoder les IDs EcoTaxa/EcoPart dans le système final ;
- exposer des credentials ou secrets ;
- modifier les données brutes.

## Sources de données concernées

| Source | Rôle dans le système | Statut dans ce repo |
|---|---|---|
| EcoTaxa | Objets individuels, taxonomie, morphométrie image | Accès authentifié testé avec probes |
| EcoPart | Profils UVP, bins de profondeur, volume, particules, CTD associée | Accès et logique de jointure explorés |
| CTD externe | Variables physico-chimiques indépendantes | Accès Amundsen/ERDDAP exploré |
| Données labo | Fichiers utilisateur, structure inconnue | À inspecter dynamiquement |
| OGSL / Bio-ORACLE | Sources environnementales complémentaires | Spécifiées dans les docs, à implémenter |

## Documents centraux

| Document | Rôle |
|---|---|
| `PLAN.md` | Plan d'implémentation cible dans IDEA |
| `ARCHITECTURE.md` | Diagrammes Mermaid de l'architecture cible |
| `TOOLS_SPEC.js` | Contrats des tools à implémenter |
| `TEST_SCENARIOS.md` | Scénarios de test comportemental |
| `docs/CONTEXT.md` | Glossaire métier et règles agent |
| `docs/DATA_ACCESS_METHODS.md` | Comment les sources ont été obtenues |
| `STAGE ULAVAL/.../Document RAG/*.md` | Corpus de référence utilisé par le RAG |
| `visualization/` | Visualisation interactive des use cases, capacités et contraintes |

## Documents RAG

Les documents RAG sont volontairement courts, découpés en chunks avec titres-question et mots-clés. Ils ne sont pas des notes libres : ils doivent répondre à des questions précises que l'agent posera pendant la planification ou la génération d'un graphique.

| Document RAG | Sert à répondre à |
|---|---|
| `colonnes_sources.md` | Quelles sources, colonnes, jointures et pièges ? |
| `colonnes_instruments.md` | Que signifient les colonnes par instrument ? |
| `copepodes_domaine.md` | Quels taxons et avertissements d'identification ? |
| `methodes_calcul.md` | Quelles formules, unités et limites de calcul ? |
| `sources_en_ligne.md` | Quelles sources en ligne et quelles limites d'accès ? |

## Critères de réussite produit

Le produit final est considéré correctement cadré si :

- une demande de graphique incomplète déclenche un blocage ou une clarification ciblée ;
- une demande complète produit un graphique avec axes, unités, source, filtres et limites ;
- les données brutes ne sont jamais modifiées ;
- les sources non activées ne sont pas appelées silencieusement ;
- les taxons non validés sont signalés comme limite ou exclus selon le choix utilisateur ;
- les jointures créent des colonnes de qualité de match ;
- les réponses restent techniques et ne deviennent pas interprétatives.

## Critères de réussite documentation

La documentation de ce dépôt est correcte si un nouveau contributeur peut :

- lire le README et comprendre le but du dépôt en moins de dix minutes ;
- utiliser `docs/FOLDER_MAP.md` pour savoir où chercher ;
- comprendre quelles données sont sûres à commiter ;
- distinguer specs, RAG, probes, fixtures et runtime cible ;
- retrouver les règles de comportement agent dans `docs/CONTEXT.md`, `PLAN.md` et `TEST_SCENARIOS.md`.

## Workflow de contribution recommandé

1. Modifier d'abord les specs Markdown de référence.
2. Mettre à jour les documents RAG si la modification touche les colonnes, sources, calculs ou limites.
3. Mettre à jour `TOOLS_SPEC.js` si un contrat de tool change.
4. Mettre à jour `TEST_SCENARIOS.md` si le comportement utilisateur change.
5. Mettre à jour `visualization/data.js` en dernier pour refléter les specs.
6. Ne jamais commiter `.env`, tokens, exports ZIP/TSV complets ou données sensibles.
