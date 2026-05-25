

## Objectif sea level A — Explorer et analyser une question scientifique

**Intention utilisateur :** le chercheur ou l'étudiant veut explorer une question scientifique sur les copépodes sans être bloqué par le code, les jointures ou la manipulation des données.

**Résultat attendu :** l'assistant aide à formuler le contexte, valide les données disponibles, produit des analyses standards réalistes et explique les résultats avec leurs limites.

**Use cases couverts :**

- UC-SL-02 — Sélectionner le mode de travail
- UC-SL-03 — Téléverser ses données
- UC-SL-04 — Interroger les données en ligne
- UC-SL-05 — Valider les données
- UC-SL-07 — Décrire son contexte scientifique
- UC-SL-08 — Valider la reformulation du contexte
- UC-SL-09 — Générer un graphique
- UC-SL-10 — Analyser la distribution verticale
- UC-SL-11 — Analyser la distribution spatio-temporelle
- UC-SL-12 — Analyser la taxonomie et les stades
- UC-SL-13 — Analyser les variables environnementales CTD
- UC-SL-15 — Calculer une variable dérivée
- UC-SL-17 — Préparer un livrable scientifique

**Succès :** l'utilisateur obtient une analyse ou une visualisation exploitable, avec les sources citées et les limites scientifiques explicites.

---

## Objectif sea level B — Évaluer la couverture et les lacunes des données

**Intention utilisateur :** le chercheur veut comprendre ce que les données couvrent réellement et où se trouvent les manques.

**Résultat attendu :** l'assistant distingue les zones, périodes, espèces, stades, campagnes ou variables bien représentées de celles qui sont absentes ou insuffisamment couvertes.

**Use cases couverts :**

- UC-SL-04 — Interroger les données en ligne
- UC-SL-05 — Valider les données
- UC-SL-11 — Analyser la distribution spatio-temporelle
- UC-SL-12 — Analyser la taxonomie et les stades
- UC-SL-14 — Analyser la couverture et les lacunes
- UC-SL-16 — Exporter la session d'analyse
- UC-SL-17 — Préparer un livrable scientifique

**Succès :** l'utilisateur obtient une synthèse claire de la couverture et des lacunes, utilisable pour orienter une exploration scientifique ou soutenir une demande de subvention.

---

## UC-SL-00 — S'inscrire

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** aucune — premier accès à la plateforme

**Main success scenario :**
1. L'utilisateur accède à la plateforme pour la première fois.
2. L'utilisateur sélectionne l'option créer un compte.
3. L'utilisateur renseigne ses informations.
4. Le système envoie un courriel de confirmation.
5. L'utilisateur confirme son adresse.
6. Le système crée le compte et démarre une session vide.

**Extensions :**

3a. Informations invalides : le système signale les champs à corriger.

3b. Compte déjà existant : le système redirige vers UC-SL-01.

5a. Lien expiré : le système propose d'en renvoyer un.

**Critères d'acceptation :**

**Étant donné** premier accès, formulaire soumis
**Alors** courriel de confirmation envoyé

**Étant donné** lien de confirmation cliqué
**Alors** compte créé, session vide démarrée

**Étant donné** lien expiré **Quand** l'utilisateur tente de confirmer
**Alors** le système propose un nouveau lien

---

## UC-SL-01 — Se connecter à la plateforme

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** compte existant

**Main success scenario :**
1. L'utilisateur accède à la plateforme.
2. L'utilisateur s'authentifie.
3. Le système charge l'historique des conversations et sessions d'analyse.
4. L'utilisateur reprend ou démarre une session.

**Extensions :**

2a. Compte inexistant : le système propose la création d'un compte.

3a. Aucun historique : le système démarre une session vide.

**Critères d'acceptation :**

**Étant donné** compte valide **Quand** l'utilisateur s'authentifie
**Alors** historique de sessions chargé

**Étant donné** compte inexistant **Quand** tentative de connexion
**Alors** le système propose la création d'un compte

---

## UC-SL-02 — Sélectionner le mode de travail

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** utilisateur connecté

**Main success scenario :**
1. Après connexion, le système présente les deux modes disponibles.
2. L'utilisateur sélectionne le mode Contexte ou le mode Analyse.
3. Le système configure son comportement selon le mode choisi.
4. L'utilisateur peut changer de mode à tout moment.

**Extensions :**

2a. Mode Contexte : aucune génération de script ou visuel.

2b. Mode Analyse : génération scripts, analyses et visuels à partir du contexte établi.

