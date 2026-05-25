# Assistant copépodes — specs, RAG et exploration de données

Ce dépôt documente et prépare un assistant scientifique pour produire des graphiques à partir de données de copépodes marins.

Il ne contient pas le runtime applicatif principal. Le runtime cible est le projet IDEA, dans un dépôt séparé. Ici, on trouve les specs métier, les documents RAG, les scénarios de validation, les définitions de tools et les scripts d'exploration qui prouvent comment accéder aux sources EcoTaxa, EcoPart et CTD.

## À quoi sert ce repo ?

Le but est de transformer un besoin de recherche en système implémentable :

```text
chercheur NeoLab
→ question ou besoin de graphique
→ specs de comportement agent
→ documents RAG fiables
→ tools de données à implémenter dans IDEA
→ graphiques reproductibles, sans interprétation scientifique automatique
```

L'assistant cible doit aider à inspecter des fichiers, identifier les colonnes utiles, vérifier les sources, préparer des jointures, générer des graphiques et documenter les limites techniques. Il ne doit pas interpréter biologiquement les résultats : l'interprétation reste au chercheur.

## Critères de réussite du dépôt

Une personne qui ne connaît pas le projet doit pouvoir :

1. comprendre le problème scientifique et le périmètre de l'assistant ;
2. trouver les specs complètes : use cases, capacités, contraintes ;
3. comprendre le rôle des documents RAG et des colonnes de données ;
4. savoir quelles sources ont été explorées et comment les exports ont été obtenus ;
5. comprendre l'architecture cible avec IDEA ;
6. identifier ce qui est prêt, ce qui est expérimental et ce qui ne doit pas être commité ;
7. reprendre l'implémentation dans IDEA sans deviner les règles métier.

## Lire dans cet ordre

| Étape | Fichier | Pourquoi |
|---|---|---|
| 1 | [docs/REPO_GUIDE.md](docs/REPO_GUIDE.md) | Vue d'ensemble pour nouvel arrivant |
| 2 | [docs/FOLDER_MAP.md](docs/FOLDER_MAP.md) | Rôle de chaque dossier et fichier majeur |
| 3 | [docs/DOCUMENTATION_STATUS.md](docs/DOCUMENTATION_STATUS.md) | Ce qui est à jour et ce qui reste historique |
| 4 | [docs/CONTEXT.md](docs/CONTEXT.md) | Glossaire métier et règles de comportement |
| 5 | [PLAN.md](PLAN.md) | Plan d'implémentation consolidé dans IDEA |
| 6 | [TOOLS_SPEC.js](TOOLS_SPEC.js) | Spécification des tools à implémenter |
| 7 | [TEST_SCENARIOS.md](TEST_SCENARIOS.md) | Scénarios de validation comportementale |
| 8 | [STAGE ULAVAL/Agent/Ressources scientifiques/Document RAG](STAGE%20ULAVAL/Agent/Ressources%20scientifiques/Document%20RAG) | Corpus RAG copépodes |

## Structure courte

```text
.
├── README.md                         point d'entrée
├── CLAUDE.md                         consignes agent/Codex pour ce repo
├── PLAN.md                           plan d'implémentation cible dans IDEA
├── ARCHITECTURE.md                   diagrammes Mermaid de l'architecture cible
├── TOOLS_SPEC.js                     contrats des tools copépodes
├── TEST_SCENARIOS.md                 scénarios de validation
├── docs/                             guide repo, contexte, ADR, accès données
├── STAGE ULAVAL/                     specs métier et documents RAG sources
├── data_exploration/                 probes API et fixtures TSV
├── visualization/                    visualisation D3 des specs
└── polar_data_tools/                 package placeholder, non implémenté
```

## Données et secrets

- Les fichiers `.env`, tokens, mots de passe et exports bruts complets ne doivent pas être commités.
- Les scripts d'exploration peuvent régénérer les exports avec des credentials locaux.
- Les fichiers partageables sont les fixtures légères dans `data_exploration/examples_tsv/` et les rapports/documentations dérivés.
- Les gros TSV/ZIP restent locaux et doivent être ignorés par git.

## Commandes utiles

Visualisation des specs :

```bash
cd visualization
python3 -m http.server 8080
```

Exporter un projet EcoTaxa authentifié, exemple probe GREEN EDGE :

```bash
cd data_exploration/ecotaxa_green_edge_probe
python src/export_green_edge_authenticated.py --with-images none --statusfilter V
```

Explorer les sources Amundsen :

```bash
cd data_exploration/amundsen_data_probe
python src/search_catalog.py
python src/inspect_resources.py
python src/inspect_files.py
```

Tester la liaison EcoPart/EcoTaxa existante :

```bash
cd data_exploration/ecopart_1165_link_probe
python src/probe_ecopart_1165_link.py
python src/test_minimal_join.py
```

## État actuel

Le dépôt est une base de specs et de preuves d'accès aux données. Les documents RAG et les scénarios sont suffisamment structurés pour démarrer l'implémentation dans IDEA. Les tools ne sont pas encore le runtime final ici : ils sont spécifiés pour être codés dans le dépôt IDEA.
