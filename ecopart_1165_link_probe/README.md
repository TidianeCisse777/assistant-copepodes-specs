# EcoPart / EcoTaxa 1165 link probe

Probe en lecture seule pour tester si le projet EcoTaxa `1165` (`UVP5 IPS Amundsen 2018`) est déjà lié à EcoPart.

Objectif : vérifier la liaison avant de coder une jointure.

## Installation

```bash
cd ecopart_1165_link_probe
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Exécution

```bash
python src/probe_ecopart_1165_link.py
python src/build_depth_enriched_table.py
```

## Sorties

- `outputs/report_ecopart_link.md` : conclusion sur la liaison EcoPart 105 vers EcoTaxa 1165.
- `outputs/report_join_test.md` : test minimal de jointure via `profile_id`.
- `outputs/report_depth_enriched_table.md` : test de jointure `profile_id + profondeur la plus proche`.
- `outputs/report_ecopart_export.md` : résumé de l'export EcoPart authentifié.

Les réponses HTML/API et exports complets sont générés dans `outputs/raw/` quand les scripts sont lancés. Ce dossier est ignoré par git.

Extraits conservés dans `../examples_tsv/` :

- `uvp_amundsen_1165_ecotaxa_object_sample.tsv` : objets EcoTaxa avec taxonomie et morphométrie.
- `uvp_amundsen_105_ecopart_particles_reduced.tsv` : CTD + particules agrégées par profil/profondeur.
- `uvp_amundsen_1165_105_join_preview.tsv` : aperçu de jointure `profile_id`.
- `uvp_amundsen_1165_105_enriched_nearest_depth.tsv` : table objet enrichie avec profondeur EcoPart la plus proche.

Résultat validé : EcoPart `105` est explicitement lié à EcoTaxa `1165`. La jointure fiable commence par `profile_id`, puis doit être affinée avec la profondeur pour associer les CTD/particules aux objets individuels.
