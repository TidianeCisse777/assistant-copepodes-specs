# Capacités agent V1 — Assistant scientifique copépodes
Format : Use cases opérationnels

---

## AG-V1-01 — Comprendre les sources disponibles

**Use cases liés :** UC-SL-04, UC-SL-05, UC-SL-11, UC-SL-14

**Précondition :** session active

**Main success scenario :**
1. L'utilisateur demande quelles données sont disponibles.
2. L'agent distingue EcoTaxa, EcoPart, Amundsen, OGSL, Bio-ORACLE et fichiers labo.
3. L'agent indique ce que chaque source contient.
4. L'agent signale les limites connues et les sources non activées.

**Extensions :**

2a. Source inconnue : l'agent demande à l'utilisateur de préciser la source.

4a. Données labo absentes : l'agent indique que la structure réelle reste inconnue.

**Critères d'acceptation :**

**Étant donné** une question sur les sources disponibles
**Alors** l'agent répond avec sources citées, rôle de chaque source et limites explicites

**Étant donné** une source non activée
**Alors** l'agent indique qu'elle doit être activée avant interrogation

---

## AG-V1-02 — Aider à formuler le contexte scientifique

**Use cases liés :** UC-SL-02, UC-SL-07, UC-SL-08

**Précondition :** mode Contexte actif

**Main success scenario :**
1. L'utilisateur décrit une question scientifique dans une discussion guidée.
2. L'agent identifie les espèces, stades, zone, période et variables d'intérêt.
3. L'agent identifie les hypothèses, limites de données et attentes de mise à l'épreuve.
4. L'agent reformule la démarche scientifique.
5. L'utilisateur valide ou corrige la reformulation.

**Extensions :**

2a. Espèce ou stade ambigu : l'agent demande une précision.

2b. Variable non disponible dans les sources connues : l'agent le signale.

3a. Hypothèse trop vague : l'agent demande une formulation plus précise.

**Critères d'acceptation :**

**Étant donné** une question scientifique incomplète
**Alors** l'agent pose des questions ciblées avant toute analyse

**Étant donné** une reformulation validée
**Alors** le contexte devient disponible pour le mode Analyse

**Étant donné** le mode Contexte actif
**Alors** l'agent peut utiliser une discussion guidée mais ne lance pas d'analyse

---

## AG-V1-03 — Valider les données chargées

**Use cases liés :** UC-SL-03, UC-SL-05, UC-SL-06

**Précondition :** données chargées dans la session

**Main success scenario :**
1. L'utilisateur demande une validation des données.
2. L'agent inspecte colonnes, unités, types et valeurs manquantes.
3. L'agent signale les anomalies ou limites.
4. L'utilisateur décide de continuer, nettoyer ou ignorer certaines anomalies.

**Extensions :**

2a. Format non reconnu : l'agent indique les formats acceptés.

3a. Colonnes scientifiques manquantes : l'agent indique les analyses impossibles.

**Critères d'acceptation :**

**Étant donné** un fichier chargé
**Quand** l'utilisateur demande une validation
**Alors** l'agent produit un rapport sans modifier les données

**Étant donné** des colonnes manquantes
**Alors** l'agent les relie aux analyses qui deviennent impossibles

---

## AG-V1-04 — Interroger une source activée

**Use cases liés :** UC-SL-04, UC-SL-11

**Précondition :** source activée explicitement, session active

**Main success scenario :**
1. L'utilisateur choisit une source en ligne.
2. L'agent demande les paramètres nécessaires : zone, période, espèces, profondeur.
3. L'agent interroge la source activée.
4. L'agent rapporte les données trouvées et les lacunes.
5. L'utilisateur valide les données récupérées.

**Extensions :**

1a. Source non activée : l'agent refuse l'interrogation et explique comment l'activer.

3a. Aucun résultat : l'agent signale explicitement une lacune.

**Critères d'acceptation :**

**Étant donné** une source activée et des paramètres validés
**Alors** l'agent rapporte résultats, absences et provenance

**Étant donné** aucune donnée trouvée
**Alors** l'absence est marquée comme lacune et non comme erreur

---

## AG-V1-05 — Expliquer les colonnes et unités

**Use cases liés :** UC-SL-05, UC-SL-10, UC-SL-11, UC-SL-12, UC-SL-13, UC-SL-15

**Précondition :** données chargées ou source documentée

**Main success scenario :**
1. L'utilisateur demande la signification d'une colonne.
2. L'agent identifie la source de la colonne.
3. L'agent donne la définition, l'unité et le niveau de confiance.
4. L'agent signale les colonnes proches à ne pas confondre.

**Extensions :**

2a. Colonne inconnue : l'agent indique qu'elle n'est pas documentée.

3a. Définition déduite : l'agent précise que la définition n'est pas officielle.

**Critères d'acceptation :**

**Étant donné** une colonne Amundsen documentée
**Alors** l'agent donne la définition et l'unité officielle

**Étant donné** une colonne EcoTaxa ou EcoPart observée
**Alors** l'agent distingue définition observée et définition déduite

---