3a. Mode Analyse sans contexte défini : redirection vers le mode Contexte.

**Critères d'acceptation :**

**Étant donné** mode Contexte sélectionné
**Alors** toute génération de script ou visuel désactivée

**Étant donné** mode Analyse, aucun contexte défini
**Alors** redirection vers le mode Contexte

---

## UC-SL-03 — Téléverser ses données

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** utilisateur connecté, session active

**Main success scenario :**
1. L'utilisateur sélectionne l'option téléverser.
2. L'utilisateur choisit ses fichiers.
3. Le système valide le format.
4. Le système affiche un feedback de confirmation.

**Extensions :**

3a. Format non reconnu : le système indique les formats acceptés.

3b. Fichier corrompu : le système signale l'erreur.

**Critères d'acceptation :**

**Étant donné** fichier au format valide **Quand** téléversement lancé
**Alors** données disponibles pour la session, confirmation affichée

**Étant donné** format non reconnu **Quand** téléversement lancé
**Alors** formats acceptés indiqués, fichier non chargé

---

## UC-SL-04 — Interroger les données en ligne

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** utilisateur connecté, session active

**Main success scenario :**
1. L'utilisateur indique qu'il veut interroger des données en ligne.
2. Le système engage une discussion pour préciser les paramètres : source, zone géographique, période, espèces.
3. L'utilisateur et le système affinent les paramètres ensemble jusqu'à validation.
4. Le système interroge les sources en ligne spécifiées.
5. Le système rapporte ce qu'il a trouvé et ce qui est absent.
6. Le système stocke les données récupérées pour la session.
7. L'utilisateur valide les données récupérées.

**Extensions :**

5a. Aucune donnée trouvée : le système signale explicitement comme lacune.

7a. L'utilisateur affine les paramètres : retour à l'étape 2.

**Critères d'acceptation :**

**Étant donné** zone, période, espèces précisées **Quand** sources interrogées
**Alors** résultats rapportés, lacunes signalées, données stockées

**Étant donné** aucune donnée trouvée pour un paramètre
**Alors** signalé explicitement comme lacune

---

## UC-SL-05 — Valider les données

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** données chargées

**Main success scenario :**
1. L'utilisateur choisit de valider ses données et précise ce qu'il veut vérifier.
2. Le système exécute les vérifications demandées.
3. Le système rapporte les résultats.
4. L'utilisateur décide de la suite — nettoyer, ignorer, ou continuer.

**Extensions :**

4a. L'utilisateur veut nettoyer : redirige vers UC-SL-06.

4b. L'utilisateur continue sans nettoyer : anomalies enregistrées pour les analyses suivantes.

**Critères d'acceptation :**

**Étant donné** vérifications précisées par l'utilisateur **Quand** exécutées
**Alors** rapport produit, données non modifiées

**Étant donné** l'utilisateur continue sans nettoyer
**Alors** anomalies enregistrées pour les analyses suivantes

---

## UC-SL-06 — Nettoyer les données

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** UC-SL-05 complété, anomalies identifiées

**Main success scenario :**
1. Le système présente les anomalies identifiées et propose des actions de nettoyage.
2. L'utilisateur valide les actions proposées.
3. Le système nettoie les données et confirme.

**Extensions :**

2a. L'utilisateur refuse certaines actions : données brutes conservées, risques signalés.

2b. L'utilisateur modifie une action : le système ajuste et soumet à nouveau.

**Critères d'acceptation :**

**Étant donné** anomalies identifiées **Quand** l'utilisateur valide le nettoyage
**Alors** données nettoyées, modifications confirmées

**Étant donné** l'utilisateur refuse une action
**Alors** données brutes conservées, risques pour l'analyse signalés

---

## UC-SL-07 — Décrire son contexte scientifique

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** mode Contexte actif

**Main success scenario :**
1. Le système invite l'utilisateur à décrire sa démarche scientifique.
2. L'utilisateur explique la question ou l'hypothèse qu'il veut explorer.
3. L'utilisateur précise comment les données s'inscrivent dans cette démarche.
4. Le système enregistre le contexte et invite à le valider.

**Extensions :**

2a. Hypothèse non formulée : le système pose des questions ciblées.

**Critères d'acceptation :**

**Étant donné** mode Contexte actif **Quand** démarche décrite
**Alors** contexte enregistré, validation demandée

---

## UC-SL-08 — Valider la reformulation du contexte

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** UC-SL-07 complété

