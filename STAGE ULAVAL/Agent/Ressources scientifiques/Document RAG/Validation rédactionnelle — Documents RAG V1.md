# Validation rédactionnelle — Documents RAG V1

Objectif : figer la rédaction des documents RAG avant implémentation.

Cette validation porte sur :

- format des chunks ;
- clarté des questions ;
- autonomie des réponses ;
- cohérence avec les use cases, capacités agent et contraintes ;
- absence de données inventées ;
- lisibilité scientifique.

Elle ne valide pas encore la performance de retrieval ni la qualité d'un moteur RAG réel.

---

## Definition of Done rédactionnelle d'un document RAG

Un document RAG V1 est considéré prêt si :

- chaque chunk commence par `---` ;
- chaque chunk commence ensuite par un titre `#` sous forme de question ;
- chaque chunk est autonome ;
- les noms de colonnes réels sont conservés quand ils sont connus ;
- les unités sont indiquées quand elles sont nécessaires ;
- les limites ou conditions d'usage sont explicites ;
- les calculs indiquent les colonnes requises ;
- les sources ou niveaux de confiance sont distingués ;
- le document ne contient pas de secret, token ou credential ;
- le document ne remplace pas les données absentes par des hypothèses non signalées.

---

## Résultat global

Statut global : prêt à figer côté rédaction.

Points vérifiés :

- tous les fichiers Markdown sont en UTF-8 valide ;
- tous les chunks RAG commencent par `---` ;
- tous les titres de chunks sont des questions ;
- aucun séparateur orphelin détecté ;
- aucune occurrence de `ECOTaxa` au lieu de `EcoTaxa` ;
- aucune occurrence `TODO`, `à définir`, `à préciser` ;
- aucun ancien vocabulaire "kit" dans les documents RAG ;
- aucune section `Quand refuser` restante dans `methodes_calcul.md` : la logique est maintenant orientée feedback.

---

## Validation par document

| Document | Chunks | Statut | Validation |
|---|---:|---|---|
| `colonnes_instruments.md` | 9 | OK | Dictionnaire instrument EcoTaxa clair. Titres-question valides. |
| `colonnes_sources.md` | 8 | OK | Colonnes observées EcoTaxa, EcoPart et Amundsen. Jointures et pièges couverts. |
| `copepodes_domaine.md` | 13 | OK | Domaine copépodes structuré par questions biologiques. Limites taxonomiques visibles. |
| `methodes_calcul.md` | 10 | OK | Calculs, colonnes requises, unités et feedback si données incomplètes. |
| `sources_en_ligne.md` | 7 | OK | Sources en ligne et rôle de chaque source documentés. |
| `PLAN DOC RAG.md` | n/a | OK | Guide d'organisation et format obligatoire des chunks. |

---

## Couverture par rapport aux besoins V1

Les documents RAG couvrent les besoins suivants :

- comprendre les sources disponibles ;
- expliquer les colonnes et unités ;
- différencier EcoTaxa, EcoPart, Amundsen, OBIS, CMEMS et fichiers labo ;
- calculer ou refuser proprement une concentration, biomasse, taille, lipid fullness ou association CTD ;
- soutenir les analyses verticales, spatio-temporelles, taxonomiques, environnementales et de couverture/lacunes ;
- rappeler les limites biologiques et taxonomiques des copépodes ;
- guider l'agent vers les sources à utiliser selon la question.

---

## Points de vigilance pour la vérification système

Ces points ne bloquent pas la rédaction, mais devront être testés avec un vrai pipeline RAG :

- vérifier que le découpage en chunks produit les bons passages pour des questions utilisateur réelles ;
- vérifier que les titres-question améliorent bien la récupération ;
- vérifier que le moteur RAG cite le bon document et le bon chunk ;
- vérifier que les réponses ne mélangent pas des chunks incompatibles ;
- vérifier que les colonnes `obj_*` et `object_*` ne sont pas homogénéisées à tort ;
- vérifier que `methodes_calcul.md` déclenche bien un feedback utile quand les colonnes manquent ;
- vérifier que les sources en ligne ne sont pas utilisées sans activation ou credential quand requis.

---

## Décision de figer

Les documents RAG V1 peuvent être figés côté rédaction.

La prochaine étape de validation sera la **vérification système RAG**, après choix ou prototypage du moteur de retrieval.

