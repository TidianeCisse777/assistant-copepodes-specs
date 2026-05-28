# Carte de translation des scripts vers tools ou MCP

Objectif: documenter quels scripts d'exploration, de probe et de vérification doivent plus tard devenir des tools IDEA, quels scripts relèvent plutôt d'un connecteur MCP, et quels scripts restent volontairement hors runtime.

Ce document ne décrit pas encore l'implémentation. Il sert de pont entre:

- les scripts de `data_exploration/` et des probes;
- les futurs `tools` dans le runtime IDEA;
- les futurs connecteurs MCP pour les sources externes qui ont une vie propre.

## Règle de classement

### Candidat `tool`

Un script devient plutôt un `tool` si:

- il lit ou transforme des données déjà disponibles localement;
- il inspecte des colonnes, des exports ou des artefacts de session;
- il prépare une table de travail dérivée;
- il n'a pas besoin d'un cycle de vie réseau complexe.

### Candidat `MCP`

Un script devient plutôt un connecteur MCP si:

- il parle à une source externe authentifiée ou à un service distant;
- il nécessite un cycle de vie propre au transport, à la session ou aux credentials;
- il sert surtout à découvrir, exporter ou synchroniser une source distante.

### Reste probe uniquement

Un script peut rester probe uniquement si:

- il sert à prouver un accès;
- il documente une hypothèse;
- il ne vaut pas la peine d'être exposé au runtime utilisateur.

## Hiérarchie de décision

1. D'abord décider si la fonctionnalité doit être disponible dans IDEA runtime.
2. Ensuite décider si elle doit vivre comme `tool` ou comme `MCP`.
3. Ensuite décider si elle doit être un outil générique ou un connecteur spécialisé par source.
4. Enfin décider si le script probe reste conservé comme preuve d'exploration.

## Inventaire courant

### EcoTaxa

| Script | Rôle actuel | Cible future | Type attendu | Notes |
|---|---|---|---|---|
| `data_exploration/ecotaxa_14622_probe/src/export_14622_authenticated.py` | Export authentifié d'un projet EcoTaxa | Export de projet EcoTaxa | MCP ou tool source-specific | Candidat MCP si le transport/auth doit rester séparé du runtime |
| `data_exploration/ecotaxa_14622_probe/src/inspect_14622_export.py` | Inspection d'un export EcoTaxa | Inspection d'export | tool | Lecture locale d'un TSV/ZIP déjà obtenu |
| `data_exploration/ecotaxa_14622_probe/src/get_14622_columns.py` | Extraction de colonnes | Profil de colonnes | tool | Peut devenir un helper de `inspect_export` |
| `data_exploration/ecotaxa_14622_probe/src/classify_14622_columns.py` | Classification de colonnes | Inférence de rôles de colonnes | tool | À aligner avec `infer_column_roles` |
| `data_exploration/ecotaxa_14622_probe/src/profile_14622_export.py` | Profilage de l'export | Profil qualité / couverture | tool | À rapprocher du futur `inspect_file`/`summarize_understanding` |
| `data_exploration/ecotaxa_green_edge_probe/src/export_green_edge_authenticated.py` | Export authentifié GREEN EDGE | Export de projet EcoTaxa | MCP ou tool source-specific | Même logique que ci-dessus |
| `data_exploration/ecotaxa_green_edge_probe/src/inspect_green_edge_export.py` | Inspection d'export GREEN EDGE | Inspection d'export | tool | Local |
| `data_exploration/ecotaxa_loki_probe/src/export_loki_authenticated.py` | Export authentifié LOKI | Export de projet EcoTaxa | MCP ou tool source-specific | Candidat MCP si l'auth reste externe |
| `data_exploration/ecotaxa_loki_probe/src/inspect_loki_export.py` | Inspection d'export LOKI | Inspection d'export | tool | Local |

### EcoPart

| Script | Rôle actuel | Cible future | Type attendu | Notes |
|---|---|---|---|---|
| `data_exploration/ecopart_1165_link_probe/src/export_ecopart_105_authenticated.py` | Export authentifié EcoPart | Export de dataset EcoPart | MCP ou tool source-specific | Si l'accès distant reste contraint, préférer MCP |
| `data_exploration/ecopart_1165_link_probe/src/probe_ecopart_1165_link.py` | Vérification de liaison EcoPart -> EcoTaxa | Résolution de lien / jointure assistée | tool | Peut devenir un outil de validation de jointure |
| `data_exploration/ecopart_1165_link_probe/src/build_depth_enriched_table.py` | Construction de table enrichie par profondeur | Table de travail dérivée | tool | Rentre clairement dans le runtime IDEA |
| `data_exploration/ecopart_1165_link_probe/src/test_minimal_join.py` | Test minimal de jointure | Cas de non-régression | test, pas tool | À garder hors runtime utilisateur |

### Amundsen / CTD