**Main success scenario :**
1. Le système reformule le contexte soumis.
2. L'utilisateur valide ou corrige la reformulation.
3. Le contexte est confirmé et disponible pour les analyses suivantes.

**Extensions :**

2a. L'utilisateur corrige : le système reformule à nouveau.

3a. Incohérence détectée avec les données : signalée avant confirmation.

**Critères d'acceptation :**

**Étant donné** l'utilisateur valide la reformulation
**Alors** contexte enregistré, disponible pour les analyses

**Étant donné** incohérence détectée **Quand** contexte soumis
**Alors** incohérence signalée avant de continuer

---

## UC-SL-09 — Générer un graphique

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** contexte validé, données chargées, mode Analyse actif

**Main success scenario :**
1. L'utilisateur décrit le graphique qu'il veut obtenir en lien avec son contexte.
2. Le système identifie les données nécessaires.
3. Le système génère le graphique et cite les sources.
4. L'utilisateur valide ou demande un ajustement.

**Extensions :**

2a. Données insuffisantes : ce qui manque est signalé ; un graphique exploratoire peut être proposé seulement si ses limites sont explicites.

4a. Ajustement demandé : retour à l'étape 1.

**Critères d'acceptation :**

**Étant donné** contexte validé, données chargées **Quand** graphique décrit
**Alors** graphique généré, sources citées

**Étant donné** données insuffisantes
**Alors** manques signalés ; aucun graphique trompeur ou non sourcé n'est généré

---

## UC-SL-10 — Analyser la distribution verticale

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** contexte validé, données chargées, mode Analyse actif

**Main success scenario :**
1. L'utilisateur demande comment une espèce, un groupe, un stade ou une variable varie avec la profondeur.
2. Le système identifie les colonnes nécessaires : taxon ou groupe, profondeur, station/profil, date et variable à analyser.
3. Le système propose un traitement vertical adapté : profil, distribution par bins de profondeur, résumé par profondeur, ou comparaison entre profils.
4. L'utilisateur valide le traitement.
5. Le système produit l'analyse verticale, les graphiques associés et cite les sources.

**Extensions :**

2a. Profondeur absente : le système signale que l'analyse verticale est impossible.

2b. Profondeur disponible seulement par intervalle : le système utilise le midpoint et signale la méthode.

3a. Variable biologique ou environnementale absente : le système propose une alternative disponible.

4a. L'utilisateur conteste le traitement : le système ajuste et soumet à nouveau.

**Critères d'acceptation :**

**Étant donné** une profondeur disponible **Quand** l'analyse verticale est demandée
**Alors** le système produit un résumé ou graphique par profondeur avec unités et sources

**Étant donné** une profondeur manquante
**Alors** le système signale que l'analyse verticale n'est pas possible et indique les colonnes manquantes

---

## UC-SL-11 — Analyser la distribution et les lacunes spatio-temporelles

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** contexte validé, données chargées, mode Analyse actif

**Main success scenario :**
1. L'utilisateur demande où et quand les observations ou mesures sont disponibles.
2. Le système identifie les colonnes nécessaires : latitude, longitude, date/heure, station ou campagne, espèce/groupe si applicable.
3. Le système produit une synthèse spatiale et temporelle : carte, timeline, nombre d'observations par zone/période, ou tableau de couverture.
4. Le système signale les périodes, stations ou zones peu représentées ou absentes.
5. L'utilisateur affine le périmètre, demande les lacunes explicites, ou valide les résultats.

**Extensions :**

2a. Position absente : le système propose une analyse temporelle seulement.

2b. Date absente : le système propose une analyse spatiale seulement.

4a. L'utilisateur demande les lacunes spatio-temporelles : le système produit une carte des zones sans données et une timeline des gaps entre campagnes, avec l'amplitude de chaque gap.

5a. L'utilisateur affine la zone, la période ou le groupe : retour à l'étape 1.

**Critères d'acceptation :**

**Étant donné** latitude, longitude et date disponibles **Quand** l'analyse spatio-temporelle est demandée
**Alors** carte et timeline sont produites avec sources citées

**Étant donné** une dimension absente
**Alors** le système adapte l'analyse et indique la limite

**Étant donné** l'utilisateur demande les lacunes spatio-temporelles
**Alors** le système produit une carte des zones sans données et une timeline des gaps entre campagnes, chaque absence étant explicitement distinguée d'une zone couverte

---

## UC-SL-12 — Analyser la taxonomie, les stades et les absences

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** contexte validé, données chargées, mode Analyse actif

