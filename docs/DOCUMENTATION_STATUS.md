# Statut de la documentation

Ce fichier garde la trace de ce qui est à jour, de ce qui est volontairement historique, et de ce qui reste à réviser.

## À jour pour l'onboarding

- `README.md` : point d'entrée et ordre de lecture.
- `docs/REPO_GUIDE.md` : vue d'ensemble produit et critères de réussite.
- `docs/FOLDER_MAP.md` : rôle des dossiers et règles de commit.
- `data_exploration/README.md` : règles des probes, credentials et outputs.
- `STAGE ULAVAL/README.md` : rôle du corpus métier.

## À jour pour le RAG

- `colonnes_sources.md` : généralisé, sans dépendance à un projet spécifique.
- `colonnes_instruments.md` : généralisé, avec mots-clés par chunk.
- `sources_en_ligne.md` : aligné sur les sources autorisées actuelles.

## Décisions actuelles

- Le runtime cible est IDEA.
- Les sources autorisées dans le prompt cible sont EcoTaxa, EcoPart, CTD externe, OGSL, Bio-ORACLE et fichiers labo.
- OBIS et CMEMS ne sont pas des sources autorisées dans le prompt cible actuel.
- Les IDs de projets dans les probes sont des exemples d'exploration, pas des constantes système.
- L'assistant produit des graphiques et métadonnées techniques, pas d'interprétation scientifique.

## Dette documentaire connue

- Certains use cases et anciennes notes peuvent encore porter des libellés historiques.
- Les noms `Assistant scientifique` et `Assistant graphique` coexistent ; `Assistant graphique copépodes` est le nom cible pour le comportement runtime.
- `TOOLS_SPEC.js` reste une spécification de transition : toute source historique doit rester cohérente avec `sources_en_ligne.md` avant implémentation.
- Les documents Word/PDF générés doivent préciser leur source Markdown ou leur commande de génération avant d'être traités comme source de vérité.