## AG-V1-06 — Construire une table de travail

**Use cases liés :** UC-SL-04, UC-SL-10, UC-SL-11, UC-SL-13, UC-SL-15

**Précondition :** contexte validé, données chargées, mode Analyse actif

**Main success scenario :**
1. L'utilisateur demande une table utile pour une analyse.
2. L'agent identifie les sources nécessaires.
3. L'agent propose les clés de jointure et les colonnes de sortie.
4. L'utilisateur valide.
5. L'agent construit la table et cite les sources.

**Extensions :**

3a. Jointure incertaine : l'agent propose une table de diagnostic avant la table finale.

3b. Colonne obligatoire absente : l'agent refuse la construction et indique ce qui manque.

**Critères d'acceptation :**

**Étant donné** une table construite
**Alors** les sources, clés de jointure et colonnes calculées sont explicites

**Étant donné** une jointure par profondeur
**Alors** la table contient un indicateur de delta ou de qualité du match

---

## AG-V1-07 — Calculer une variable dérivée

**Use cases liés :** UC-SL-15

**Précondition :** données chargées, méthode connue, mode Analyse actif

**Main success scenario :**
1. L'utilisateur demande une variable dérivée.
2. L'agent identifie la méthode de calcul.
3. L'agent vérifie les colonnes et unités requises.
4. L'agent soumet la méthode à validation.
5. L'agent calcule la variable après validation.

**Extensions :**

3a. Colonne manquante : l'agent refuse le calcul et indique l'information manquante.

4a. Méthode contestée : l'agent ajuste et soumet à nouveau.

**Critères d'acceptation :**

**Étant donné** une demande de calcul
**Alors** l'agent présente formule, colonnes, unités et limites avant exécution

**Étant donné** une variable source absente
**Alors** aucun calcul n'est produit

---

## AG-V1-08 — Générer un graphique scientifique

**Use cases liés :** UC-SL-09, UC-SL-10, UC-SL-11, UC-SL-13, UC-SL-14, UC-SL-17

**Précondition :** contexte validé, données chargées, mode Analyse actif

**Main success scenario :**
1. L'utilisateur décrit le graphique attendu.
2. L'agent identifie les données nécessaires.
3. L'agent vérifie que les variables sont disponibles.
4. L'agent génère le graphique avec unités et sources.
5. L'utilisateur valide ou demande un ajustement.

**Extensions :**

3a. Données insuffisantes : l'agent signale le manque ; un graphique exploratoire peut être proposé seulement si ses limites sont explicites.

5a. Ajustement demandé : l'agent modifie le graphique en conservant la méthode.

**Critères d'acceptation :**

**Étant donné** un graphique généré
**Alors** les axes, unités et sources sont indiqués

**Étant donné** des données insuffisantes
**Alors** l'agent explique le manque et ne produit aucun visuel trompeur ou non sourcé

---

## AG-V1-09 — Produire une analyse exploratoire

**Use cases liés :** UC-SL-10, UC-SL-11, UC-SL-12, UC-SL-13, UC-SL-14

**Précondition :** contexte validé, données chargées, mode Analyse actif

**Main success scenario :**
1. L'utilisateur formule une question exploratoire.
2. L'agent propose une méthode d'analyse.
3. L'utilisateur valide la méthode.
4. L'agent produit résultats, tableaux ou graphiques.
5. L'agent distingue résultats, limites et hypothèses.

**Extensions :**

2a. Question trop large : l'agent demande de réduire le périmètre.

4a. Résultat non concluant : l'agent signale l'absence de signal clair.

**Critères d'acceptation :**

**Étant donné** une analyse exploratoire
**Alors** la méthode est validée avant exécution

**Étant donné** un résultat produit
**Alors** l'agent sépare observation, interprétation et limite des données

---

## AG-V1-10 — Évaluer la complétude et synthétiser les lacunes

**Use cases liés :** UC-SL-11 (ext. 4a), UC-SL-12 (ext. 3b), UC-SL-14

**Précondition :** contexte validé, données chargées, mode Analyse actif

**Main success scenario :**
1. L'utilisateur demande une évaluation de la complétude ou une synthèse des lacunes pour son périmètre.
2. L'agent évalue le taux de remplissage des colonnes clés : disponible, partielle ou absente.
3. L'agent identifie les variables critiques inutilisables et explique quelle analyse devient impossible pour chacune.
4. L'agent produit un rapport de lacunes structuré distinguant ce qui est disponible, manquant et inutilisable.
5. L'utilisateur exporte le rapport ou affine le périmètre.

**Extensions :**

2a. Aucune colonne clé identifiable : l'agent demande à l'utilisateur de préciser les variables d'intérêt.

3a. Variable critique absente partout : l'agent la marque comme bloquante, indique l'alternative disponible si elle existe.

4a. Lacunes spatio-temporelles ou absences taxonomiques déjà produites (UC-SL-11 ext. 4a, UC-SL-12 ext. 3b) : l'agent les intègre dans la synthèse globale si disponibles.

**Critères d'acceptation :**

