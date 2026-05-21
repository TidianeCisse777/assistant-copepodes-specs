// ================================================================
//  data.js — Données de la visualisation
//  Assistant scientifique copépodes · NeoLab · Université Laval
//
//  CE FICHIER EST LA SEULE SOURCE À MODIFIER.
//  index.html contient uniquement le rendu D3 — ne pas y toucher.
//
// ----------------------------------------------------------------
//  AJOUTER UN USE CASE — checklist complète
// ----------------------------------------------------------------
//
//  1. USE_CASES (ce fichier)
//     → Ajouter une entrée "UC-SL-XX": { title, category, description,
//       actors, preconditions, flow, postconditions, scope }
//     → category : "platform" | "data" | "science" | "output"
//
//  2. TREE_DATA (ce fichier, section tout en bas)
//     → Ajouter un nœud dans le bon objectif (SLA ou SLB) :
//       { id: "UC-SL-XX", type: "usecase", children: [ ... ] }
//     → Les enfants sont les capacités (AG-V1-XX), elles-mêmes
//       parentes des docs RAG.
//     → Si un UC est partagé entre SLA et SLB : dupliquer le nœud
//       avec un id suffixé "_slb" et un champ ucId: "UC-SL-XX".
//
//  3. CAPABILITIES (ce fichier, si nouvelle capacité nécessaire)
//     → Ajouter "AG-V1-XX": { title, description, usecases, ragdocs }
//
//  4. Documents RAG (ce fichier, si nouveau doc nécessaire)
//     → Ajouter dans RAG_DOCS : { title, description, path }
//
//  5. Fichiers specs (hors visualisation — sync manuelle)
//     → Use Cases — Assistant scientifique copépodes V1.md
//     → Validation rédactionnelle — Use Cases V1.md
//     → Capacites agent V1.md (si nouvelle capacité)
//     → Validation rédactionnelle — Capacités agent V1.md
//     → Contraintes agent V1.md (si nouvelle contrainte)
//     → sources_en_ligne.md (si nouvelle source activée)
//
// ----------------------------------------------------------------
//  MODIFIER UN TITRE OU UNE DESCRIPTION
// ----------------------------------------------------------------
//     → Éditer USE_CASES, CAPABILITIES, RAG_DOCS, CONSTRAINTS ou
//       BUSINESS_OBJECTIVES selon le cas.
//     → Si le titre d'un UC change : mettre à jour aussi TREE_DATA
//       (le nœud n'a pas de titre propre — il hérite de USE_CASES
//       via l'identifiant id / ucId).
//
//  Version : V1.1 (mai 2026)
// ================================================================

// ================================================================
//  USE CASES  (UC-SL-00 à UC-SL-17)
// ================================================================