| Script | Rôle actuel | Cible future | Type attendu | Notes |
|---|---|---|---|---|
| `data_exploration/amundsen_data_probe/src/inspect_files.py` | Inspection de fichiers Amundsen | Inspection de source / dataset | tool | Lecture de métadonnées et colonnes |
| `data_exploration/amundsen_data_probe/src/search_catalog.py` | Recherche dans le catalogue | Recherche catalogue | MCP ou tool source-specific | MCP si transport distant et authentifié, sinon tool d'accès |
| `data_exploration/amundsen_data_probe/src/inspect_resources.py` | Inspection des ressources | Découverte des ressources disponibles | MCP ou tool source-specific | Proche d'un connecteur d'annuaire |
| `data_exploration/amundsen_data_probe/src/compare_ecopart_amundsen_ctd.py` | Comparaison EcoPart vs CTD | Couplage / validation de jointure | tool | À rattacher au workflow de jointure et qualité |

### Bio-ORACLE / OGSL

Il n'y a pas encore de script runtime stabilisé dans ce dépôt pour ces sources.

Statut attendu:

- **Bio-ORACLE**: plutôt candidat `MCP` si l'accès distant/interpolation reste externe; les extractions locales de petits échantillons peuvent aussi devenir des `tools` si elles s'opèrent sur des fichiers déjà récupérés.
- **OGSL**: plutôt candidat `MCP` pour la découverte/extraction distante; inspection locale des exports = `tool`.

## Table de décision rapide

| Situation | Cible recommandée |
|---|---|
| Lire un TSV déjà exporté | `tool` |
| Classer des colonnes locales | `tool` |
| Construire une table dérivée | `tool` |
| Exporter depuis une API distante authentifiée | `MCP` ou source-specific connector |
| Découvrir des jeux de données disponibles à distance | `MCP` ou source-specific connector |
| Tester une hypothèse d'accès non destinée au runtime | probe uniquement |

## Intentions utilisateur à supporter explicitement

### OGSL

L'utilisateur doit pouvoir demander, en langage naturel :

- va chercher un profil CTD OGSL pour telle période ;
- va chercher des données OGSL pour telle station / telle zone ;
- va me sortir une série OGSL sur telle variable ;
- prends OGSL comme source environnementale pour tel use case.

Contrat attendu :

- période de début et de fin ;
- variable(s) demandée(s) ;
- zone, station, mission ou profil si pertinent ;
- éventuellement profondeur / couche ciblée ;
- format de sortie local ;
- provenance et limites de couverture.

### Bio-ORACLE

L'utilisateur doit pouvoir demander, en langage naturel :

- va chercher Bio-ORACLE pour telle période / tel scénario ;
- extrais la variable environnementale X sur telle zone ;
- utilise Bio-ORACLE pour enrichir mon jeu de données de zooplancton ;
- compare plusieurs scénarios Bio-ORACLE sur une période donnée.

Contrat attendu :

- variable environnementale ;
- scénario ou modèle si disponible ;
- période future ou historique selon le cas ;
- zone ou coordonnées ;
- résolution / profondeur si nécessaire ;
- méthode de couplage ou d'interpolation ;
- sortie locale traçable.

### Point commun attendu

Pour OGSL comme pour Bio-ORACLE, le runtime ne doit pas faire semblant d'avoir déjà les données si la source n'est pas activée.

Le bon contrat d'interface doit donc permettre :

1. de poser une requête simple en langage naturel ;
2. de convertir cette requête en paramètres explicites ;
3. d'appeler le connecteur distant adéquat ;
4. de récupérer un extrait ou un agrégat local ;
5. de documenter provenance, période, variable, couverture et limites.

## Recommandation d'implémentation future

### OGSL

Préférer un **connecteur MCP** si l'accès s'appuie sur des requêtes distantes ou un catalogue de profils qui évolue.

Préférer un **tool local** seulement si la donnée est déjà matérialisée dans un fichier ou une table dérivée.

### Bio-ORACLE

Préférer un **connecteur MCP** pour la découverte et l'extraction distantes.

Réserver le **tool local** aux opérations post-récupération :

- inspection ;
- filtrage ;
- agrégation ;
- normalisation ;
- export de table de travail.

## Ce qu'il faut faire avant l'implémentation

Avant de convertir un script en tool ou MCP:

1. Vérifier si le besoin existe dans le runtime IDEA ou seulement dans la phase de recherche.
2. Vérifier si le script manipule des données locales ou une source distante.
3. Décider si la logique appartient à un outil générique ou à un connecteur source-specific.
4. Définir les entrées, sorties et effets de bord.
5. Définir le statut de sécurité et d'authentification.
6. Laisser le script probe dans `data_exploration/` s'il sert de preuve technique.

## Notes de gouvernance

- Ce document ne remplace pas `TOOLS_SPEC.js`.
- Ce document ne remplace pas `PLAN.md`.
- Ce document ne remplace pas le corpus RAG.
- Les noms de tools et de connecteurs listés ici sont des cibles provisoires à valider avant implémentation.
