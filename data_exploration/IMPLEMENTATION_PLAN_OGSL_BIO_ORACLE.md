# Plan d'implémentation OGSL / Bio-ORACLE

Ce document décrit comment traduire les besoins utilisateur autour d'OGSL et de Bio-ORACLE en intégration cohérente avec l'architecture actuelle du projet.

Il ne décrit pas le code final ligne par ligne. Il fixe le contrat d'implémentation à respecter pour que les futurs connecteurs, tools et tests restent alignés avec le runtime IDEA.

## Objectif produit

Permettre à l'utilisateur de demander en langage naturel :

- "Va me chercher des données OGSL pour telle période / telle station / telle zone."
- "Va me chercher Bio-ORACLE pour telle période / tel scénario / telle variable."
- "Couple Bio-ORACLE avec mes données de zooplancton sur telle zone et telle période."
- "Utilise OGSL comme source environnementale pour mon use case."

Le système doit alors :

1. traduire la demande en paramètres explicites ;
2. vérifier si la source est activée ;
3. récupérer ou préparer la donnée distante ;
4. matérialiser une table de travail locale traçable ;
5. documenter la provenance, la période, les variables, la couverture et les limites.

## Architecture cible

L'architecture active du runtime IDEA sépare déjà les responsabilités utiles :

- `agents/` : comportement métier et instructions ;
- `core/mcp/` : gestion des connexions et appels de connecteurs distants ;
- `core/tool_registry/` : tools composables côté runtime ;
- `core/instruction_renderer/` : blocs d'instructions LLM ;
- `core/session_store.py` : état actif de session ;
- `core/prompt_store.py` : prompts actifs ;
- `core/rag_store.py` : corpus documentaire ;
- `routers/mcp_routes.py` : gestion des connexions MCP ;
- `routers/file_routes.py` : fichiers locaux ;
- `routers/chat_routes.py` : orchestration conversationnelle.

Le bon découpage est le suivant :

- **MCP** pour l'accès distant, authentifié ou catalogué ;
- **tool local** pour l'inspection, l'agrégation, la normalisation et la production de tables dérivées ;
- **prompt / instruction** pour l'orchestration conversationnelle et les demandes de clarification ;
- **RAG** pour les règles métier, les colonnes, les limites et les méthodes.

## Contrat utilisateur

### OGSL

L'utilisateur doit pouvoir demander :

- un profil CTD OGSL pour une période donnée ;
- des données OGSL sur une station, une mission ou une zone ;
- une variable spécifique sur une couche ou une profondeur ;
- un extrait environnemental régional pour un use case donné.

Le système doit demander les précisions manquantes si nécessaire :

- période de début et de fin ;
- station, mission ou zone ;
- variable(s) ;
- profondeur ou couche ;
- format de sortie ;
- utilisation finale.

### Bio-ORACLE

L'utilisateur doit pouvoir demander :

- des données Bio-ORACLE pour un scénario donné ;
- une variable environnementale sur une zone précise ;
- un enrichissement d'un jeu de données local avec Bio-ORACLE ;
- une comparaison entre plusieurs scénarios ou périodes.

Le système doit demander les précisions manquantes si nécessaire :

- variable environnementale ;
- scénario / modèle ;
- période cible ;
- zone ou coordonnées ;
- résolution / profondeur si pertinente ;
- méthode de couplage ;
- format de sortie.

## Découpage fonctionnel recommandé

### Couche 1 : intention conversationnelle

Responsabilité :

- comprendre la demande utilisateur ;
- décider si la demande relève d'OGSL, de Bio-ORACLE, ou d'un autre flux ;
- poser une question ciblée si une information bloquante manque ;
- éviter toute invention de paramètre.

Implémentation cible :

- prompt principal ;
- blocs d'instructions du mode plan/analyse ;
- règles de clarification ciblée.

### Couche 2 : résolution de paramètres

Responsabilité :

- convertir la demande en paramètres explicites ;
- normaliser période, zone, variable, scénario, profondeur, station, mission ;
- préparer une requête transportable vers le connecteur.

Implémentation cible :

- helper de parsing / normalisation ;
- éventuellement tool de validation des paramètres ;
- règles RAG pour les colonnes et les méthodes.

### Couche 3 : accès distant

Responsabilité :

- interroger OGSL ou Bio-ORACLE ;
- gérer auth, transport, pagination ou catalogue ;
- récupérer un extrait ou un agrégat utilisable ;
- ne pas exposer de secret.