const USE_CASES = {
  "UC-SL-00": {
    title: "Inscription",
    category: "platform",
    description: "Création d'un compte utilisateur sur la plateforme.",
    actors: ["Chercheur", "Étudiant gradué", "Technicien"],
    preconditions: "Aucune.",
    flow: "L'utilisateur accède à la page d'inscription, renseigne ses informations et crée son compte.",
    postconditions: "Compte créé, accès à la connexion disponible.",
    scope: "Hors périmètre de l'agent — fonctionnalité plateforme uniquement."
  },
  "UC-SL-01": {
    title: "Connexion",
    category: "platform",
    description: "Authentification d'un utilisateur existant sur la plateforme.",
    actors: ["Chercheur", "Étudiant gradué", "Technicien"],
    preconditions: "Compte existant.",
    flow: "L'utilisateur saisit ses identifiants et accède à son espace de travail.",
    postconditions: "Session ouverte, accès à l'agent disponible.",
    scope: "Hors périmètre de l'agent — fonctionnalité plateforme uniquement."
  },
  "UC-SL-02": {
    title: "Sélectionner le mode de travail",
    category: "data",
    description: "L'utilisateur choisit entre Mode Contexte (discussion guidée, aucune exécution) et Mode Analyse (formulaire structuré, exécution validée avant lancement).",
    actors: ["Chercheur", "Étudiant gradué"],
    preconditions: "Session ouverte.",
    flow: "1. L'utilisateur sélectionne le mode via l'interface.\n2. L'agent adapte son comportement (vocabulaire, interactions, formulaires).",
    postconditions: "Mode actif, comportement de l'agent ajusté.",
    scope: "Mode Contexte : questions guidées, reformulation, pas de code. Mode Analyse : formulaire → validation → rapport statique."
  },
  "UC-SL-03": {
    title: "Charger des données",
    category: "data",
    description: "L'utilisateur charge un ou plusieurs fichiers de données locaux (CSV, Excel, JSON, exports R/Python) dans la session de travail.",
    actors: ["Chercheur", "Technicien"],
    preconditions: "Session ouverte, fichiers disponibles localement.",
    flow: "1. L'utilisateur sélectionne les fichiers.\n2. L'agent inspecte les colonnes, types, unités, valeurs manquantes.\n3. Un rapport de validation est retourné.",
    postconditions: "Données chargées, profil de données disponible pour l'analyse.",
    scope: "Formats acceptés : CSV, XLSX, JSON, exports EcoTaxa/EcoPart. Structure inconnue jusqu'à inspection."
  },
  "UC-SL-04": {
    title: "Interroger des sources en ligne",
    category: "data",
    description: "L'utilisateur active une source en ligne (EcoTaxa, EcoPart, OBIS, CMEMS, Amundsen CTD via ERDDAP) et lance une requête paramétrée.",
    actors: ["Chercheur"],
    preconditions: "Source identifiée, paramètres de requête définis, credentials disponibles si requis.",
    flow: "1. L'utilisateur sélectionne la source et les paramètres.\n2. L'agent valide les paramètres contre les contraintes de la source.\n3. Les données sont récupérées et chargées dans la session.",
    postconditions: "Données en ligne disponibles, profil affiché.",
    scope: "Sources : EcoTaxa API, EcoPart API, ERDDAP (Amundsen CTD), OBIS API, CMEMS (compte gratuit requis)."
  },
  "UC-SL-05": {
    title: "Valider les données chargées",
    category: "data",
    description: "L'agent inspecte les données chargées (colonnes, types, unités, valeurs manquantes, cohérence) et retourne un rapport de validation structuré.",
    actors: ["Chercheur", "Technicien"],
    preconditions: "Données chargées dans la session.",
    flow: "1. L'agent liste les colonnes disponibles avec leur type et unité.\n2. Il identifie les valeurs manquantes, anomalies, colonnes non reconnues.\n3. Rapport structuré avec niveau de confiance par colonne.",
    postconditions: "Rapport de validation disponible, colonnes documentées.",
    scope: "Ne modifie pas les données brutes (CT-AG-10). Signale mais ne corrige pas les anomalies."
  },
  "UC-SL-06": {
    title: "Nettoyer les données",
    category: "data",
    description: "L'agent applique des transformations de nettoyage validées par l'utilisateur (filtrage, renommage, conversion d'unités) sur une copie des données.",
    actors: ["Chercheur"],
    preconditions: "Données validées, méthode de nettoyage soumise et approuvée.",
    flow: "1. L'agent propose une méthode de nettoyage.\n2. L'utilisateur valide ou modifie.\n3. L'agent applique sur une copie (jamais les originaux).\n4. Rapport des transformations appliquées.",
    postconditions: "Données nettoyées disponibles, transformations documentées.",
    scope: "Données brutes jamais modifiées (CT-AG-10). Méthode soumise avant exécution (CT-AG-06)."
  },
  "UC-SL-07": {
    title: "Décrire le contexte scientifique",
    category: "science",
    description: "En Mode Contexte, l'agent guide l'utilisateur par des questions structurées pour formuler sa question scientifique, ses hypothèses et le périmètre des données à mobiliser.",
    actors: ["Chercheur", "Étudiant gradué"],
    preconditions: "Mode Contexte actif.",
    flow: "1. L'agent pose des questions guidées (espèce cible, zone géographique, variable d'intérêt, période).\n2. L'utilisateur répond et reformule.\n3. L'agent synthétise le contexte et le soumet pour validation.",
    postconditions: "Contexte scientifique validé, prêt pour le passage en Mode Analyse.",
    scope: "Aucun code exécuté. Aucune analyse produite. Discussion uniquement (CT-AG-25)."
  },
  "UC-SL-08": {
    title: "Valider la reformulation du contexte",
    category: "science",
    description: "L'agent présente une reformulation structurée du contexte scientifique. L'utilisateur valide ou corrige avant de passer à l'analyse.",
    actors: ["Chercheur"],
    preconditions: "Contexte décrit (UC-SL-07 complété).",
    flow: "1. L'agent présente : question reformulée, hypothèses, données mobilisées, limites anticipées.\n2. L'utilisateur valide ou corrige.\n3. Validation → transition vers Mode Analyse.",
    postconditions: "Contexte verrouillé, Mode Analyse activable.",
    scope: "Le contexte validé est tracé et inclus dans les livrables finaux."
  },
  "UC-SL-09": {
    title: "Générer un graphique",
    category: "science",
    description: "L'agent génère une visualisation scientifique à partir des données chargées, avec titre, axes, unités, source, filtres et limites explicites.",
    actors: ["Chercheur", "Étudiant gradué"],
    preconditions: "Données chargées, contexte validé, paramètres de graphique définis.",
    flow: "1. L'utilisateur spécifie le type de graphique et les variables.\n2. L'agent soumet la méthode pour validation.\n3. Le graphique est généré et affiché comme rapport statique.",
    postconditions: "Graphique disponible avec métadonnées complètes.",
    scope: "Tout graphique exploratoire doit être clairement étiqueté comme tel. Aucun graphique sans source tracée (CT-AG-14)."
  },
  "UC-SL-10": {
    title: "Analyser la distribution verticale",
    category: "science",
    description: "L'agent analyse la distribution en profondeur des copépodes à partir des données EcoTaxa/EcoPart, avec jointure validée et concentration calculée.",
    actors: ["Chercheur"],
    preconditions: "EcoTaxa 1165 + EcoPart 105 chargés, jointure profile_id validée.",
    flow: "1. L'agent effectue la jointure EcoTaxa ↔ EcoPart par profile_id et profondeur (±5m).\n2. Il calcule la concentration (ind/m³) et la biovolume.\n3. Il génère les profils verticaux par taxon/stade.\n4. Rapport statique avec sources, méthodes, limites.",
    postconditions: "Profils de distribution verticale disponibles, méthode documentée.",
    scope: "Jointure EcoTaxa ↔ EcoPart validée sur données test. LOKI (2331) sans morphométrie individuelle."
  },
  "UC-SL-11": {
    title: "Analyser la distribution et les lacunes spatio-temporelles",
    category: "science",
    description: "L'agent analyse la répartition spatiale et temporelle des copépodes entre stations et campagnes, et identifie les zones ou périodes sans données.",
    actors: ["Chercheur"],
    preconditions: "Données avec coordonnées (lat/lon) et dates disponibles.",
    flow: "1. L'agent identifie les variables spatiales et temporelles disponibles.\n2. Il construit les tables de travail.\n3. Il génère les cartes, graphiques temporels et carte des lacunes si demandé.",
    postconditions: "Cartes, séries temporelles et gaps identifiés avec métadonnées.",
    scope: "OBIS pour contexte géographique global. Extension : carte des zones sans données et timeline des gaps entre campagnes."
  },
  "UC-SL-12": {
    title: "Analyser la taxonomie, les stades et les absences",
    category: "science",
    description: "L'agent analyse la composition taxonomique, la répartition par stades, et identifie les espèces attendues dans la zone mais absentes des données.",
    actors: ["Chercheur", "Étudiant gradué"],
    preconditions: "Données annotées (statut V — validé) disponibles.",
    flow: "1. L'agent filtre sur object_annotation_status = V (validé uniquement).\n2. Il analyse la composition par taxon et stade.\n3. Sur demande, il compare avec les espèces attendues via OBIS et corpus RAG.\n4. Il signale les absences et les limites d'identification.",
    postconditions: "Tableaux de composition taxonomique, absences documentées avec niveau de confiance.",
    scope: "C. glacialis vs C. finmarchicus : identification moléculaire requise. Absences : distinguer absence confirmée, biais d'échantillonnage, incertitude (CT-AG-29)."
  },
  "UC-SL-13": {
    title: "Analyser les variables environnementales CTD",
    category: "science",
    description: "L'agent analyse les variables CTD (température, salinité, oxygène, fluorescence, nitrate) et les associe aux données biologiques.",
    actors: ["Chercheur"],
    preconditions: "CTD Amundsen (ERDDAP) ou EcoPart disponible, jointure par proximité validée.",
    flow: "1. L'agent récupère/charge les données CTD.\n2. Il effectue la jointure par proximité (date/heure/lat/lon/profondeur).\n3. Il calcule les profils et croise avec les données biologiques.",
    postconditions: "Profils CTD disponibles, association biologie-environnement documentée.",
    scope: "Jointure EcoPart ↔ Amundsen validée sur ips_007. Tolérance : temps <5min, position <0.001°, profondeur <0.5m."
  },
  "UC-SL-14": {
    title: "Évaluer la complétude des données et synthétiser les lacunes",
    category: "science",
    description: "L'agent évalue le taux de remplissage des colonnes clés, identifie les variables critiques inutilisables, compare avec OBIS si activé, et produit un rapport de lacunes exportable.",
    actors: ["Chercheur"],
    preconditions: "Données chargées, contexte validé, mode Analyse actif.",
    flow: "1. L'agent évalue le taux de remplissage par colonne clé.\n2. Il identifie les variables critiques inutilisables et explique les analyses bloquées.\n3. Si OBIS activé et zone définie, il compare la couverture locale aux données de référence.\n4. Il produit un rapport distinguant disponible / manquant / inutilisable.",
    postconditions: "Rapport de lacunes structuré, exportable pour demande de subvention.",
    scope: "Lacunes spatio-temporelles → UC-SL-11. Absences taxonomiques → UC-SL-12. Ce UC : complétude des variables et synthèse globale."
  },
  "UC-SL-15": {
    title: "Calculer une variable dérivée",
    category: "science",
    description: "L'agent calcule une variable dérivée (concentration, biomasse, indice de plénitude lipidique, longueur prosome) avec validation de la méthode avant exécution.",
    actors: ["Chercheur"],
    preconditions: "Colonnes source disponibles, méthode de calcul identifiée.",
    flow: "1. L'utilisateur spécifie la variable à calculer.\n2. L'agent vérifie la disponibilité des colonnes requises.\n3. Il soumet la méthode pour validation.\n4. Il exécute et retourne le résultat documenté.",
    postconditions: "Variable calculée, formule et colonnes source documentées.",
    scope: "Volume échantillonné uniquement dans EcoPart — requis pour concentration. acq_pixel requis pour conversion pixels→mm."
  },
  "UC-SL-16": {
    title: "Exporter l'analyse de session",
    category: "output",
    description: "L'agent compile un résumé complet de la session : contexte, sources mobilisées, méthodes appliquées, résultats, limites.",
    actors: ["Chercheur", "Étudiant gradué"],
    preconditions: "Session avec au moins une analyse complétée.",
    flow: "1. L'agent compile le résumé de session.\n2. Il structure : contexte → sources → méthodes → résultats → limites.\n3. L'utilisateur valide et exporte.",
    postconditions: "Résumé exporté, session documentée.",
    scope: "Format structuré, non narratif. Sources toutes citées, méthodes toutes tracées."
  },
  "UC-SL-17": {
    title: "Préparer un livrable scientifique",
    category: "output",
    description: "L'agent génère un livrable structuré (contexte, résultats, figures, méthodes, citations, limites) pour révision humaine ou demande de subvention.",
    actors: ["Chercheur"],
    preconditions: "Analyses complétées, contexte validé.",
    flow: "1. L'agent sélectionne les analyses à inclure.\n2. Il génère : contexte, résultats par use case, figures, méthodes, citations, limites.\n3. Il signale explicitement tout résultat manquant ou non concluant.",
    postconditions: "Livrable structuré disponible pour révision humaine.",
    scope: "Ne jamais inventer de citations (CT-AG-15). Livrable = support de révision, pas publication finale."
  }
};

