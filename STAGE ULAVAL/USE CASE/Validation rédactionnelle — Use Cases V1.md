# Validation rédactionnelle — Use Cases V1

Objectif : figer la rédaction des use cases avant implémentation.

Cette validation porte sur :

- clarté ;
- non-ambiguïté ;
- non-contradiction ;
- format Cockburn léger ;
- cohérence avec les capacités agent et contraintes V1.

Elle ne valide pas encore le fonctionnement système réel.

---

## Définition of Done rédactionnelle d'un use case

Un use case V1 est considéré prêt si :

- le titre décrit une intention utilisateur claire ;
- `System`, `Primary Actor`, `Goal Level` et `Précondition` sont présents ;
- le scénario principal décrit un flux nominal compréhensible ;
- les extensions couvrent les principaux cas d'échec ou de limite ;
- les critères d'acceptation sont observables ;
- le use case ne mélange pas plusieurs objectifs utilisateurs incompatibles ;
- le use case ne contredit pas les contraintes agent V1 ;
- le use case ne décrit pas trop finement l'implémentation technique sauf si c'est une contrainte assumée.

---

## Résultat global

Statut global : prêt à figer côté rédaction — **V1.1 (révision axe lacunes)**.

Points vérifiés :

- 18 use cases présents : `UC-SL-00` à `UC-SL-17`.
- Tous les use cases ont les sections Cockburn attendues.
- Les use cases métier `UC-SL-02` à `UC-SL-17` sont couverts par les capacités agent.
- `UC-SL-00` et `UC-SL-01` restent hors capacités agent, car ils relèvent de la plateforme/authentification.
- Le vocabulaire "kit" a été retiré des use cases.
- Les analyses ne sont plus formulées comme une analyse générique unique.
- Les contraintes détaillées sont déplacées dans `Contraintes agent V1.md`.

Corrections appliquées pendant la validation initiale :

- `UC-SL-09` ne dit plus qu'aucun graphique partiel ne peut être généré. La formulation est maintenant alignée avec les contraintes : un graphique exploratoire est possible si les limites sont explicites ; aucun graphique trompeur ou non sourcé ne doit être généré.

Révision V1.1 — axe couverture et lacunes :

- `UC-SL-11` enrichi : ajout d'une extension et d'un critère d'acceptation pour l'identification des lacunes spatio-temporelles (zones sans données, gaps entre campagnes). Le titre devient "Analyser la distribution et les lacunes spatio-temporelles".
- `UC-SL-12` enrichi : ajout de l'extension 3b et d'un critère d'acceptation pour l'identification des absences taxonomiques (espèces attendues dans la zone mais non observées, comparaison via corpus RAG et OBIS). Le titre devient "Analyser la taxonomie, les stades et les absences".
- `UC-SL-14` réécrit : ancienne formulation trop générique et chevauchant UC-SL-11 et UC-SL-12. Nouveau périmètre recentré sur la complétude des variables mesurées (taux de remplissage par colonne, variables critiques inutilisables) et la synthèse globale des lacunes avec comparaison aux sources externes (OBIS). Le titre devient "Évaluer la complétude des données et synthétiser les lacunes". Une note de périmètre explicite dans le use case évite la confusion avec UC-SL-11 et UC-SL-12.

---

## Validation par use case

| Use case | Statut | Validation |
|---|---|---|
| UC-SL-00 — S'inscrire | OK | Use case plateforme clair. Hors périmètre agent scientifique. |
| UC-SL-01 — Se connecter à la plateforme | OK | Use case plateforme clair. Hors périmètre agent scientifique. |
| UC-SL-02 — Sélectionner le mode de travail | OK | Séparation Contexte / Analyse cohérente avec `CT-AG-23`. |
| UC-SL-03 — Téléverser ses données | OK | Flux simple et testable. |
| UC-SL-04 — Interroger les données en ligne | OK | Couvre sélection source, paramètres et lacunes. La discussion sert au cadrage, pas à l'analyse libre. |
| UC-SL-05 — Valider les données | OK | Couvre inspection sans modification. Cohérent avec préservation des données brutes. |
| UC-SL-06 — Nettoyer les données | OK | Nettoyage conditionné à validation utilisateur. |
| UC-SL-07 — Décrire son contexte scientifique | OK | Couvre le ticket d'entrée scientifique. |
| UC-SL-08 — Valider la reformulation du contexte | OK | Couvre validation humaine avant analyse. |
| UC-SL-09 — Générer un graphique | OK | Aligné avec sources, unités, limites et graphiques exploratoires contrôlés. |
| UC-SL-10 — Analyser la distribution verticale | OK | Use case concret, colonnes nécessaires explicites, limites de profondeur couvertes. |
| UC-SL-11 — Analyser la distribution et les lacunes spatio-temporelles | OK (V1.1) | Use case concret, couvre carte/timeline et cas position/date absentes. Enrichi : extension 4a et critère d'acceptation pour la production d'une carte des zones sans données et d'une timeline des gaps entre campagnes. |
| UC-SL-12 — Analyser la taxonomie, les stades et les absences | OK (V1.1) | Couvre taxon, stade, statut d'annotation et analyse exploratoire si annotations non validées. Enrichi : extension 3b et critère d'acceptation pour l'identification des espèces attendues non observées, via corpus RAG et OBIS. |
| UC-SL-13 — Analyser les variables environnementales CTD | OK | Couvre source CTD, jointure et deltas. |
| UC-SL-14 — Évaluer la complétude des données et synthétiser les lacunes | OK (V1.1) | Réécrit. Ancienne version trop vague et chevauchant UC-SL-11/12. Nouveau périmètre : complétude des variables mesurées (taux de remplissage, variables critiques inutilisables) + comparaison aux sources externes (OBIS) + rapport de lacunes exportable. Note de périmètre explicite dans le use case. |
| UC-SL-15 — Calculer une variable dérivée | OK | Méthode validée avant exécution, calcul bloqué si colonnes sources manquantes. |
| UC-SL-16 — Exporter la session d'analyse | OK | Export technique clair, distinct du livrable scientifique. |
| UC-SL-17 — Préparer un livrable scientifique | OK | Transforme les résultats en livrable sans produire une nouvelle analyse. |

---

## Points de vigilance pour la vérification système

Ces points ne bloquent pas la rédaction, mais devront être testés lors de l'implémentation :

- vérifier que le mode Contexte permet bien la discussion guidée sans exécuter d'analyse ;
- vérifier que le mode Analyse passe bien par une requête structurée ;
- vérifier que les résultats sont affichés en rapport statique, sans streaming textuel ;
- vérifier que les sources et méthodes sont traçables ;
- vérifier que les erreurs de colonnes manquantes produisent un feedback utile ;
- vérifier que les analyses exploratoires sont visuellement distinguées des résultats confirmés ;
- vérifier que les exports et livrables ne contiennent aucun secret.

---

## Décision de figer

Les use cases V1.1 peuvent être figés côté rédaction.

La révision V1.1 est circonscrite à UC-SL-11, UC-SL-12 et UC-SL-14 — les 15 autres use cases restent inchangés. Les modifications n'introduisent pas de nouveaux use cases ; elles précisent les périmètres et éliminent les chevauchements sur l'axe lacunes.

La prochaine étape de validation sera la **vérification système**, après prototypage ou implémentation. L'axe couverture/lacunes (UC-SL-11 extension 4a, UC-SL-12 extension 3b, UC-SL-14 complet) devra être priorisé dans les tests car il implique des comparaisons avec OBIS qui nécessitent une source activée.

