# Projet — Intelligent Data Exploring Assistant pour le zooplancton

## Objectif

Développer un assistant intelligent capable d'aider les chercheurs à explorer et analyser des données zooplanctoniques à partir de questions en langage naturel.

L'idée est de rendre l'analyse scientifique plus accessible, plus rapide et plus interactive.

---

## Problème

Les chercheurs travaillent avec des données nombreuses, complexes et dispersées :

- données biologiques ;
- données environnementales ;
- données d'imagerie ;
- données de campagnes océanographiques.

Ces données demandent souvent des compétences techniques pour être nettoyées, jointes, analysées et visualisées.

---

## Solution proposée

Le projet s'inspire du framework **Intelligent Data Exploring Assistant (IDEA)**.

L'assistant doit permettre de :

- poser une question scientifique en langage naturel ;
- identifier les données utiles ;
- générer du code d'analyse ;
- exécuter ce code ;
- produire des visualisations ;
- expliquer les résultats et les limites.

---

## Adaptation au zooplancton

Dans notre cas, l'assistant est spécialisé sur les données marines et zooplanctoniques.

Il doit aider à explorer des questions liées à :

- la distribution des espèces ;
- la profondeur ;
- la température ;
- les conditions environnementales ;
- les variations spatiales et temporelles ;
- les relations entre organismes et environnement.

---

## Architecture générale

Le système combine :

- **LLM** : comprendre la question et guider l'analyse ;
- **RAG** : récupérer les connaissances scientifiques utiles ;
- **Tools** : accéder aux données et les inspecter ;
- **Python** : nettoyer, joindre, calculer et visualiser ;
- **validation humaine** : garder un contrôle scientifique sur les résultats.

---

## Ce que l'assistant peut faire

L'assistant peut aider à :

- comprendre les données disponibles ;
- vérifier les colonnes et les unités ;
- construire une table de travail ;
- faire une analyse exploratoire ;
- générer des graphiques ;
- expliquer ce qui est fiable ou non.

---

## Ce que l'assistant n'est pas

Ce projet n'est pas seulement un chatbot.

Ce n'est pas non plus un modèle de machine learning isolé.

C'est un système qui combine :

```text
raisonnement
+ données scientifiques
+ génération de code
+ exécution
+ visualisation
```

---

## Impact attendu

L'assistant doit permettre :

- d'accélérer l'exploration des données ;
- de réduire les barrières techniques ;
- de faciliter la production de figures et analyses ;
- d'améliorer la compréhension des données ;
- de soutenir le travail scientifique des chercheurs.

---

## Positionnement

Ce projet vise à développer un assistant intelligent pour l'analyse interactive de données écologiques marines, avec une première application aux données de zooplancton.