// ================================================================
//  CAPACITÉS AGENT  (AG-V1-01 à AG-V1-14)
// ================================================================

const CAPABILITIES = {
  "AG-V1-01": {
    title: "Comprendre les sources disponibles",
    description: "L'agent distingue les sources activées (EcoTaxa, EcoPart, Amundsen CTD, OBIS, CMEMS, fichiers lab) et explique leurs contenus, formats, clés de jointure et limitations.",
    constraints: ["CT-AG-01", "CT-AG-08"],
    ragDocs: ["colonnes_sources", "sources_en_ligne"]
  },
  "AG-V1-02": {
    title: "Aider à formuler le contexte scientifique",
    description: "En Mode Contexte, l'agent guide l'utilisateur par des questions structurées pour préciser l'espèce cible, la zone géographique, la variable d'intérêt, la période et les hypothèses.",
    constraints: ["CT-AG-04", "CT-AG-25", "CT-AG-26"],
    ragDocs: ["copepodes_domaine"]
  },
  "AG-V1-03": {
    title: "Valider les données chargées",
    description: "L'agent inspecte les données : liste des colonnes, types, unités, valeurs manquantes, cohérence. Retourne un rapport structuré avec niveau de confiance par colonne.",
    constraints: ["CT-AG-03", "CT-AG-05", "CT-AG-10"],
    ragDocs: ["colonnes_sources", "colonnes_instruments"]
  },
  "AG-V1-04": {
    title: "Interroger les sources activées",
    description: "L'agent exécute des requêtes sur les sources en ligne avec les paramètres validés par l'utilisateur, en respectant les limitations (volume, credentials, scope V1).",
    constraints: ["CT-AG-08", "CT-AG-11", "CT-AG-12"],
    ragDocs: ["sources_en_ligne"]
  },
  "AG-V1-05": {
    title: "Expliquer les colonnes et unités",
    description: "L'agent fournit la définition, l'unité, le niveau de confiance et les distinctions critiques de toute colonne demandée, avec citation de la source.",
    constraints: ["CT-AG-01", "CT-AG-03", "CT-AG-27"],
    ragDocs: ["colonnes_sources", "colonnes_instruments"]
  },
  "AG-V1-06": {
    title: "Construire des tables de travail",
    description: "L'agent joint plusieurs sources en documentant les clés de jointure utilisées, les colonnes de sortie, la stratégie et les pertes de données.",
    constraints: ["CT-AG-05", "CT-AG-07", "CT-AG-10"],
    ragDocs: ["colonnes_sources"]
  },
  "AG-V1-07": {
    title: "Calculer des variables dérivées",
    description: "L'agent calcule des métriques dérivées (concentration ind/m³, biomasse mg C/m², indice lipidique, longueur prosome) avec validation de la méthode avant exécution et traçabilité complète.",
    constraints: ["CT-AG-05", "CT-AG-06", "CT-AG-20"],
    ragDocs: ["methodes_calcul"]
  },
  "AG-V1-08": {
    title: "Générer des graphiques scientifiques",
    description: "L'agent produit des graphiques avec titre, axes titrés, unités, source de données, filtres appliqués et limites explicites. Résultat affiché comme rapport statique.",
    constraints: ["CT-AG-14", "CT-AG-13", "CT-AG-01"],
    ragDocs: ["methodes_calcul", "colonnes_sources"]
  },
  "AG-V1-09": {
    title: "Produire une analyse exploratoire",
    description: "L'agent exécute des analyses (distribution, composition, corrélation) en distinguant explicitement observation, interprétation et hypothèse dans le rapport.",
    constraints: ["CT-AG-13", "CT-AG-19", "CT-AG-24"],
    ragDocs: ["colonnes_sources", "methodes_calcul"]
  },
  "AG-V1-10": {
    title: "Évaluer la complétude et synthétiser les lacunes",
    description: "L'agent évalue le taux de remplissage des colonnes clés, identifie les variables critiques inutilisables, compare avec OBIS si activé, et produit un rapport de lacunes structuré exportable.",
    constraints: ["CT-AG-01", "CT-AG-03", "CT-AG-29"],
    ragDocs: ["sources_en_ligne", "copepodes_domaine"]
  },
  "AG-V1-11": {
    title: "Répondre aux questions de domaine copépodes",
    description: "L'agent répond aux questions biologiques (espèces, stades, lipides, diapause, rôle écologique) en s'appuyant sur le corpus RAG et en signalant l'incertitude.",
    constraints: ["CT-AG-19", "CT-AG-27", "CT-AG-02"],
    ragDocs: ["copepodes_domaine"]
  },
  "AG-V1-12": {
    title: "Exporter les résumés de session",
    description: "L'agent compile un résumé structuré de la session (contexte, sources, méthodes, résultats, limites) sans narration excessive.",
    constraints: ["CT-AG-20", "CT-AG-01", "CT-AG-18"],
    ragDocs: []
  },
  "AG-V1-13": {
    title: "Préparer les livrables scientifiques",
    description: "L'agent génère un livrable structuré (contexte, résultats, figures, méthodes, citations, limites) pour soutenir la révision humaine et les demandes de subvention.",
    constraints: ["CT-AG-15", "CT-AG-28", "CT-AG-01", "CT-AG-20"],
    ragDocs: ["copepodes_domaine", "methodes_calcul", "colonnes_sources"]
  },
  "AG-V1-14": {
    title: "Interface adaptée au mode de travail",
    description: "L'agent adapte son interface et son comportement selon le mode actif : discussion guidée en Mode Contexte, formulaire structuré → rapport statique en Mode Analyse.",
    constraints: ["CT-AG-23", "CT-AG-24", "CT-AG-26"],
    ragDocs: []
  }
};

