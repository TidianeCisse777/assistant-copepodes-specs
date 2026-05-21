# EcoTaxa LOKI authenticated export

Export authentifié du projet EcoTaxa `2331` : `LOKI - copepod lipids`.

Le flux final :

1. se connecte à EcoTaxa avec un compte ayant accès au projet ;
2. lance `/api/object_set/export/general` ;
3. attend le job EcoTaxa ;
4. télécharge `/api/jobs/{job_id}/file` ;
5. inspecte le ZIP/TSV et liste les colonnes.

## Installation

```bash
cd ecotaxa_loki_probe
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Créer `.env` à partir de `.env.example`, puis remplir localement les identifiants. Le fichier `.env` est ignoré par git.

```bash
cp .env.example .env
```

Variables supportées :

```env
ECOTAXA_USERNAME=
ECOTAXA_PASSWORD=
ECOTAXA_TOKEN=
```

`ECOTAXA_TOKEN` est optionnel. S'il est présent, il remplace le login username/password.

## Export

```bash
python src/export_loki_authenticated.py
```

Options utiles :

```bash
python src/export_loki_authenticated.py --with-images none
python src/export_loki_authenticated.py --job-id 232296
```

## Inspection seule

```bash
python src/inspect_loki_export.py outputs/raw/ecotaxa_loki_2331_export_job_232296.zip
```

## Sorties

Les exports complets sont générés dans `outputs/raw/` quand le script est lancé. Ce dossier est ignoré par git pour éviter de conserver les gros fichiers et les réponses intermédiaires.

Artefacts conservés dans le dépôt nettoyé :

- `outputs/report.md` : conclusion du test LOKI.
- `../examples_tsv/loki_2331_ecotaxa_export_sample_50.tsv` : extrait léger du TSV exporté.

Résultat validé : l'export authentifié fonctionne, mais ce projet fournit surtout taxonomie, annotations, stade/orientation. Il ne fournit pas directement des mesures individuelles de poids, lipides ou biomasse.
