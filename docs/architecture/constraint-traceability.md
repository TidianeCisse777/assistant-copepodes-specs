# Traçabilité des contraintes agent

## Objectif

Rendre vérifiable chaque contrainte `CT-AG-*`.

Une contrainte ne doit pas être considérée comme couverte simplement parce qu'elle est mentionnée dans un prompt. Elle doit avoir :

- un point d'application ;
- un mécanisme de vérification ;
- un test ou une preuve observable.

## Types de points d'application

| Type | Rôle |
|---|---|
| `system_prompt` | Règle globale non négociable |
| `mode_prompt` | Règle dépendante du Mode Plan, Mode Analyse ou Mode En Ligne |
| `tool` | Validation exécutable dans une fonction |
| `rag` | Connaissance documentaire ou citation |
| `ui` | Contrainte d'interface ou workflow utilisateur |
| `runtime` | Configuration modèle, session, logs, jobs, streaming |
| `test` | Test automatisé ou scénario comportemental |

## Statuts

| Statut | Sens |
|---|---|
| `covered` | Vérifiable maintenant |
| `partial` | Règle présente mais vérification incomplète |
| `planned` | Emplacement décidé, pas encore implémenté |
| `blocked` | Dépend d'une décision ou d'un composant absent |
| `revised` | La contrainte V1 doit être adaptée à la décision actuelle |

## Matrice initiale

| ID | Résumé | Application cible | Vérification cible | Statut |
|---|---|---|---|---|
| CT-AG-01 | Toujours citer les sources utilisées | `system_prompt`, `plot.generate`, `deliverable.build` | Test graphique/livrable sans source refusé ou incomplet | partial |
| CT-AG-02 | Ne pas inventer données absentes | `system_prompt`, tools de calcul/colonnes | Tests colonnes/valeurs absentes | partial |
| CT-AG-03 | Distinguer fiable/exploratoire/impossible | `system_prompt`, `mode_prompt`, `plot.plan`, `plot.generate` | Test prompt + statut de fiabilité dans plan ou métadonnées | partial |
| CT-AG-04 | Exiger contexte avant analyse | `mode_prompt`, UI Mode Plan | Test blocage contexte incomplet | partial |
| CT-AG-05 | Valider colonnes/unités avant calcul | `tool`, `plot.plan`, `calc.execute` | Tests colonnes manquantes/unités absentes | partial |
| CT-AG-06 | Soumettre méthode avant exécution | `system_prompt`, `mode_prompt` Plan | Test prompt + plan avant génération | partial |
| CT-AG-07 | Tracer les jointures | `joins.plan`, `joins.execute`, métadonnées | Test métadonnées de jointure | partial |
| CT-AG-08 | Respecter limites des sources | `system_prompt`, RAG, tools sources | Tests source sollicitée hors capacité | partial |
| CT-AG-09 | Encadrer exécution de code | `system_prompt`, runtime OpenInterpreter | Test prompt + comportement erreur visible | partial |
| CT-AG-10 | Préserver données brutes | `system_prompt`, tools data/joins/calc | Test copie/table dérivée, brut inchangé | partial |
| CT-AG-11 | Gérer credentials | `system_prompt`, tools sources, logs | Tests absence secrets dans sortie/logs | partial |
| CT-AG-12 | Limiter téléchargements | `system_prompt`, `mode_prompt`, tools sources | Test prompt + demande validation avant gros téléchargement | partial |
| CT-AG-13 | Ne pas surinterpréter | `system_prompt`, livrables | Test refus interprétation | covered |
| CT-AG-14 | Graphiques lisibles et sourcés | `system_prompt`, `plot.generate` | Test titre/axes/unités/source/limites | partial |
| CT-AG-15 | Livrables sans citations inventées | `system_prompt`, RAG, `deliverable.build` | Test citations subset RAG/métadonnées | partial |
| CT-AG-16 | Respecter périmètre V1 | `system_prompt`, mode prompts | Test hors périmètre refuse ou marque V2 | partial |
| CT-AG-17 | Paramètres modèle stables | `runtime` LiteLLM/config | Test/config review paramètres modèle | planned |
| CT-AG-18 | Réduire narration | `system_prompt`, templates réponse | Snapshot sorties courtes structurées | partial |
| CT-AG-19 | Ancrer dans données/RAG | `system_prompt`, RAG/tools | Test aucune preuve -> blocage | partial |
| CT-AG-20 | Tracer chaque segment | `system_prompt`, tools, livrables, métadonnées | Test prompt + provenance par segment | partial |
| CT-AG-21 | Vérifier cohérence sortie/données | `system_prompt`, tools génération/livrable | Test prompt + assertions post-génération | partial |
| CT-AG-22 | Analyses lourdes en jobs | `runtime`, UI/backend | Test job/status pour analyse lourde | planned |
| CT-AG-23 | Séparer cadrage et analyse | UI, mode prompts | Test Mode Plan sans exécution, Mode Analyse structuré | planned |
| CT-AG-24 | Pas de streaming dans rapports | UI/runtime report renderer | Test rapport affiché en bloc | planned |
| CT-AG-25 | Ticket d'entrée cognitif | UI Mode Plan, mode prompt | Test demande vague bloquée | planned |
| CT-AG-26 | Vocabulaire clinique | `system_prompt`, templates | Test prompt + snapshot sans anthropomorphisme | partial |
| CT-AG-27 | Incertitude visible | `plot.generate`, templates | Test limites/validation visuellement signalées | partial |
| CT-AG-28 | Livrables pour révision humaine | `system_prompt`, `deliverable.build` | Test review_flags et absence prêt-à-publier | partial |
| CT-AG-29 | Contextualiser absences | `system_prompt`, tools couverture, RAG, livrable | revised : absence locale ≠ absence biologique, retirer OBIS, adapter OGSL/Bio-ORACLE/RAG | partial |