// ================================================================
//  DOCUMENTS RAG  (5 fichiers)
// ================================================================

const RAG_DOCS = {
  "colonnes_sources": {
    title: "colonnes_sources.md",
    shortTitle: "Colonnes des sources",
    description: "Explique les colonnes des exports réels : EcoTaxa 1165 (UVP5 Amundsen 2018), EcoTaxa 2331 (LOKI copépodes lipides), EcoPart 105, Amundsen CTD. Inclut les stratégies de jointure et les pièges courants.",
    chunks: 8,
    usage: "Quand l'utilisateur demande « que signifie cette colonne ? », « comment joindre ces sources ? », « quelles variables sont disponibles ? »",
    keyContent: "obj_orig_id / profile_id (clé de jointure EcoTaxa↔EcoPart), object_depth_min/max, taxon, fre_feret, Profile, Sampled volume [L], TE90/PSAL/OXYM/FLOR/NTRA"
  },
  "colonnes_instruments": {
    title: "colonnes_instruments.md",
    shortTitle: "Colonnes par instrument",
    description: "Dictionnaire complet des colonnes EcoTaxa par instrument (UVP5, UVP6, ZooScan). Colonnes de métadonnées (sample_*, acq_*, process_*) et de mesure (object_*).",
    chunks: 9,
    usage: "Quand l'utilisateur demande « comment identifier l'instrument ? », « que signifie object_feret ? », « comment convertir les pixels ? »",
    keyContent: "acq_pixel (dimension pixel en mm — obligatoire pour conversion taille), object_mean (proxy opacité), object_area, object_feret (diamètre de Feret)"
  },
  "copepodes_domaine": {
    title: "copepodes_domaine.md",
    shortTitle: "Domaine copépodes",
    description: "Connaissances biologiques : espèces (C. hyperboreus, C. glacialis, C. finmarchicus, Metridia, Oithona, Pseudocalanus, Temora, Eurytemora), stades de vie (N1-N6, C1-C5, AF/AM), diapause, métabolisme lipidique, groupes fonctionnels, rôle dans la pompe à carbone.",
    chunks: 13,
    usage: "Quand l'utilisateur demande « quel est le rôle de ce copépode ? », « que signifient les lipides ? », « comment contribuent-ils à l'export de carbone ? »",
    keyContent: "⚠ Problème critique : C. glacialis vs C. finmarchicus morphologiquement identiques dans les zones de chevauchement — marqueurs moléculaires requis pour identification fiable."
  },
  "methodes_calcul": {
    title: "methodes_calcul.md",
    shortTitle: "Méthodes de calcul",
    description: "Méthodes de calcul des métriques scientifiques : concentration (ind/m³), biomasse (mg C/m²), indice de plénitude lipidique, longueur prosome, association CTD. Chaque méthode inclut formule, colonnes requises, unités, limites et feedback si données insuffisantes.",
    chunks: 10,
    usage: "Quand l'utilisateur demande « comment calculer X ? », « pourquoi ne puis-je pas calculer X ? », « que me manque-t-il ? »",
    keyContent: "Concentration = N_objets / Sampled_volume [L] × 1000. Volume sampled uniquement dans EcoPart. Biomasse : longueur prosome → masse sèche → carbone."
  },
  "sources_en_ligne": {
    title: "sources_en_ligne.md",
    shortTitle: "Sources en ligne",
    description: "Où trouver chaque source, méthodes d'accès, détails API, comptes requis. Arbre de décision : quelle source pour quelle question ? Aucun credential stocké dans ce fichier.",
    chunks: 7,
    usage: "Quand l'utilisateur demande « où est-ce que je trouve X ? », « ai-je besoin d'un compte ? », « quel jeu de données utiliser ? »",
    keyContent: "EcoTaxa/EcoPart : API avec token. ERDDAP Amundsen : accès public. OBIS : API publique. CMEMS : compte gratuit requis. Projets EcoTaxa : 1165 (UVP5 Amundsen), 2331 (LOKI)"
  }
};

