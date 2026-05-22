# Contexte métier — Assistant scientifique copépodes
#
# Ce fichier définit les termes métier du domaine.
# Pour les specs complètes : STAGE ULAVAL/
# Pour les tools et l'implémentation : TOOLS_SPEC.js, IMPLEMENTATION_ORDER.md

## Glossaire

### Use case d'analyse standardisé

Un use case d'analyse standardisé est un parcours d'analyse concret qui regroupe des traitements, graphiques, tableaux et contrôles qualité adaptés à un type de question scientifique.

Il remplace les formulations trop génériques comme "générer une analyse". Il sert à guider l'utilisateur vers des traitements réalistes et reproductibles selon les données disponibles.

Exemples de use cases d'analyse V1 :

- distribution verticale ;
- distribution spatio-temporelle ;
- taxonomie / stades ;
- environnement CTD ;
- couverture et lacunes.

### Interprétation scientifique (hors périmètre)

L'agent ne produit aucune interprétation scientifique des résultats. Il génère des sorties (graphiques, tableaux, rapports de lacunes, variables dérivées) et les labellise (source, méthode, limites). L'interprétation biologique — ce que les données signifient, ce qu'elles impliquent sur les espèces ou l'écosystème — appartient exclusivement au chercheur.

Cette règle est plus forte que CT-AG-13 : ce n'est pas seulement "ne pas sur-interpréter", c'est ne pas interpréter du tout.

### Données labo

Les données labo sont des fichiers fournis par l'utilisateur (CSV, Excel, TSV) contenant des mesures produites en laboratoire : analyses lipidiques, biomasse carbone (g CO2/m³), et autres variables dérivées d'échantillons biologiques.

Contrairement aux sources en ligne (EcoTaxa, EcoPart, Amundsen), leur structure est inconnue avant inspection. L'agent doit les inspecter via `data.inspect` avant tout traitement.

Ces fichiers sont une source citeable au même titre que les sources en ligne (CT-AG-01).

### Use case post-analyse

Un use case post-analyse transforme les résultats produits pendant la session en livrable utilisable par un chercheur.

Le système prépare automatiquement le dossier ou la synthèse, les titres et légendes de figures, les citations des sources et méthodes, puis l'utilisateur valide ou ajuste.

Il ne produit pas une nouvelle analyse scientifique. Il organise, documente et rend présentables les résultats déjà générés.