## Règle de progression

Pour passer une contrainte de `partial` à `covered`, il faut au minimum :

1. une règle dans le bon point d'application ;
2. un test automatisé ou scénario comportemental ;
3. une sortie observable qui prouve la règle.

Exemple :

```text
CT-AG-14
Application : plot.generate
Test : graphique généré sans unité -> erreur ou statut incomplete
Preuve : métadonnées contiennent title, axes, units, source, filters, limitations
```

## Contraintes Verrouillées Dans Le System Prompt

Ces contraintes sont maintenant présentes dans le system prompt et testées structurellement côté IDEA. Elles restent `partial` quand une vérification comportementale, un tool ou une sortie observable est encore nécessaire.

- CT-AG-03 : fiable / exploratoire / impossible.
- CT-AG-06 : plan ou méthode avant exécution.
- CT-AG-12 : pas de téléchargement massif sans validation.
- CT-AG-18 et CT-AG-26 : ton sobre, clinique, non anthropomorphique.
- CT-AG-20 : principe de provenance.
- CT-AG-21 : vérifier cohérence sortie/données.
- CT-AG-29 révisée : absence locale ne prouve jamais une absence biologique.

## Décisions CONTEXT / Grill

Ces règles viennent du travail de cadrage dans `docs/CONTEXT.md`. Elles complètent les contraintes V1 et doivent aussi rester vérifiables.