// ================================================================
//  CONTRAINTES AGENT  (CT-AG-01 à CT-AG-29)
// ================================================================

const CONSTRAINTS = [
  { id: "CT-AG-01", title: "Toujours citer les sources utilisées", description: "Chaque résultat doit être accompagné de la référence à la source de données utilisée (fichier, projet, API, DOI)." },
  { id: "CT-AG-02", title: "Ne jamais inventer de données absentes", description: "Si une donnée n'est pas disponible dans les sources actives, l'agent le dit explicitement. Aucune valeur imputée sans validation." },
  { id: "CT-AG-03", title: "Distinguer résultats fiables, exploratoires et impossibles", description: "Chaque résultat est classé : fiable (données complètes validées), exploratoire (données partielles ou non validées), impossible (données absentes ou insuffisantes)." },
  { id: "CT-AG-04", title: "Exiger le contexte scientifique avant l'analyse", description: "Aucune analyse exécutée sans contexte validé (espèce, zone, variable, période, hypothèse). L'agent pose les questions manquantes." },
  { id: "CT-AG-05", title: "Valider colonnes et unités avant calcul", description: "Toutes les colonnes utilisées dans un calcul doivent être identifiées, leur type et unité vérifiés avant l'exécution." },
  { id: "CT-AG-06", title: "Soumettre la méthode avant exécution", description: "L'agent présente la méthode (colonnes, formule, paramètres) pour validation explicite de l'utilisateur avant tout calcul ou graphique." },
  { id: "CT-AG-07", title: "Tracer les jointures entre sources", description: "Toute jointure entre sources est documentée : clé utilisée, tolérance, pertes, qualité de la correspondance." },
  { id: "CT-AG-08", title: "Respecter les limitations des sources", description: "Chaque source a des contraintes documentées (couverture, résolution, période). L'agent les communique explicitement." },
  { id: "CT-AG-09", title: "Encadrer l'exécution du code", description: "Le code exécuté est traçable, explicable et limité à la session. Les erreurs sont expliquées, pas cachées." },
  { id: "CT-AG-10", title: "Préserver les données brutes", description: "Les données brutes chargées ne sont jamais modifiées. Toute transformation s'applique sur une copie explicitement nommée." },
  { id: "CT-AG-11", title: "Gérer les credentials sans exposition", description: "Les tokens, mots de passe et credentials ne sont jamais affichés, loggés ou inclus dans les livrables." },
  { id: "CT-AG-12", title: "Limiter les téléchargements", description: "Les requêtes sur sources en ligne sont proportionnées à la question. Pas de téléchargement massif non justifié." },
  { id: "CT-AG-13", title: "Ne pas sur-interpréter", description: "L'agent sépare clairement : observation (ce que montrent les données), interprétation (ce que cela suggère), hypothèse (ce que cela pourrait signifier si confirmé)." },
  { id: "CT-AG-14", title: "Produire des graphiques lisibles et sourcés", description: "Tout graphique inclut : titre/intention, axes titrés, unités, source de données, filtre/périmètre, limites importantes." },
  { id: "CT-AG-15", title: "Préparer les livrables sans inventer de citations", description: "Les références bibliographiques dans les livrables sont tirées des données et du corpus RAG uniquement. Aucune citation inventée." },
  { id: "CT-AG-16", title: "Respecter le scope V1", description: "Périmètre V1 : exploration, validation, analyses standard, graphiques simples, livrables structurés. Pas de modèles prédictifs ni d'automatisation complète." },
  { id: "CT-AG-17", title: "Configurer le modèle pour variabilité réduite", description: "Temperature = 0.0 pour la reproductibilité des analyses. Configuration documentée dans les livrables." },
  { id: "CT-AG-18", title: "Réduire la narration générative", description: "Les réponses sont courtes, structurées et orientées résultat. Pas de texte de remplissage, pas de phrases de transition inutiles." },
  { id: "CT-AG-19", title: "Ancrer les réponses dans les données et le RAG", description: "Toute affirmation factuellement incorrecte ou non étayée par les données ou le corpus RAG est interdite." },
  { id: "CT-AG-20", title: "Tracer la provenance des résultats", description: "Chaque résultat inclut : identifiant de fichier/source, ligne ou profil concerné, colonne, DOI ou URL, timestamp de récupération." },
  { id: "CT-AG-21", title: "Vérifier la cohérence entre output et données source", description: "L'agent vérifie que les sorties (tableaux, chiffres, graphiques) sont cohérentes avec les données sources avant présentation." },
  { id: "CT-AG-22", title: "Privilégier le traitement asynchrone pour analyses lourdes", description: "Les analyses longues sont traitées en job asynchrone, pas en chat instantané. Le résultat est retourné comme rapport statique." },
  { id: "CT-AG-23", title: "Séparer les interfaces Contexte et Analyse", description: "Mode Contexte = chat guidé (questions ouvertes). Mode Analyse = formulaire structuré → bouton validation → rapport statique. Pas de champs texte libres en Mode Analyse." },
  { id: "CT-AG-24", title: "Supprimer le streaming de texte dans les rapports", description: "Les rapports d'analyse sont affichés comme blocs statiques complets. Pas de streaming progressif." },
  { id: "CT-AG-25", title: "Imposer un ticket d'entrée cognitif", description: "Avant toute analyse, l'agent exige un minimum de contexte (espèce, zone, variable, période). Bloque si contexte insuffisant." },
  { id: "CT-AG-26", title: "Vocabulaire clinique, non anthropomorphique", description: "Pas de « je », pas d'expressions de chaleur ou d'enthousiasme. Vocabulaire technique, neutre, clinique." },
  { id: "CT-AG-27", title: "Rendre l'incertitude visible", description: "Les niveaux de confiance sont affichés explicitement (fiable / exploratoire / impossible). Code couleur si applicable." },
  { id: "CT-AG-28", title: "Encadrer la réutilisation des livrables", description: "Les livrables incluent sources, méthodes et limites. L'utilisateur est informé des conditions de réutilisation des résultats." },
  { id: "CT-AG-29", title: "Contextualiser les absences lors des comparaisons de couverture", description: "Lors d'une comparaison locale vs OBIS ou corpus RAG, distinguer explicitement : absence confirmée, absence par biais d'échantillonnage, et absence incertaine. Signaler les biais systématiques arctiques (données hivernales, C. glacialis vs C. finmarchicus). Concerne UC-SL-12 ext. 3b, UC-SL-14, AG-V1-10, AG-V1-11." }
];

