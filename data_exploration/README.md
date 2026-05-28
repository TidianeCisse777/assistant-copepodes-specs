# Exploration de données

Ce dossier contient les probes qui ont permis de comprendre les sources EcoTaxa, EcoPart et CTD avant l'implémentation des tools dans IDEA.

Les probes sont des preuves de méthode. Ils ne sont pas encore l'API finale de l'assistant.

## Règles de sécurité

À ne jamais commiter :

- `.env` ;
- tokens, mots de passe, cookies ou JWT ;
- ZIP d'export complets ;
- TSV/CSV complets lourds ;
- `outputs/raw/` ;
- caches Python.

À commiter :

- scripts `src/*.py` ;
- `.env.example` ;
- `requirements.txt` ;
- rapports Markdown légers ;
- dictionnaires de colonnes ;
- fixtures TSV courtes dans `examples_tsv/`.

## Dossiers

| Dossier | Rôle |
|---|---|
| `examples_tsv/` | Fixtures légères utilisées pour tests et documentation |
| `ecotaxa_loki_probe/` | Export et inspection EcoTaxa authentifié pour un projet LOKI |
| `ecotaxa_green_edge_probe/` | Export et inspection EcoTaxa authentifié pour un projet UVP5 |
| `ecopart_1165_link_probe/` | Exploration EcoPart et jointure EcoTaxa/EcoPart |
| `amundsen_data_probe/` | Exploration catalogue, ERDDAP et CTD externe |
| `bio_oracle_probe/` | Extrait Bio-ORACLE public minimal pour tests environnementaux |
| `ogsl_probe/` | Extrait OGSL CTD public minimal pour tests de contexte régional |

## Documentation utile

- [`copepod_jointure_hierarchy.md`](./copepod_jointure_hierarchy.md) : hiérarchie des jointures et couplages entre données labo, EcoTaxa, EcoPart, Amundsen CTD, OGSL et Bio-ORACLE.
- [`IMPLEMENTATION_PLAN_OGSL_BIO_ORACLE.md`](./IMPLEMENTATION_PLAN_OGSL_BIO_ORACLE.md) : plan d'implémentation des connecteurs et tools OGSL / Bio-ORACLE.

## Credentials

Chaque probe authentifié utilise un `.env` local, créé depuis `.env.example`.

Exemple :

```env
ECOTAXA_USERNAME=
ECOTAXA_PASSWORD=
ECOTAXA_TOKEN=
```

Le token est optionnel. Si `ECOTAXA_USERNAME` et `ECOTAXA_PASSWORD` sont fournis, le script peut obtenir un JWT en mémoire sans l'écrire dans le fichier `.env`.

## Probes EcoTaxa

Structure typique :

```text
probe/
├── .env.example
├── .gitignore
├── requirements.txt
├── src/
│   ├── export_*_authenticated.py
│   └── inspect_*_export.py
└── outputs/
    ├── report.md
    ├── column_null_profile.md
    ├── columns_by_category.md
    ├── clean/
    └── raw/              # ignoré
```

Les exports complets sont régénérables et restent locaux. Les rapports et dictionnaires dérivés peuvent être commités s'ils aident à concevoir les tools.

## Fixtures TSV

`examples_tsv/` contient des extraits courts pour :

- inspection de colonnes EcoTaxa ;
- preview de jointure EcoTaxa/EcoPart ;
- particules et profils EcoPart ;
- CTD externe ;
- comparaison EcoPart/CTD.

Ces fixtures sont les données de référence pour les premiers tests unitaires des tools.

## Passage vers IDEA

Les scripts de ce dossier servent à définir les futurs tools :

- `data.inspect` ;
- `data.validate` ;
- `columns.describe` ;
- `sources.query_ecotaxa` ;
- `sources.query_ecopart` ;
- `sources.query_amundsen_ctd` ;
- `joins.execute`.

Avant de transformer un probe en tool, vérifier :

1. absence de credential dans les logs et retours ;
2. paramètres source dynamiques, jamais hardcodés dans le runtime ;
3. sauvegarde des données dérivées sans modification du brut ;
4. retour structuré testable ;
5. gestion claire des erreurs API et des jobs async.