| ID | Décision | Application cible | Vérification cible | Statut |
|---|---|---|---|---|
| CTX-01 | Nom canonique : Assistant graphique copépodes | `system_prompt`, UI, docs | Test prompt contient le nom anglais/canonique | partial |
| CTX-02 | IDEA est le runtime, pas l'identité métier | `system_prompt`, `CopepodProfile` | Test prompt garde OpenInterpreter mais remplace géoscience/SEA | partial |
| CTX-03 | System prompt rédigé en anglais | `system_prompt` | Test ou revue prompt en anglais | covered |
| CTX-04 | Réponses dans la langue utilisateur, français si ambigu | `system_prompt`, tests comportementaux | Scénario fr/en | partial |
| CTX-05 | Pas de limite artificielle de 500 tokens | tests prompt | Absence de test limite 500 tokens | covered |
| CTX-06 | Prompt inspiré de SEA mais domaine sea-level supprimé | `system_prompt` | Test headings SEA-like + termes sea-level absents | covered |
| CTX-07 | Sources autorisées : EcoTaxa, EcoPart, Amundsen CTD, données labo, OGSL, Bio-ORACLE | `system_prompt`, Mode En Ligne | Test prompt + mode sources | partial |
| CTX-08 | OBIS supprimé du prompt cible | `system_prompt`, RAG à réviser | Test OBIS non autorisé | covered |
| CTX-09 | Mode En Ligne activé par source | mode prompt, session state, UI | Test source non activée bloque requête | planned |
| CTX-10 | Source non chargée/activée : signaler les données manquantes | mode prompt, tools | Test demande source absente -> blocage | partial |
| CTX-11 | Amundsen CTD prioritaire sur OGSL si les deux couvrent le même besoin | mode prompt, source selection tool | Test sélection source | partial |
| CTX-12 | OGSL source régionale du golfe du Saint-Laurent, avec métadonnées obligatoires | RAG, source tool, métadonnées | Test métadonnées OGSL | planned |
| CTX-13 | Bio-ORACLE source environnementale/future, ne valide pas les taxons | `system_prompt`, source tool | Test prompt + scénario taxon via Bio-ORACLE refusé | partial |
| CTX-14 | Métadonnées Bio-ORACLE obligatoires : variable, scénario/modèle, période, zone, extraction/interpolation, source | source tool, graph metadata | Test graph Bio-ORACLE sans scénario/période incomplet | planned |
| CTX-15 | Mode Analyse utilise des colonnes déjà identifiées | mode prompt, session state | Test Mode Analyse sans colonnes -> blocage | planned |
| CTX-16 | Étape de planification graphique verrouille contexte, qualité, langage, format, artefacts | `system_prompt`, mode prompt Plan | Test prompt + plan contient champs obligatoires | partial |
| CTX-17 | Python/R choisi dans la planification graphique | mode prompt Plan, graph execution | Test plan exige langage | partial |
| CTX-18 | JavaScript/D3 seulement si demandé ou nécessaire au livrable | mode prompt, graph tool | Test défaut Python/R | planned |
| CTX-19 | Graphiques statiques par défaut, interactifs seulement si demandé/nécessaire | `system_prompt`, graph tool | Test défaut format statique | partial |
| CTX-20 | Tout graphique sauvegardé comme artefact | `system_prompt`, graph tool | Test fichier artefact existe | partial |
| CTX-21 | Table couplée sauvegardée quand plusieurs sources sont combinées | `system_prompt`, join/graph tool | Test prompt + table dérivée sauvegardée | partial |
| CTX-22 | Tableaux autorisés seulement comme support technique du graphique/livrable | `system_prompt`, templates | Test demande tableau interprétatif refusée ou recadrée | partial |
| CTX-23 | Titres/légendes descriptifs, non interprétatifs, avec noms scientifiques si disponibles | graph tool, templates | Test titre sans conclusion biologique | partial |
| CTX-24 | Style graphique simple, lisible, scientifique | graph tool | Test métadonnées/figure minimale | partial |
| CTX-25 | Validation humaine EcoTaxa : si statut absent/non confirmé, demander inclure/exclure avant graphique/calcul taxonomique | mode prompt, data/plot tool | Test validation inconnue -> question | partial |
| CTX-26 | Données taxonomiques non confirmées incluses : signaler limite technique | graph metadata, deliverable | Test limite présente | partial |
| CTX-27 | Réponses de domaine autorisées uniquement pour planifier ou documenter techniquement un graphique | `system_prompt`, tests comportementaux | Test question biologique autonome refusée/recadrée | partial |
| CTX-28 | Livrables techniques autorisés pour révision humaine, pas rapport interprétatif final | `system_prompt`, deliverable tool | Test livrable sans discussion/conclusion | partial |
| CTX-29 | Formats standards : graphique produit, blocage, refus d'interprétation | templates, mode prompts | Snapshot sorties | planned |
| CTX-30 | CopepodProfile garde temporairement blocs génériques au premier incrément | `CopepodProfile`, tests | Test instruction_blocks actuels | covered |
| CTX-31 | CopepodProfile exclut tags station/climate | `CopepodProfile`, tests | Test `tool_tags == {"core","rag","mcp"}` | covered |
| CTX-32 | Les signatures détaillées des tools ne sont pas dupliquées dans le system prompt | prompt review, tests | Test absence signatures longues ou duplication | planned |
| CTX-33 | Les project IDs EcoTaxa/EcoPart ne sont pas hardcodés ; sources découvertes dynamiquement | source tools, docs | Test pas de constante 1165/2331/105 dans système | planned |

## Couverture Globale Actuelle

| Ensemble | Couverture |
|---|---|
| Contraintes V1 `CT-AG-01` à `CT-AG-29` | Exhaustive dans la matrice, couverture variable |
| Décisions `CONTEXT.md` / grill-with-docs | Tracées par `CTX-01` à `CTX-33` |
| System prompt actuel | Couvre une partie des contraintes constitutionnelles |
| Modes / tools / RAG / UI | Encore nécessaires pour rendre la majorité des règles vérifiables |