**Main success scenario :**
1. L'utilisateur demande une analyse taxonomique, une analyse des stades, ou l'identification des espèces ou stades attendus mais absents.
2. Le système identifie les colonnes nécessaires : taxon, statut d'annotation, stade si disponible, objet ou comptage.
3. Le système vérifie la fiabilité des annotations disponibles.
4. Le système produit une synthèse : liste des taxons, abondance brute ou comptage, répartition par stade, ou comparaison entre groupes.
5. Le système cite les sources et signale les limites taxonomiques.

**Extensions :**

2a. Stade absent : le système produit seulement une synthèse taxonomique.

2b. Taxon absent : le système signale que l'analyse taxonomique est impossible.

3a. Annotations non validées : le système signale que l'analyse est exploratoire.

3b. L'utilisateur demande les absences taxonomiques : le système compare la liste des taxons observés aux espèces documentées pour la zone géographique définie, à partir du corpus RAG copépodes. Il liste les espèces attendues non observées dans les données, en citant la source de référence.

**Critères d'acceptation :**

**Étant donné** taxon et statut d'annotation disponibles **Quand** l'analyse taxonomique est demandée
**Alors** le système produit une synthèse par taxon avec statut de validation

**Étant donné** stade disponible **Quand** l'analyse des stades est demandée
**Alors** le système produit une synthèse par stade ou taxon/stade

**Étant donné** zone géographique définie et taxons observés disponibles **Quand** l'identification des absences est demandée
**Alors** le système liste les espèces attendues dans la zone et non observées dans les données, avec la source de référence citée et le niveau de confiance indiqué

---

## UC-SL-13 — Analyser les variables environnementales CTD

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** contexte validé, données chargées, mode Analyse actif

**Main success scenario :**
1. L'utilisateur demande une analyse des conditions environnementales associées aux observations.
2. Le système identifie les variables disponibles : température, salinité, oxygène, fluorescence, nitrate, profondeur, temps, position.
3. Le système vérifie la source CTD utilisée et la méthode de jointure si les données viennent de plusieurs sources.
4. Le système produit des profils ou résumés environnementaux adaptés au contexte.
5. Le système signale les limites, notamment les deltas de jointure en profondeur, temps ou position.

**Extensions :**

2a. Aucune variable CTD disponible : le système signale que l'analyse environnementale est impossible.

3a. Jointure non validée : le système présente l'analyse comme exploratoire ou demande validation.

4a. L'utilisateur choisit une variable CTD précise : le système limite l'analyse à cette variable.

**Critères d'acceptation :**

**Étant donné** variables CTD disponibles **Quand** l'analyse environnementale est demandée
**Alors** le système produit une synthèse avec unités, sources et profondeur associée

**Étant donné** une jointure CTD utilisée
**Alors** le système conserve et affiche les deltas de jointure pertinents

---

## UC-SL-14 — Évaluer la complétude des données et synthétiser les lacunes

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** contexte validé, données chargées, mode Analyse actif

**Note :** Ce use case couvre la couverture au niveau des **variables mesurées** et la **synthèse globale des lacunes**. L'analyse des lacunes spatio-temporelles est couverte dans UC-SL-11. L'identification des absences taxonomiques est couverte dans UC-SL-12.

**Main success scenario :**
1. L'utilisateur demande une évaluation de la complétude de ses données pour son périmètre scientifique.
2. Le système évalue le taux de remplissage de chaque colonne clé : variables présentes, partiellement remplies, ou absentes.
3. Le système identifie les variables critiques inutilisables et en explique la conséquence pour les analyses (ex : volume échantillonné absent → calcul de concentration impossible).
4. Le système produit un rapport de lacunes structuré : ce qui est disponible, ce qui est manquant, ce qui est inutilisable et pourquoi.
5. L'utilisateur peut utiliser ce rapport pour orienter les analyses, planifier des collectes ou préparer une demande de subvention.

**Extensions :**

2a. Aucune colonne clé identifiable : le système demande à l'utilisateur de préciser les variables d'intérêt.

3a. Variable critique manquante partout : le système la signale comme bloquante et indique l'alternative disponible si elle existe.

4a. L'utilisateur veut affiner par dimension : le système peut produire un sous-rapport limité à la complétude taxonomique, spatiale, temporelle ou instrumentale.

**Critères d'acceptation :**

**Étant donné** données chargées **Quand** l'évaluation de complétude est demandée
**Alors** le système produit un tableau de remplissage par colonne clé, avec le statut de chaque variable : disponible, partielle ou absente

**Étant donné** une variable critique absente
**Alors** le système l'identifie comme bloquante, explique quelle analyse est impossible et indique si une alternative existe

