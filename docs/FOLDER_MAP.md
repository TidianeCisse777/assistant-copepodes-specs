# Carte des dossiers

Cette carte explique pourquoi chaque dossier existe et comment il s'insère dans le projet.

## Racine

| Chemin | Rôle | Pourquoi il existe |
|---|---|---|
| `README.md` | Point d'entrée du repo | Donner le contexte à une personne qui arrive sans historique |
| `CLAUDE.md` | Instructions de travail pour agents Codex/Claude | Fixe le sprint actif, les fichiers de référence et les règles TDD/credentials |
| `PLAN.md` | Plan d'implémentation consolidé | Sert de référence unique pour la cible IDEA |
| `ARCHITECTURE.md` | Diagrammes de l'architecture cible | Visualise le flux utilisateur, prompt stack, sources et modes |
| `TOOLS_SPEC.js` | Spécification des tools | Définit signatures, contraintes et tests attendus des tools copépodes |
| `TEST_SCENARIOS.md` | Scénarios comportementaux | Vérifie que l'agent se comporte comme attendu en cas nominal et cas limite |
| `uv.lock` | Lockfile Python/UV | Trace l'environnement potentiel, même si le runtime final est ailleurs |
| `mermaid-filter.err` | Fichier local d'erreur Mermaid | Artefact non lié, ne devrait pas être commité |

## `docs/`

Documentation transversale qui rend le repo compréhensible et maintenable.

| Chemin | Rôle |
|---|---|
| `docs/REPO_GUIDE.md` | Vue d'ensemble produit, périmètre, réussite et workflow |
| `docs/FOLDER_MAP.md` | Carte des dossiers et fichiers |
| `docs/DOCUMENTATION_STATUS.md` | Statut de la documentation et dette connue |
| `docs/CONTEXT.md` | Glossaire métier et règles de comportement agent |
| `docs/DATA_ACCESS_METHODS.md` | Méthodes d'accès EcoTaxa/EcoPart/CTD et probes associés |
| `docs/PRD_IDEA_copepod.md` | PRD produit pour l'adaptation IDEA |
| `docs/PRD_IDEA_copepod.docx` | Version Word du PRD |
| `docs/adr/` | Décisions d'architecture |
| `docs/architecture/` | Documents de traçabilité et architecture détaillée |

Ce dossier doit rester lisible par un humain. Les documents générés lourds ou binaires ne doivent être ajoutés que s'ils sont explicitement utiles.

## `STAGE ULAVAL/`

Dossier de référence métier issu du stage et des specs validées.

| Sous-dossier | Rôle |
|---|---|
| `STAGE ULAVAL/USE CASE/` | Use cases complets de l'assistant |
| `STAGE ULAVAL/Agent/Spec de L'agent/` | Capacités et contraintes agent |
| `STAGE ULAVAL/Agent/Ressources scientifiques/Document RAG/` | Corpus RAG source |
| `STAGE ULAVAL/ANALYSE EXIGENCE/` | Espace d'analyse d'exigences, s'il est présent localement |
| `STAGE ULAVAL/Analyse sur les données/` | Espace d'analyse de données, s'il est présent localement |

### Documents RAG

| Fichier | Pourquoi il existe |
|---|---|
| `colonnes_sources.md` | Expliquer sources, schémas, jointures et pièges EcoTaxa/EcoPart/CTD |
| `colonnes_instruments.md` | Définir les colonnes par instrument et les règles de nettoyage |
| `copepodes_domaine.md` | Définir le périmètre taxonomique et les avertissements d'identification |
| `methodes_calcul.md` | Décrire formules, unités, variables dérivées et limites |
| `sources_en_ligne.md` | Décrire les sources externes et conditions d'accès |

Ces fichiers sont optimisés pour le RAG : chunks séparés par `---`, titres-question, mots-clés, tableaux courts et règles explicites.

## `data_exploration/`

Scripts d'exploration et preuves d'accès aux données. Ce dossier sert à apprendre comment les sources fonctionnent avant d'implémenter des tools propres dans IDEA.

| Sous-dossier | Rôle | À commiter |
|---|---|---|
| `examples_tsv/` | Fixtures TSV légères et partageables | Oui |
| `ecotaxa_loki_probe/` | Export/inspection EcoTaxa authentifié pour un projet LOKI | Scripts, `.env.example`, rapports légers |
| `ecotaxa_green_edge_probe/` | Export/inspection EcoTaxa authentifié pour un projet UVP5 | Scripts, `.env.example`, rapports et dictionnaires légers |
| `ecopart_1165_link_probe/` | Exploration EcoPart et jointure avec EcoTaxa | Scripts, rapports légers |
| `amundsen_data_probe/` | Exploration catalogue/ERDDAP CTD externe | Scripts, rapports légers |

À ne pas commiter :

- `.env`
- tokens ou mots de passe
- exports ZIP complets
- réponses API brutes volumineuses
- TSV complets lourds
- caches Python

## `data_exploration/examples_tsv/`

Fixtures légères utilisées pour tests, documentation et futures implémentations.

Elles prouvent les formats sans exposer ou versionner les exports complets. Elles doivent rester petites, anonymisées si nécessaire, et directement exploitables par des tests.

## Probes EcoTaxa

Les dossiers `ecotaxa_*_probe/` contiennent généralement :

| Chemin | Rôle |
|---|---|
| `.env.example` | Modèle de credentials locaux |
| `.gitignore` | Protection contre secrets et exports lourds |
| `requirements.txt` | Dépendances minimales du probe |
| `src/export_*_authenticated.py` | Lance un export API authentifié |
| `src/inspect_*_export.py` | Inspecte ZIP/TSV exporté et produit colonnes/preview/rapport |
| `outputs/report.md` | Résumé léger commitable |
| `outputs/clean/*.md|*.json` | Dictionnaires et profils committables |

Ces probes sont des preuves de méthode. Le code final doit être transformé en tools robustes dans IDEA.

## `visualization/`

Visualisation D3.js des specs.

| Fichier | Rôle |
|---|---|
| `index.html` | Interface D3 |
| `data.js` | Données de l'arbre : use cases, capacités, contraintes, RAG |
| `notes.js` | Notes de révision |
| `README.md` | Mode d'emploi de la visualisation |

Lancer localement :

```bash
cd visualization
python3 -m http.server 8080
```

La visualisation reflète les specs. Elle ne doit pas devenir la source de vérité.

## `polar_data_tools/`

Package placeholder. Il signale une intention de factoriser des outils Python, mais l'architecture active cible plutôt l'intégration dans IDEA.

Ne pas supposer que ce dossier contient le runtime final tant qu'il n'est pas explicitement développé.

## `.claude/`

Configuration et worktrees d'agents.

| Chemin | Rôle |
|---|---|
| `.claude/settings.json` | Configuration agent partagée |
| `.claude/settings.local.json` | Configuration locale |
| `.claude/worktrees/` | Worktrees d'agents, historiques ou temporaires |

Ces dossiers peuvent contenir du contexte utile, mais ils ne sont pas la source documentaire principale du projet.

## `.git/`, `.venv/`, caches et artefacts locaux

Ces dossiers sont techniques ou locaux :

- `.git/` : historique Git ;
- `.venv/` : environnement Python local ;
- `__pycache__/`, `.pytest_cache/` : caches ;
- `.DS_Store` : artefact macOS ;
- `outputs/raw/` : données brutes régénérables ;
- `*.zip` : exports lourds ou archives.

Ils ne doivent pas guider la compréhension métier du repo et ne doivent pas être ajoutés volontairement aux commits.