// ================================================================
//  OBJECTIFS MÉTIER  (Sea Level A & B)
// ================================================================

const BUSINESS_OBJECTIVES = {
  "SLA": {
    code: "Sea Level A",
    title: "Explorer et analyser une question scientifique",
    description: "Le chercheur ou l'étudiant veut explorer une question scientifique sur les copépodes sans être bloqué par le code, les jointures ou la manipulation des données.",
    expected: "L'assistant aide à formuler le contexte, valide les données disponibles, produit des analyses standards réalistes et explique les résultats avec leurs limites.",
    success: "L'utilisateur obtient une analyse ou une visualisation exploitable, avec les sources citées et les limites scientifiques explicites."
  },
  "SLB": {
    code: "Sea Level B",
    title: "Évaluer la couverture et les lacunes des données",
    description: "Le chercheur veut comprendre ce que les données couvrent réellement et où se trouvent les manques.",
    expected: "L'assistant distingue les zones, périodes, espèces, stades, campagnes ou variables bien représentées de celles qui sont absentes ou insuffisamment couvertes.",
    success: "L'utilisateur obtient une synthèse claire de la couverture et des lacunes, utilisable pour orienter une exploration scientifique ou soutenir une demande de subvention."
  }
};

// ================================================================
//  GROUPES CATÉGORIES
// ================================================================

const CATEGORY_GROUPS = {
  "platform": { title: "Accès à la plateforme",  description: "Fonctionnalités d'accès — hors périmètre de l'agent." },
  "data":     { title: "Gestion des données",     description: "Préparation, chargement, validation et nettoyage des données." },
  "science":  { title: "Analyse scientifique",    description: "Exploration, analyse et calcul sur les données copépodes." },
  "output":   { title: "Production de livrables", description: "Export et formalisation des résultats de session." }
};

// ================================================================
//  STRUCTURE DE L'ARBRE
//  User → Objectif métier (SLA / SLB / Plateforme)
//       → Groupe catégorie (Données / Analyse / Livrable)
//       → Use Case → Capacité Agent → Document RAG
//
//  Les UC partagés entre SLA et SLB ont un suffixe _slb dans leur
//  id de nœud et un champ ucId qui pointe vers USE_CASES.
// ================================================================