**Étant donné** rapport de lacunes produit
**Alors** il distingue explicitement disponible, manquant et inutilisable, et peut être exporté comme support pour une demande de subvention

---

## UC-SL-15 — Calculer une variable dérivée

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** données chargées, mode Analyse actif

**Main success scenario :**
1. L'utilisateur décrit la variable qu'il veut obtenir et son contexte scientifique.
2. Le système identifie les variables sources disponibles dans les données.
3. Le système propose une méthode de calcul et la soumet à l'utilisateur.
4. L'utilisateur valide la méthode.
5. Le système calcule la variable et l'ajoute aux données de la session.

**Extensions :**

2a. Variables sources manquantes : manques signalés, alternatives proposées si possible.

4a. L'utilisateur conteste la méthode : le système ajuste et soumet à nouveau.

**Critères d'acceptation :**

**Étant donné** variable décrite avec contexte scientifique **Quand** méthode proposée
**Alors** validation demandée avant exécution

**Étant donné** méthode validée
**Alors** variable calculée, ajoutée aux données de la session

**Étant donné** variables sources manquantes
**Alors** manques signalés, aucun calcul exécuté

---

## UC-SL-16 — Exporter la session d'analyse

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** session active avec au moins une analyse produite

**Main success scenario :**
1. L'utilisateur demande un export de la session.
2. Le système compile le contexte scientifique, les hypothèses explorées et les analyses produites.
3. Le système génère un fichier export.
4. L'utilisateur télécharge le fichier.

**Extensions :**

2a. Aucune analyse produite : export signalé comme vide.

3a. L'utilisateur choisit le format d'export (PDF, CSV, JSON).

**Critères d'acceptation :**

**Étant donné** session avec au moins une analyse **Quand** export demandé
**Alors** contexte, hypothèses et analyses compilés dans un fichier téléchargeable

**Étant donné** aucune analyse produite **Quand** export demandé
**Alors** export signalé comme vide

---

## UC-SL-17 — Préparer un livrable scientifique

**System :** Assistant scientifique copépodes

**Primary Actor :** Utilisateur

**Goal Level :** Sea level

**Précondition :** session active avec au moins une analyse ou un graphique produit

**Main success scenario :**
1. L'utilisateur demande un livrable scientifique à partir des résultats de la session.
2. Le système rassemble automatiquement le contexte scientifique, les données utilisées, les analyses, les graphiques, les méthodes, les citations et les limites.
3. Le système propose un livrable adapté à l'usage : dossier de résultats, synthèse de présentation, annexe méthodologique ou support pour demande de subvention.
4. Le système prépare les titres de graphiques, légendes, citations courtes et citations complètes.
5. L'utilisateur valide, corrige ou ajuste le format.
6. Le système génère le livrable final.

**Extensions :**

2a. Contexte scientifique absent : le système demande de compléter ou valider le contexte avant de générer le livrable.

2b. Source ou méthode non tracée : le système signale que la citation ou la méthode doit être complétée.

3a. Analyse incomplète : le système distingue les résultats confirmés, exploratoires et manquants.

5a. L'utilisateur veut un format spécifique : le système adapte le livrable au format demandé.

**Critères d'acceptation :**

**Étant donné** au moins une analyse produite **Quand** livrable demandé
**Alors** le système génère un livrable structuré avec contexte, résultats, figures, titres, légendes, citations et limites

**Étant donné** une information manquante pour un titre, une légende ou une citation
**Alors** le système la signale explicitement au lieu de l'inventer

**Étant donné** une analyse incomplète
**Alors** le livrable distingue les résultats confirmés, exploratoires et manquants

---

## Contraintes transversales

Les contraintes détaillées de l'agent sont documentées dans :

```text
STAGE ULAVAL/Agent/Spec de L'agent/Contraintes agent V1.md
```

**CT-01 — Citation des sources**

Toute analyse ou résultat produit par le système doit citer les sources de données utilisées.

**CT-02 — Transparence du code**

L'utilisateur peut à tout moment demander à voir le code ou la méthode utilisée pour produire un résultat.

**CT-03 — Prévention de la paresse intellectuelle**

Le système ne génère pas d'analyse sans contexte scientifique défini. Il pousse l'utilisateur à formuler sa démarche avant d'agir.

**CT-04 — Formats et taille des données acceptés**

Le système accepte uniquement les formats documentés. Tout fichier dépassant la taille maximale définie est refusé avec un message explicite.

---