Implémentation cible :

- connecteur MCP source-specific ;
- gestion de sessions / transports dans `core/mcp/manager.py` ;
- invocation dans `core/mcp/tools.py`.

### Couche 4 : préparation locale

Responsabilité :

- inspecter la réponse distante ;
- filtrer, normaliser, agréger ;
- construire une table de travail dérivée ;
- sauver la provenance et les limites.

Implémentation cible :

- tool local dans `core/tool_registry/` ;
- artefacts de session ;
- fichiers dérivés sauvegardés dans la session.

## Décision source par source

### OGSL

Recommandation :

- **MCP** pour la découverte et l'extraction distante ;
- **tool local** pour l'inspection et la mise en forme d'un extrait déjà récupéré.

Pourquoi :

- la donnée OGSL est avant tout une source distante exploitable par catalogue ou requête ;
- l'utilisateur veut typiquement demander une période, une station ou une zone ;
- le runtime doit pouvoir faire la même chose sans exposer la complexité réseau au niveau conversationnel.

### Bio-ORACLE

Recommandation :

- **MCP** pour la découverte et l'extraction distante ;
- **tool local** pour le post-traitement, le couplage et la production d'une table dérivée.

Pourquoi :

- Bio-ORACLE est typiquement demandé comme couche environnementale à récupérer ou à interpoler ;
- la source a un fort besoin de paramétrage (scénario, période, zone, variable) ;
- le runtime doit pouvoir matérialiser localement la table couplée pour le graphe.

## Flux d'implémentation

### Flux OGSL

1. L'utilisateur demande un extrait ou un profil OGSL.
2. Le modèle vérifie si la session autorise la source.
3. Si des paramètres manquent, il pose une question ciblée.
4. Le connecteur MCP récupère les données nécessaires.
5. Un tool local inspecte et normalise l'extrait.
6. Le runtime sauvegarde la table de travail.
7. Le message de sortie cite la source, la période, les variables et les limites.

### Flux Bio-ORACLE

1. L'utilisateur demande un scénario ou une variable Bio-ORACLE.
2. Le modèle vérifie si la session autorise la source.
3. Si des paramètres manquent, il pose une question ciblée.
4. Le connecteur MCP récupère l'extrait ou la grille nécessaire.
5. Un tool local normalise et/ou couple la donnée avec les données locales.
6. Le runtime sauvegarde la table de travail dérivée.
7. Le message de sortie cite la source, le scénario, la période, la zone et les limites.

## Points d'architecture à respecter

- Ne pas hardcoder des identifiants de jeux de données dans le prompt runtime.
- Ne pas supposer une source disponible sans activation explicite.
- Ne pas faire passer un connecteur distant pour un simple outil local.
- Ne pas mélanger la recherche d'accès et le post-traitement local dans un seul outil.
- Ne pas écraser les données brutes lors du couplage.
- Toujours garder une trace de provenance et de couverture.

## Compatibilité avec l'architecture actuelle

Ce plan est compatible avec :

- `core/mcp/manager.py` pour le transport et le cycle de vie ;
- `core/mcp/tools.py` pour l'invocation ;
- `core/tool_registry/` pour les opérations locales ;
- `core/session_store.py` pour l'état actif ;
- `core/instruction_renderer/` pour les instructions de clarification ;
- `core/rag_store.py` pour les règles métier, les limites et les définitions.

Il ne demande pas de casser le runtime IDEA existant.

## Priorisation d'implémentation

### Phase 1

- définir les contrats de paramètres pour OGSL et Bio-ORACLE ;
- figer les règles de clarification ;
- documenter les limites et les formats de sortie.

### Phase 2

- brancher les connecteurs MCP pour l'accès distant ;
- exposer les outils de validation / inspection locale ;
- brancher les artefacts de session pour les tables dérivées.

### Phase 3

- écrire les scénarios de test ;
- vérifier les cas riches, pauvres et ambiguës ;
- vérifier les cas de couplage local ;
- vérifier la traçabilité des sorties.

## Critères d'acceptation

Le plan est considéré prêt à implémenter si :

- une requête OGSL/Bio-ORACLE en langage naturel peut être convertie en paramètres explicites ;
- une info bloquante manquante déclenche une question ciblée ;
- un accès distant est traité via MCP, pas via une fausse abstraction locale ;
- un extrait récupéré est ensuite normalisé localement ;
- la provenance et les limites sont documentées ;
- aucune donnée brute n'est écrasée ;
- aucun secret n'est exposé.