**Étant donné** données chargées **Quand** l'évaluation de complétude est demandée
**Alors** l'agent produit un tableau de remplissage par colonne clé avec statut disponible / partielle / absente

**Étant donné** une variable critique absente
**Alors** l'agent l'identifie comme bloquante et explique quelle analyse est impossible

**Étant donné** rapport de lacunes produit
**Alors** il distingue explicitement disponible, manquant et inutilisable, et est exportable comme support de demande de subvention

---

## AG-V1-11 — Répondre sur le domaine copépodes

**Use cases liés :** UC-SL-07, UC-SL-10, UC-SL-11, UC-SL-12 (ext. 3b), UC-SL-13

**Précondition :** corpus scientifique disponible

**Main success scenario :**
1. L'utilisateur pose une question sur une espèce, un stade ou une variable biologique.
2. L'agent cherche dans le corpus scientifique.
3. L'agent répond avec les termes du domaine.
4. L'agent signale les points à valider si la connaissance est incertaine.

**Extensions :**

1a. Espèce ambiguë : l'agent demande une précision.

3a. Question liée aux données disponibles : l'agent indique quelles sources peuvent vérifier la réponse.

**Critères d'acceptation :**

**Étant donné** une question domaine
**Alors** l'agent répond avec source documentaire ou signale l'absence de preuve

**Étant donné** une distinction taxonomique incertaine
**Alors** l'agent ne conclut pas sans méthode d'identification fiable

---

## AG-V1-12 — Exporter une synthèse de session

**Use cases liés :** UC-SL-16

**Précondition :** session active avec contexte ou analyse

**Main success scenario :**
1. L'utilisateur demande un export.
2. L'agent compile le contexte scientifique.
3. L'agent ajoute sources, méthodes, résultats et limites.
4. L'agent génère un export lisible.

**Extensions :**

1a. Session vide : l'agent signale que l'export serait vide.

3a. Analyse incomplète : l'agent indique les sections manquantes.

**Critères d'acceptation :**

**Étant donné** une session avec analyse
**Alors** l'export contient contexte, sources, méthode, résultats et limites

**Étant donné** une session vide
**Alors** l'agent refuse l'export ou le marque comme vide

---

## AG-V1-13 — Préparer un livrable scientifique

**Use cases liés :** UC-SL-17

**Précondition :** session active avec au moins une analyse, un graphique ou une synthèse de couverture

**Main success scenario :**
1. L'utilisateur demande un livrable scientifique à partir de la session.
2. L'agent rassemble contexte, sources, méthodes, résultats, graphiques, limites et citations.
3. L'agent propose un format adapté : dossier de résultats, synthèse de présentation, annexe méthodologique ou support de subvention.
4. L'agent prépare les titres de graphiques, légendes, citations courtes et citations complètes.
5. L'utilisateur valide ou ajuste.
6. L'agent génère le livrable final.

**Extensions :**

2a. Contexte absent : l'agent demande de compléter le contexte avant génération.

2b. Source ou méthode non tracée : l'agent signale que la citation ou la méthode doit être complétée.

3a. Résultats incomplets : l'agent distingue résultats confirmés, exploratoires et manquants.

5a. Format demandé différent : l'agent adapte la structure du livrable.

**Critères d'acceptation :**

**Étant donné** une session avec analyse ou graphique
**Alors** l'agent produit un livrable structuré avec contexte, résultats, figures, titres, légendes, citations et limites

**Étant donné** une information manquante pour une légende ou une citation
**Alors** l'agent la signale explicitement au lieu de l'inventer

**Étant donné** une analyse incomplète
**Alors** le livrable distingue les résultats confirmés, exploratoires et manquants

---

## AG-V1-14 — Appliquer l'interface adaptée au mode de travail

**Use cases liés :** UC-SL-02, UC-SL-07, UC-SL-08, UC-SL-10, UC-SL-11, UC-SL-12, UC-SL-13, UC-SL-14, UC-SL-15

**Précondition :** session active

**Main success scenario :**
1. L'utilisateur sélectionne ou utilise un mode de travail.
2. En mode Contexte, l'agent autorise une discussion guidée pour clarifier la question scientifique.
3. En mode Analyse, l'agent transforme le contexte en formulaire ou requête structurée.
4. L'utilisateur valide les paramètres structurés.
5. L'agent lance l'analyse seulement après validation.
6. L'agent retourne un rapport statique plutôt qu'une conversation progressive.

**Extensions :**

2a. L'utilisateur demande une analyse en mode Contexte : l'agent redirige vers la validation du contexte puis le mode Analyse.

3a. Paramètres incomplets : l'agent bloque le lancement et demande les champs manquants.

5a. L'utilisateur modifie un paramètre : l'agent met à jour la requête structurée avant exécution.

**Critères d'acceptation :**

**Étant donné** le mode Contexte actif
**Alors** l'agent peut dialoguer mais ne lance pas d'analyse

**Étant donné** le mode Analyse actif
**Alors** l'agent utilise une requête structurée validée avant exécution

**Étant donné** une analyse terminée
**Alors** le résultat est présenté comme rapport statique, pas comme chat libre