const TREE_DATA = {
  id: "user", name: "Utilisateur", type: "user",
  children: [
    // ── Plateforme (hors objectifs sea level) ──
    {
      id: "grp-platform", type: "catgroup", category: "platform",
      children: [
        { id: "UC-SL-00", type: "usecase", category: "platform", children: [] },
        { id: "UC-SL-01", type: "usecase", category: "platform", children: [] }
      ]
    },

    // ── Sea Level A ──
    {
      id: "SLA", type: "objective", objId: "SLA",
      children: [
        {
          id: "SLA-data", type: "catgroup", category: "data",
          children: [
            { id: "UC-SL-02", type: "usecase", category: "data", children: [
              { id: "cap14_uc02", type: "capability", capId: "AG-V1-14", children: [] }
            ]},
            { id: "UC-SL-03", type: "usecase", category: "data", children: [
              { id: "cap03_uc03", type: "capability", capId: "AG-V1-03", children: [
                { id: "r_csrc_uc03", type: "ragdoc", ragId: "colonnes_sources",     children: [] },
                { id: "r_cins_uc03", type: "ragdoc", ragId: "colonnes_instruments", children: [] }
              ]}
            ]},
            { id: "UC-SL-04", type: "usecase", category: "data", children: [
              { id: "cap01_uc04", type: "capability", capId: "AG-V1-01", children: [
                { id: "r_src_uc04a", type: "ragdoc", ragId: "sources_en_ligne", children: [] }
              ]},
              { id: "cap04_uc04", type: "capability", capId: "AG-V1-04", children: [
                { id: "r_src_uc04b", type: "ragdoc", ragId: "sources_en_ligne", children: [] }
              ]}
            ]},
            { id: "UC-SL-05", type: "usecase", category: "data", children: [
              { id: "cap03_uc05", type: "capability", capId: "AG-V1-03", children: [
                { id: "r_csrc_uc05a", type: "ragdoc", ragId: "colonnes_sources",     children: [] },
                { id: "r_cins_uc05",  type: "ragdoc", ragId: "colonnes_instruments", children: [] }
              ]},
              { id: "cap05_uc05", type: "capability", capId: "AG-V1-05", children: [
                { id: "r_csrc_uc05b", type: "ragdoc", ragId: "colonnes_sources", children: [] }
              ]}
            ]},
            { id: "UC-SL-06", type: "usecase", category: "data", children: [
              { id: "cap03_uc06", type: "capability", capId: "AG-V1-03", children: [
                { id: "r_csrc_uc06", type: "ragdoc", ragId: "colonnes_sources", children: [] }
              ]},
              { id: "cap05_uc06", type: "capability", capId: "AG-V1-05", children: [
                { id: "r_cins_uc06", type: "ragdoc", ragId: "colonnes_instruments", children: [] }
              ]}
            ]}
          ]
        },
        {
          id: "SLA-science", type: "catgroup", category: "science",
          children: [
            { id: "UC-SL-07", type: "usecase", category: "science", children: [
              { id: "cap02_uc07", type: "capability", capId: "AG-V1-02", children: [
                { id: "r_cop_uc07", type: "ragdoc", ragId: "copepodes_domaine", children: [] }
              ]}
            ]},
            { id: "UC-SL-08", type: "usecase", category: "science", children: [
              { id: "cap02_uc08", type: "capability", capId: "AG-V1-02", children: [
                { id: "r_cop_uc08", type: "ragdoc", ragId: "copepodes_domaine", children: [] }
              ]}
            ]},
            { id: "UC-SL-09", type: "usecase", category: "science", children: [
              { id: "cap08_uc09", type: "capability", capId: "AG-V1-08", children: [
                { id: "r_meth_uc09", type: "ragdoc", ragId: "methodes_calcul",  children: [] }
              ]},
              { id: "cap06_uc09", type: "capability", capId: "AG-V1-06", children: [
                { id: "r_csrc_uc09", type: "ragdoc", ragId: "colonnes_sources", children: [] }
              ]}
            ]},
            { id: "UC-SL-10", type: "usecase", category: "science", children: [
              { id: "cap09_uc10", type: "capability", capId: "AG-V1-09", children: [
                { id: "r_csrc_uc10a", type: "ragdoc", ragId: "colonnes_sources", children: [] }
              ]},
              { id: "cap06_uc10", type: "capability", capId: "AG-V1-06", children: [
                { id: "r_csrc_uc10b", type: "ragdoc", ragId: "colonnes_sources", children: [] }
              ]},
              { id: "cap07_uc10", type: "capability", capId: "AG-V1-07", children: [
                { id: "r_meth_uc10",  type: "ragdoc", ragId: "methodes_calcul",  children: [] }
              ]}
            ]},
            { id: "UC-SL-11", type: "usecase", category: "science", children: [
              { id: "cap09_uc11", type: "capability", capId: "AG-V1-09", children: [
                { id: "r_csrc_uc11", type: "ragdoc", ragId: "colonnes_sources", children: [] }
              ]},
              { id: "cap06_uc11", type: "capability", capId: "AG-V1-06", children: [
                { id: "r_src_uc11",  type: "ragdoc", ragId: "sources_en_ligne", children: [] }
              ]}
            ]},
            { id: "UC-SL-12", type: "usecase", category: "science", children: [
              { id: "cap09_uc12", type: "capability", capId: "AG-V1-09", children: [
                { id: "r_csrc_uc12", type: "ragdoc", ragId: "colonnes_sources",  children: [] }
              ]},
              { id: "cap11_uc12", type: "capability", capId: "AG-V1-11", children: [
                { id: "r_cop_uc12",  type: "ragdoc", ragId: "copepodes_domaine", children: [] }
              ]},
              { id: "cap05_uc12", type: "capability", capId: "AG-V1-05", children: [
                { id: "r_cins_uc12", type: "ragdoc", ragId: "colonnes_instruments", children: [] }
              ]}
            ]},
            { id: "UC-SL-13", type: "usecase", category: "science", children: [
              { id: "cap09_uc13", type: "capability", capId: "AG-V1-09", children: [
                { id: "r_meth_uc13", type: "ragdoc", ragId: "methodes_calcul",  children: [] }
              ]},
              { id: "cap06_uc13", type: "capability", capId: "AG-V1-06", children: [
                { id: "r_csrc_uc13", type: "ragdoc", ragId: "colonnes_sources", children: [] }
              ]},
              { id: "cap04_uc13", type: "capability", capId: "AG-V1-04", children: [
                { id: "r_src_uc13",  type: "ragdoc", ragId: "sources_en_ligne", children: [] }
              ]}
            ]},
            { id: "UC-SL-15", type: "usecase", category: "science", children: [
              { id: "cap07_uc15", type: "capability", capId: "AG-V1-07", children: [
                { id: "r_meth_uc15",  type: "ragdoc", ragId: "methodes_calcul",      children: [] }
              ]},
              { id: "cap05_uc15", type: "capability", capId: "AG-V1-05", children: [
                { id: "r_csrc_uc15",  type: "ragdoc", ragId: "colonnes_sources",     children: [] },
                { id: "r_cins_uc15",  type: "ragdoc", ragId: "colonnes_instruments", children: [] }
              ]}
            ]}
          ]
        },
        {
          id: "SLA-output", type: "catgroup", category: "output",
          children: [
            { id: "UC-SL-17", type: "usecase", category: "output", children: [
              { id: "cap13_uc17", type: "capability", capId: "AG-V1-13", children: [
                { id: "r_cop_uc17",  type: "ragdoc", ragId: "copepodes_domaine", children: [] },
                { id: "r_meth_uc17", type: "ragdoc", ragId: "methodes_calcul",   children: [] },
                { id: "r_csrc_uc17", type: "ragdoc", ragId: "colonnes_sources",  children: [] }
              ]}
            ]}
          ]
        }
      ]
    },

    // ── Sea Level B ──
    {
      id: "SLB", type: "objective", objId: "SLB",
      children: [
        {
          id: "SLB-data", type: "catgroup", category: "data",
          children: [
            { id: "UC-SL-04_slb", ucId: "UC-SL-04", type: "usecase", category: "data", children: [
              { id: "cap01_uc04b", type: "capability", capId: "AG-V1-01", children: [
                { id: "r_src_uc04c", type: "ragdoc", ragId: "sources_en_ligne", children: [] }
              ]},
              { id: "cap04_uc04b", type: "capability", capId: "AG-V1-04", children: [
                { id: "r_src_uc04d", type: "ragdoc", ragId: "sources_en_ligne", children: [] }
              ]}
            ]},
            { id: "UC-SL-05_slb", ucId: "UC-SL-05", type: "usecase", category: "data", children: [
              { id: "cap03_uc05b", type: "capability", capId: "AG-V1-03", children: [
                { id: "r_csrc_uc05c", type: "ragdoc", ragId: "colonnes_sources",     children: [] },
                { id: "r_cins_uc05b", type: "ragdoc", ragId: "colonnes_instruments", children: [] }
              ]},
              { id: "cap05_uc05b", type: "capability", capId: "AG-V1-05", children: [
                { id: "r_csrc_uc05d", type: "ragdoc", ragId: "colonnes_sources", children: [] }
              ]}
            ]}
          ]
        },
        {
          id: "SLB-science", type: "catgroup", category: "science",
          children: [
            { id: "UC-SL-11_slb", ucId: "UC-SL-11", type: "usecase", category: "science", children: [
              { id: "cap09_uc11b", type: "capability", capId: "AG-V1-09", children: [
                { id: "r_csrc_uc11b", type: "ragdoc", ragId: "colonnes_sources", children: [] }
              ]},
              { id: "cap06_uc11b", type: "capability", capId: "AG-V1-06", children: [
                { id: "r_src_uc11b",  type: "ragdoc", ragId: "sources_en_ligne", children: [] }
              ]}
            ]},
            { id: "UC-SL-12_slb", ucId: "UC-SL-12", type: "usecase", category: "science", children: [
              { id: "cap09_uc12b", type: "capability", capId: "AG-V1-09", children: [
                { id: "r_csrc_uc12b", type: "ragdoc", ragId: "colonnes_sources",  children: [] }
              ]},
              { id: "cap11_uc12b", type: "capability", capId: "AG-V1-11", children: [
                { id: "r_cop_uc12b",  type: "ragdoc", ragId: "copepodes_domaine", children: [] }
              ]},
              { id: "cap05_uc12b", type: "capability", capId: "AG-V1-05", children: [
                { id: "r_cins_uc12b", type: "ragdoc", ragId: "colonnes_instruments", children: [] }
              ]}
            ]},
            { id: "UC-SL-14", type: "usecase", category: "science", children: [
              { id: "cap10_uc14", type: "capability", capId: "AG-V1-10", children: [
                { id: "r_src_uc14",  type: "ragdoc", ragId: "sources_en_ligne",  children: [] }
              ]},
              { id: "cap01_uc14", type: "capability", capId: "AG-V1-01", children: [
                { id: "r_cop_uc14",  type: "ragdoc", ragId: "copepodes_domaine", children: [] }
              ]}
            ]}
          ]
        },
        {
          id: "SLB-output", type: "catgroup", category: "output",
          children: [
            { id: "UC-SL-16", type: "usecase", category: "output", children: [
              { id: "cap12_uc16", type: "capability", capId: "AG-V1-12", children: [] }
            ]},
            { id: "UC-SL-17_slb", ucId: "UC-SL-17", type: "usecase", category: "output", children: [
              { id: "cap13_uc17b", type: "capability", capId: "AG-V1-13", children: [
                { id: "r_cop_uc17b",  type: "ragdoc", ragId: "copepodes_domaine", children: [] },
                { id: "r_meth_uc17b", type: "ragdoc", ragId: "methodes_calcul",   children: [] },
                { id: "r_csrc_uc17b", type: "ragdoc", ragId: "colonnes_sources",  children: [] }
              ]}
            ]}
          ]
        }
      ]
    }
  ]
};
