# Validation rédactionnelle — Capacités agent V1

Objectif : figer la rédaction des capacités agent avant implémentation.

Cette validation porte sur :

- clarté ;
- non-ambiguïté ;
- non-contradiction avec les use cases ;
- cohérence avec les contraintes agent ;
- traçabilité entre capacités agent et use cases client.

Elle ne valide pas encore le fonctionnement réel du système.

---

## Definition of Done rédactionnelle d'une capacité agent

Une capacité agent V1 est considérée prête si :

- elle référence les bons use cases `UC-SL-*` ;
- elle décrit un comportement observable de l'agent ;
- elle possède une précondition claire ;
- elle contient un scénario principal compréhensible ;
- elle couvre les extensions ou limites principales ;
- elle possède des critères d'acceptation testables ;
- elle respecte la séparation Contexte / Analyse ;
- elle ne contredit pas les contraintes agent V1 ;
- elle ne promet pas une autonomie scientifique sans validation humaine.

---

## Résultat global

Statut global : prêt à figer côté rédaction.

Points vérifiés :

- 14 capacités agent présentes : `AG-V1-01` à `AG-V1-14`.
- Toutes les capacités ont les sections attendues.
- Tous les use cases métier `UC-SL-02` à `UC-SL-17` sont couverts par au moins une capacité agent.
- `UC-SL-00` et `UC-SL-01` restent hors capacités agent car ils relèvent de la plateforme et de l'authentification.
- Aucune capacité ne référence un use case inexistant.
- La séparation Mode Contexte / Mode Analyse est explicitement couverte par `AG-V1-14`.
- Le livrable scientifique est couvert par `AG-V1-13`.

Correction appliquée pendant la validation :

- `AG-V1-08` ne dit plus qu'aucun graphique partiel ne peut être généré. La formulation est alignée avec les use cases et contraintes : un graphique exploratoire est possible si ses limites sont explicites ; aucun visuel trompeur ou non sourcé ne doit être produit.

---

## Validation par capacité agent

| Capacité agent | Statut | Validation |
|---|---|---|
| AG-V1-01 — Comprendre les sources disponibles | OK | Distingue les sources et leurs limites. Cohérent avec couverture/lacunes. |
| AG-V1-02 — Aider à formuler le contexte scientifique | OK | Discussion guidée autorisée seulement en mode Contexte. Ne lance pas d'analyse. |
| AG-V1-03 — Valider les données chargées | OK | Couvre inspection sans modification et relie colonnes manquantes aux analyses impossibles. |
| AG-V1-04 — Interroger une source activée | OK | Couvre activation, paramètres, résultats et lacunes. |
| AG-V1-05 — Expliquer les colonnes et unités | OK | Couvre définitions, unités, confiance et colonnes proches. |
| AG-V1-06 — Construire une table de travail | OK | Couvre sources, jointures, colonnes de sortie et diagnostic de jointure. |
| AG-V1-07 — Calculer une variable dérivée | OK | Couvre formule, colonnes, unités, validation avant calcul. |
| AG-V1-08 — Générer un graphique scientifique | OK | Couvre axes, unités, sources et limites. Pas de visuel trompeur. |
| AG-V1-09 — Produire une analyse exploratoire | OK | Couvre méthode validée, résultats, limites et hypothèses. |
| AG-V1-10 — Analyser couverture et lacunes | OK | Couvre synthèse de couverture et distinction lacune / zone non interrogée. |
| AG-V1-11 — Répondre sur le domaine copépodes | OK | Couvre corpus scientifique, ambiguïté taxonomique et absence de preuve. |
| AG-V1-12 — Exporter une synthèse de session | OK | Couvre export technique et session vide. |
| AG-V1-13 — Préparer un livrable scientifique | OK | Couvre dossier/synthèse, titres, légendes, citations et limites. |
| AG-V1-14 — Appliquer l'interface adaptée au mode de travail | OK | Couvre discussion guidée en Contexte et requête structurée en Analyse. |

---

## Couverture des use cases

Use cases couverts par les capacités agent :

```text
UC-SL-02 à UC-SL-17
```

Use cases volontairement hors capacités agent :

```text
UC-SL-00 — S'inscrire
UC-SL-01 — Se connecter à la plateforme
```

Justification : ces deux use cases relèvent de la plateforme, pas du comportement scientifique de l'agent.

---

## Points de vigilance pour la vérification système

Ces points ne bloquent pas la rédaction, mais devront être testés lors de l'implémentation :

- vérifier que l'agent ne lance pas d'analyse en mode Contexte ;
- vérifier que l'agent transforme le contexte en requête structurée en mode Analyse ;
- vérifier que les capacités d'analyse respectent les contraintes de sources, unités et jointures ;
- vérifier que les analyses exploratoires sont distinguées des résultats confirmés ;
- vérifier que les graphiques contiennent axes, unités, sources et limites ;
- vérifier que les exports et livrables ne contiennent pas de données inventées ;
- vérifier que les citations et méthodes sont traçables.

---

## Décision de figer

Les capacités agent V1 peuvent être figées côté rédaction.

La prochaine étape de validation sera la **vérification système**, après prototypage ou implémentation.

