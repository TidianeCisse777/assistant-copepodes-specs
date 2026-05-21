# Amundsen Science data probe

Mini-projet pour explorer les donnees publiques Amundsen Science, en priorite CTD-Rosette.

Objectif : voir les formats reels, les colonnes/variables disponibles, et les cles utiles pour relier les donnees environnementales aux donnees EcoTaxa/EcoPart Amundsen.

## Installation

```bash
cd amundsen_data_probe
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execution

```bash
python src/search_catalog.py
python src/inspect_resources.py
python src/inspect_files.py
python src/compare_ecopart_amundsen_ctd.py
```

## Contraintes

- Lecture seule.
- Maximum 3 datasets retenus.
- Maximum 1 petit fichier inspecte par dataset.
- Si fichier trop gros : HEAD + metadonnees seulement.
- Les reponses utiles sont sauvegardees dans `outputs/raw/`.

## Sortie principale

```text
outputs/report.md
outputs/report_ecopart_amundsen_compare.md
```

Le rapport indique :

- datasets trouves ;
- acces direct ou on-demand ;
- formats disponibles ;
- colonnes/variables detectees ;
- cles de liaison : `cast_id`, `event_id`, `station`, `date_time`, `lat/lon`, `depth` ;
- variables environnementales : temperature, salinite/conductivite, oxygene, fluorescence.
