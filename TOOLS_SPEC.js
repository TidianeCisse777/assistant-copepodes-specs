// ================================================================
//  TOOLS_SPEC.js — Spécification des tools de l'agent copépodes
//  NeoLab · Université Laval
//
//  Ce fichier mappe : capacité → tools atomiques → signatures → tests.
//  Périmètre V1 : gestion des données (AG-V1-01 à AG-V1-06).
//
//  Couche A = tests unitaires Python sur la fonction.
//  Couche B = tests de régression prompt (input fixe → structure attendue).
//
//  Pour intégration future avec visualization/data.js :
//  la clé de chaque entrée TOOLS_SPEC est le nom du tool Python ;
//  le champ `capability` est la clé de liaison avec CAPABILITIES.
// ================================================================

const TOOLS_SPEC = {

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-01 · Comprendre les sources disponibles
  //  UC : UC-SL-04, UC-SL-14
  //  RAG : colonnes_sources, sources_en_ligne
  // ──────────────────────────────────────────────────────────────

  "sources.list_available": {
    capability: "AG-V1-01",
    usecases: ["UC-SL-04"],
    description: "Retourne la liste des sources connues avec statut d'activation.",
    input: {},
    output: {
      sources: [
        {
          id: "string",          // ex. "ecotaxa_1165"
          label: "string",       // ex. "EcoTaxa UVP5 Amundsen 2018"
          type: "string",        // "local" | "api" | "rag_only"
          activated: "boolean",
          requires_credentials: "boolean"
        }
      ]
    },
    constraints: ["CT-AG-01", "CT-AG-08"],
    testA: [
      "Appel sans argument → liste non vide, chaque entrée a id/label/type/activated.",
      "Aucune source activée → activated=false pour toutes les entrées, pas d'erreur."
    ],
    testB: [
      "Prompt: 'quelles sources sont disponibles ?' → réponse liste au moins ecotaxa, ecopart, amundsen, obis.",
      "Prompt: 'ai-je besoin d'un compte pour OBIS ?' → réponse cite requires_credentials=false pour obis."
    ]
  },

  "sources.describe": {
    capability: "AG-V1-01",
    usecases: ["UC-SL-04", "UC-SL-14"],
    description: "Retourne la description complète d'une source : contenu, format, clés de jointure, limitations.",
    input: {
      source_id: "string"  // ex. "ecotaxa_1165"
    },
    output: {
      id: "string",
      label: "string",
      content_summary: "string",
      join_keys: ["string"],
      known_limitations: ["string"],
      requires_credentials: "boolean",
      rag_doc_ref: "string"  // clé dans RAG_DOCS
    },
    constraints: ["CT-AG-01", "CT-AG-08"],
    testA: [
      "source_id='ecotaxa_1165' → join_keys contient 'obj_orig_id' et 'profile_id'.",
      "source_id inconnu → erreur explicite avec liste des ids valides."
    ],
    testB: [
      "Prompt: 'que contient EcoPart 105 ?' → réponse cite profils CTD, colonnes particles, pas d'invention.",
      "Prompt: 'comment joindre EcoTaxa à EcoPart ?' → réponse cite obj_orig_id → profile_id."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-02 · Aider à formuler le contexte scientifique
  //  UC : UC-SL-07, UC-SL-08
  //  RAG : copepodes_domaine
  // ──────────────────────────────────────────────────────────────

  "context.get_required_fields": {
    capability: "AG-V1-02",
    usecases: ["UC-SL-07", "UC-SL-08"],
    description: "Retourne la liste des champs de contexte requis avant toute analyse, avec ceux déjà remplis.",
    input: {
      session_context: "object"  // état courant du contexte de session
    },
    output: {
      required: ["string"],   // ex. ["species", "zone", "variable", "period"]
      filled: ["string"],
      missing: ["string"],
      ready_for_analysis: "boolean"
    },
    constraints: ["CT-AG-04", "CT-AG-25"],
    testA: [
      "session_context vide → missing contient ['species','zone','variable','period'], ready_for_analysis=false.",
      "Tous les champs remplis → missing=[], ready_for_analysis=true."
    ],
    testB: [
      "Prompt: 'analyse mes données' sans contexte → agent retourne les champs manquants, ne lance pas d'analyse.",
      "Prompt: 'je veux analyser C. hyperboreus dans la mer de Baffin en 2018 pour les lipides' → ready_for_analysis=true."
    ]
  },

  "context.validate_species": {
    capability: "AG-V1-02",
    usecases: ["UC-SL-07", "UC-SL-08"],
    description: "Valide qu'un nom d'espèce est connu du corpus RAG et retourne les données biologiques associées.",
    input: {
      species_name: "string"
    },
    output: {
      known: "boolean",
      canonical_name: "string",
      ambiguity_warning: "string | null",  // ex. "C. glacialis/finmarchicus morphologiquement identiques"
      functional_group: "string",
      life_stages: ["string"],
      rag_doc_ref: "string"
    },
    constraints: ["CT-AG-19", "CT-AG-27"],
    testA: [
      "species_name='Calanus glacialis' → known=true, ambiguity_warning non null (C. finmarchicus).",
      "species_name='Zooplankton inconnu' → known=false, pas d'erreur fatale."
    ],
    testB: [
      "Prompt: 'analyse les Calanus glacialis' → agent signale l'ambiguïté C. glacialis / C. finmarchicus avant d'aller plus loin.",
      "Prompt: 'que sont les copépodes ?' → réponse s'appuie sur copepodes_domaine, pas d'invention."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-03 · Valider les données chargées
  //  UC : UC-SL-03, UC-SL-05, UC-SL-06
  //  RAG : colonnes_sources, colonnes_instruments
  // ──────────────────────────────────────────────────────────────

  "data.inspect": {
    capability: "AG-V1-03",
    usecases: ["UC-SL-03"],
    description: "Inspecte un DataFrame ou fichier chargé : colonnes, types, unités inférées, aperçu.",
    input: {
      df: "DataFrame",  // ou path: string
      source_hint: "string | null"  // ex. "ecotaxa_1165" pour aider l'inférence d'unités
    },
    output: {
      n_rows: "int",
      n_cols: "int",
      columns: [
        {
          name: "string",
          dtype: "string",
          unit_inferred: "string | null",
          sample_values: ["any"],
          null_count: "int",
          null_pct: "float"
        }
      ],
      detected_source: "string | null",
      join_key_candidates: ["string"]
    },
    constraints: ["CT-AG-10"],
    testA: [
      "DataFrame avec colonne 'object_depth_min' → unit_inferred='m', dtype='float'.",
      "DataFrame vide (0 lignes) → n_rows=0, colonnes présentes, pas d'erreur."
    ],
    testB: [
      "Prompt: 'charge ce TSV et dis-moi ce qu'il contient' → réponse cite n_rows, colonnes clés, source détectée.",
      "Prompt: 'quelles colonnes ai-je ?' → réponse liste colonnes avec unités, sans inventer des valeurs."
    ]
  },

  "data.validate": {
    capability: "AG-V1-03",
    usecases: ["UC-SL-03", "UC-SL-05", "UC-SL-06"],
    description: "Valide la qualité d'un DataFrame : colonnes critiques présentes, types corrects, valeurs hors plage.",
    input: {
      df: "DataFrame",
      required_columns: ["string"],  // ex. ["object_depth_min", "taxon"]
      source_type: "string | null"   // ex. "ecotaxa" pour validation spécialisée
    },
    output: {
      valid: "boolean",
      confidence_by_column: {
        "<col_name>": "reliable | exploratory | unusable"
      },
      errors: [
        {
          column: "string",
          issue: "string",
          severity: "blocking | warning"
        }
      ],
      blocking_count: "int",
      warning_count: "int"
    },
    constraints: ["CT-AG-03", "CT-AG-05", "CT-AG-10"],
    testA: [
      "DataFrame avec colonne requise manquante → valid=false, erreur severity='blocking'.",
      "DataFrame avec 30% de nulls sur colonne critique → confidence='unusable', severity='blocking'.",
      "DataFrame parfait → valid=true, blocking_count=0."
    ],
    testB: [
      "Prompt: 'mes données sont-elles utilisables pour calculer la concentration ?' → réponse vérifie 'Sampled volume [L]', retourne confidence.",
      "Prompt: 'les données ont des valeurs manquantes, c'est grave ?' → réponse distingue colonnes bloquantes vs warnings."
    ]
  },

  "data.profile_missing": {
    capability: "AG-V1-03",
    usecases: ["UC-SL-05", "UC-SL-06", "UC-SL-14"],
    description: "Produit un rapport de valeurs manquantes par colonne, groupé par catégorie (clés, mesures, métadonnées).",
    input: {
      df: "DataFrame",
      source_type: "string | null"
    },
    output: {
      summary: {
        total_rows: "int",
        complete_rows: "int",
        complete_pct: "float"
      },
      by_column: [
        {
          column: "string",
          category: "key | measure | metadata | unknown",
          null_pct: "float",
          usability: "reliable | exploratory | unusable"
        }
      ]
    },
    constraints: ["CT-AG-03", "CT-AG-27"],
    testA: [
      "Colonne avec 0% nulls → usability='reliable'.",
      "Colonne avec 80% nulls et catégorie='key' → usability='unusable'.",
      "DataFrame sans nulls → complete_pct=100.0."
    ],
    testB: [
      "Prompt: 'quelles colonnes sont inutilisables ?' → réponse liste uniquement les colonnes unusable, cite les taux.",
      "Prompt: 'mes données sont complètes ?' → réponse cite complete_pct, distingue keys vs measures."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-04 · Interroger les sources activées
  //  UC : UC-SL-04, UC-SL-13
  //  RAG : sources_en_ligne
  // ──────────────────────────────────────────────────────────────

  "sources.query_ecotaxa": {
    capability: "AG-V1-04",
    usecases: ["UC-SL-04"],
    description: "Lance un export EcoTaxa authentifié pour un projet donné.",
    input: {
      project_id: "int",
      with_images: "boolean",
      auth_token: "string"  // depuis env, jamais loggé
    },
    output: {
      job_id: "string",
      zip_path: "string | null",
      status: "pending | done | error",
      report: "string"
    },
    constraints: ["CT-AG-11", "CT-AG-12"],
    testA: [
      "project_id valide + token valide → status='done', zip_path non null.",
      "token invalide → status='error', message d'erreur explicite, token non exposé dans le message."
    ],
    testB: [
      "Prompt: 'exporte le projet EcoTaxa 1165' → agent demande confirmation avant lancement, cite le volume estimé.",
      "Prompt: 'exporte avec les images' → agent avertit du volume, attend validation (CT-AG-12)."
    ]
  },

  "sources.query_amundsen_ctd": {
    capability: "AG-V1-04",
    usecases: ["UC-SL-04", "UC-SL-13"],
    description: "Interroge ERDDAP Amundsen pour un échantillon CTD paramétré.",
    input: {
      date_start: "string",   // ISO 8601
      date_end: "string",
      lat_min: "float",
      lat_max: "float",
      lon_min: "float",
      lon_max: "float",
      variables: ["string"]  // ex. ["TE90", "PSAL", "OXYM"]
    },
    output: {
      df: "DataFrame",
      n_casts: "int",
      variables_returned: ["string"],
      variables_missing: ["string"],
      query_url: "string"
    },
    constraints: ["CT-AG-08", "CT-AG-12", "CT-AG-20"],
    testA: [
      "Requête zone/période valide → df non vide, n_casts > 0.",
      "Variable inconnue dans variables → variables_missing contient la variable, pas d'erreur fatale.",
      "Zone sans données → df vide, n_casts=0, pas d'erreur fatale."
    ],
    testB: [
      "Prompt: 'récupère la CTD pour ips_007' → agent paramètre date/lat/lon depuis le profil EcoPart, valide avant requête.",
      "Prompt: 'quelle est la température en mer de Baffin en août 2018 ?' → agent cite query_url dans la réponse."
    ]
  },

  "sources.query_obis": {
    capability: "AG-V1-04",
    usecases: ["UC-SL-04", "UC-SL-12", "UC-SL-14"],
    description: "Interroge l'API OBIS pour une espèce et une zone géographique.",
    input: {
      species: "string",      // nom scientifique canonique
      lat_min: "float",
      lat_max: "float",
      lon_min: "float",
      lon_max: "float",
      year_start: "int | null",
      year_end: "int | null"
    },
    output: {
      n_records: "int",
      records_df: "DataFrame",
      coverage_summary: {
        years: ["int"],
        datasets: ["string"],
        sampling_bias_flags: ["string"]
      }
    },
    constraints: ["CT-AG-08", "CT-AG-29"],
    testA: [
      "species='Calanus hyperboreus', zone arctique → n_records > 0.",
      "species inexistant → n_records=0, pas d'erreur fatale.",
      "Zone sans données OBIS → n_records=0, sampling_bias_flags non vide (biais arctique)."
    ],
    testB: [
      "Prompt: 'compare mes données à OBIS pour C. hyperboreus' → réponse distingue absence confirmée vs biais d'échantillonnage (CT-AG-29).",
      "Prompt: 'OBIS a-t-il des données hivernales arctiques ?' → agent cite les biais connus."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-05 · Expliquer les colonnes et unités
  //  UC : UC-SL-05, UC-SL-06, UC-SL-12, UC-SL-15
  //  RAG : colonnes_sources, colonnes_instruments
  // ──────────────────────────────────────────────────────────────

  "columns.describe": {
    capability: "AG-V1-05",
    usecases: ["UC-SL-05", "UC-SL-06"],
    description: "Retourne la définition, l'unité, le niveau de confiance et les distinctions critiques d'une colonne.",
    input: {
      column_name: "string",
      source_hint: "string | null"
    },
    output: {
      column: "string",
      definition: "string",
      unit: "string | null",
      confidence: "reliable | exploratory | unusable | unknown",
      critical_notes: ["string"],  // ex. "acq_pixel requis pour conversion mm"
      rag_doc_ref: "string",
      source_file: "string"
    },
    constraints: ["CT-AG-01", "CT-AG-03", "CT-AG-27"],
    testA: [
      "column_name='acq_pixel' → unit='mm/pixel', critical_notes contient la note de conversion.",
      "column_name='object_feret' → definition non vide, unit='pixel ou mm selon source'.",
      "column_name inconnue → confidence='unknown', pas d'erreur fatale."
    ],
    testB: [
      "Prompt: 'que signifie object_depth_min ?' → réponse cite la définition du RAG, unit='m', pas d'invention.",
      "Prompt: 'quelle colonne donne la taille ?' → réponse explique object_feret vs object_area, cite acq_pixel."
    ]
  },

  "columns.check_for_calculation": {
    capability: "AG-V1-05",
    usecases: ["UC-SL-15"],
    description: "Vérifie si les colonnes requises pour un calcul donné sont présentes et utilisables.",
    input: {
      df_columns: ["string"],
      calculation: "string"  // ex. "concentration", "biomasse", "lipid_index"
    },
    output: {
      feasible: "boolean",
      required_columns: ["string"],
      present: ["string"],
      missing: ["string"],
      unusable: ["string"],
      blocking_reason: "string | null"
    },
    constraints: ["CT-AG-05", "CT-AG-06"],
    testA: [
      "calculation='concentration', df_columns manque 'Sampled volume [L]' → feasible=false, missing=['Sampled volume [L]'], blocking_reason non null.",
      "Toutes les colonnes présentes → feasible=true, missing=[], unusable=[]."
    ],
    testB: [
      "Prompt: 'puis-je calculer la concentration ?' → agent retourne feasible + raison si non, sans lancer le calcul.",
      "Prompt: 'que me manque-t-il pour calculer la biomasse ?' → réponse liste missing columns avec explications."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-06 · Construire des tables de travail
  //  UC : UC-SL-09, UC-SL-10, UC-SL-11, UC-SL-13
  //  RAG : colonnes_sources
  // ──────────────────────────────────────────────────────────────

  "joins.plan": {
    capability: "AG-V1-06",
    usecases: ["UC-SL-09", "UC-SL-10", "UC-SL-11", "UC-SL-13"],
    description: "Produit un plan de jointure entre sources sans l'exécuter : clés, stratégie, pertes estimées.",
    input: {
      sources: ["string"],       // ex. ["ecotaxa_1165", "ecopart_105"]
      target_columns: ["string"] // colonnes souhaitées en sortie
    },
    output: {
      feasible: "boolean",
      join_steps: [
        {
          left: "string",
          right: "string",
          key: "string",
          strategy: "string",    // ex. "exact match on profile_id"
          estimated_loss_pct: "float | null"
        }
      ],
      output_columns: ["string"],
      missing_columns: ["string"],
      warnings: ["string"]
    },
    constraints: ["CT-AG-05", "CT-AG-07"],
    testA: [
      "sources=['ecotaxa_1165','ecopart_105'] → join_steps contient profile_id comme clé.",
      "target_column non disponible dans aucune source → missing_columns contient la colonne."
    ],
    testB: [
      "Prompt: 'comment joindre EcoTaxa et EcoPart ?' → agent retourne le plan avec clé obj_orig_id → profile_id.",
      "Prompt: 'je veux la température de chaque objet UVP' → agent identifie qu'il faut EcoPart + Amundsen CTD, retourne le plan à deux étapes."
    ]
  },

  "joins.execute": {
    capability: "AG-V1-06",
    usecases: ["UC-SL-09", "UC-SL-10", "UC-SL-11", "UC-SL-13"],
    description: "Exécute une jointure entre sources après validation du plan par l'utilisateur.",
    input: {
      left_df: "DataFrame",
      right_df: "DataFrame",
      key: "string",
      strategy: "string",        // "exact" | "nearest_depth" | "nearest_datetime"
      tolerance: "object | null" // ex. {"depth_m": 0.5, "time_min": 5}
    },
    output: {
      result_df: "DataFrame",
      n_matched: "int",
      n_unmatched_left: "int",
      n_unmatched_right: "int",
      match_quality: {
        pct_matched: "float",
        mean_key_delta: "float | null"
      },
      provenance: {
        left_source: "string",
        right_source: "string",
        key_used: "string",
        strategy: "string",
        tolerance: "object | null"
      }
    },
    constraints: ["CT-AG-07", "CT-AG-10", "CT-AG-20"],
    testA: [
      "Jointure exacte sur profile_id, 100% de matchs → pct_matched=100.0, n_unmatched_left=0.",
      "Clé absente dans right_df → erreur explicite, left_df non modifié (CT-AG-10).",
      "strategy='nearest_depth', tolerance dépassée → n_unmatched_left > 0, mean_key_delta dans output."
    ],
    testB: [
      "Prompt: 'construis la table de travail' → agent présente le plan (joins.plan) avant d'appeler joins.execute.",
      "Prompt: 'combien d'objets n'ont pas de profil CTD ?' → agent cite n_unmatched_left dans la réponse."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-07 · Calculer des variables dérivées
  //  UC : UC-SL-10, UC-SL-15
  //  RAG : methodes_calcul
  // ──────────────────────────────────────────────────────────────

  "calc.get_method": {
    capability: "AG-V1-07",
    usecases: ["UC-SL-15"],
    description: "Retourne la méthode de calcul d'une variable dérivée : formule, colonnes requises, unités, limites.",
    input: {
      variable: "string"  // ex. "concentration", "biomasse", "lipid_index", "prosome_length"
    },
    output: {
      variable: "string",
      formula: "string",
      required_columns: ["string"],
      output_unit: "string",
      limitations: ["string"],
      rag_doc_ref: "string"
    },
    constraints: ["CT-AG-05", "CT-AG-06"],
    testA: [
      "variable='concentration' → required_columns contient 'Sampled volume [L]', formula non vide.",
      "variable inconnue → erreur explicite avec liste des variables supportées."
    ],
    testB: [
      "Prompt: 'comment calculer la concentration ?' → réponse cite la formule et les colonnes requises depuis methodes_calcul.",
      "Prompt: 'explique-moi la méthode biomasse' → réponse cite prosome_length → masse sèche → carbone, pas d'invention."
    ]
  },

  "calc.execute": {
    capability: "AG-V1-07",
    usecases: ["UC-SL-10", "UC-SL-15"],
    description: "Exécute le calcul d'une variable dérivée après validation de la méthode par l'utilisateur.",
    input: {
      df: "DataFrame",
      variable: "string",
      method_validated: "boolean"  // doit être true pour exécuter
    },
    output: {
      result_df: "DataFrame",      // df original + nouvelle colonne
      new_column: "string",
      output_unit: "string",
      n_computed: "int",
      n_failed: "int",
      failure_reasons: ["string"],
      provenance: {
        formula: "string",
        columns_used: ["string"],
        method_source: "string"
      }
    },
    constraints: ["CT-AG-05", "CT-AG-06", "CT-AG-20"],
    testA: [
      "method_validated=false → erreur, calcul non exécuté.",
      "Colonne requise manquante → n_failed=n_rows, failure_reasons non vide.",
      "Calcul réussi → new_column présente dans result_df, n_computed > 0."
    ],
    testB: [
      "Prompt: 'calcule la concentration' → agent appelle calc.get_method, présente la méthode, attend validation avant calc.execute.",
      "Prompt: 'pourquoi le calcul a échoué sur 10 lignes ?' → agent cite failure_reasons depuis le résultat."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-08 · Générer des graphiques scientifiques
  //  UC : UC-SL-09
  //  RAG : methodes_calcul, colonnes_sources
  // ──────────────────────────────────────────────────────────────

  "plot.plan": {
    capability: "AG-V1-08",
    usecases: ["UC-SL-09"],
    description: "Propose un plan de graphique (type, axes, filtres) pour validation avant génération.",
    input: {
      df_columns: ["string"],
      user_intent: "string"  // ex. "distribution de profondeur par taxon"
    },
    output: {
      chart_type: "string",         // ex. "histogram", "scatter", "boxplot", "profile"
      x_column: "string",
      y_column: "string | null",
      color_by: "string | null",
      filters_applied: ["string"],
      title_suggestion: "string",
      limitations: ["string"]
    },
    constraints: ["CT-AG-06", "CT-AG-14"],
    testA: [
      "user_intent contient 'profondeur' → x_column ou y_column inclut une colonne depth.",
      "Colonne demandée absente dans df_columns → limitations non vide, chart_type ajusté ou null."
    ],
    testB: [
      "Prompt: 'fais un graphique de la distribution de profondeur' → agent propose le plan, attend validation avant génération.",
      "Prompt: 'graphique par taxon' → agent cite color_by='taxon' dans le plan."
    ]
  },

  "plot.generate": {
    capability: "AG-V1-08",
    usecases: ["UC-SL-09"],
    description: "Génère un graphique scientifique avec métadonnées complètes après validation du plan.",
    input: {
      df: "DataFrame",
      chart_type: "string",
      x_column: "string",
      y_column: "string | null",
      color_by: "string | null",
      title: "string",
      filters: "object | null",
      plan_validated: "boolean"
    },
    output: {
      figure_path: "string",
      metadata: {
        title: "string",
        x_label: "string",
        y_label: "string | null",
        units: "object",
        source: "string",
        filters_applied: ["string"],
        n_points: "int",
        limitations: ["string"]
      }
    },
    constraints: ["CT-AG-14", "CT-AG-13", "CT-AG-01", "CT-AG-24"],
    testA: [
      "plan_validated=false → erreur, graphique non généré.",
      "Génération réussie → figure_path valide, metadata.title non vide, metadata.source non vide.",
      "df vide → erreur explicite, pas de graphique vide généré."
    ],
    testB: [
      "Prompt: 'génère le graphique' → réponse affiche le graphique comme bloc statique complet (CT-AG-24), avec titre et source.",
      "Prompt: 'que signifie ce graphique ?' → agent sépare observation et interprétation (CT-AG-13)."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-09 · Produire une analyse exploratoire
  //  UC : UC-SL-10, UC-SL-11, UC-SL-12, UC-SL-13
  //  RAG : colonnes_sources, methodes_calcul
  // ──────────────────────────────────────────────────────────────

  "analysis.explore": {
    capability: "AG-V1-09",
    usecases: ["UC-SL-10", "UC-SL-11", "UC-SL-12", "UC-SL-13"],
    description: "Exécute une analyse exploratoire (distribution, composition, corrélation) avec séparation explicite observation / interprétation / hypothèse.",
    input: {
      df: "DataFrame",
      analysis_type: "string",     // "distribution" | "composition" | "correlation" | "temporal" | "spatial"
      target_columns: ["string"],
      context: {
        species: "string | null",
        zone: "string | null",
        period: "string | null",
        hypothesis: "string | null"
      }
    },
    output: {
      report: {
        observation: "string",      // ce que montrent les données
        interpretation: "string",   // ce que cela suggère
        hypothesis: "string | null",// ce que cela pourrait signifier si confirmé
        confidence: "reliable | exploratory | impossible",
        figures: ["string"],        // paths
        tables: ["object"],
        limitations: ["string"],
        sources_used: ["string"]
      }
    },
    constraints: ["CT-AG-13", "CT-AG-19", "CT-AG-24"],
    testA: [
      "report contient toujours les trois champs observation/interpretation/hypothesis.",
      "context vide → confidence='exploratory', observation cite l'absence de contexte.",
      "df sans les colonnes target → confidence='impossible', observation explique le blocage."
    ],
    testB: [
      "Prompt: 'analyse la distribution verticale des copépodes' → rapport sépare explicitement observation et interprétation.",
      "Prompt: 'que peut-on conclure ?' → agent utilise 'hypothèse' pour les conclusions non confirmées, pas d'assertion ferme."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-10 · Évaluer la complétude et synthétiser les lacunes
  //  UC : UC-SL-14
  //  RAG : sources_en_ligne, copepodes_domaine
  // ──────────────────────────────────────────────────────────────

  "completeness.evaluate": {
    capability: "AG-V1-10",
    usecases: ["UC-SL-14"],
    description: "Évalue le taux de remplissage des colonnes clés et identifie les variables critiques inutilisables.",
    input: {
      df: "DataFrame",
      critical_columns: ["string"],  // colonnes jugées critiques pour l'analyse prévue
      source_type: "string | null"
    },
    output: {
      by_column: [
        {
          column: "string",
          fill_rate: "float",
          status: "available | partial | unusable",
          blocked_analyses: ["string"]  // ex. ["concentration", "biomasse"]
        }
      ],
      overall_readiness: "ready | partial | blocked",
      blocked_analyses: ["string"],
      available_analyses: ["string"]
    },
    constraints: ["CT-AG-01", "CT-AG-03"],
    testA: [
      "Colonne avec fill_rate < 0.2 → status='unusable', blocked_analyses non vide.",
      "Toutes colonnes fill_rate > 0.9 → overall_readiness='ready'.",
      "critical_columns vide → overall_readiness calculé sur colonnes standard de la source."
    ],
    testB: [
      "Prompt: 'quelles analyses sont possibles avec mes données ?' → réponse cite available_analyses, pas d'analyse inventée.",
      "Prompt: 'pourquoi ne puis-je pas calculer la concentration ?' → agent cite fill_rate de 'Sampled volume [L]' et status."
    ]
  },

  "completeness.compare_obis": {
    capability: "AG-V1-10",
    usecases: ["UC-SL-14"],
    description: "Compare la couverture locale (espèces/zones/périodes) avec les données OBIS de référence.",
    input: {
      local_species: ["string"],
      local_zone: { lat_min: "float", lat_max: "float", lon_min: "float", lon_max: "float" },
      local_period: { year_start: "int", year_end: "int" }
    },
    output: {
      species_coverage: [
        {
          species: "string",
          in_local: "boolean",
          in_obis: "boolean",
          obis_n_records: "int",
          absence_type: "confirmed | sampling_bias | uncertain"  // CT-AG-29
        }
      ],
      sampling_bias_warnings: ["string"],
      rag_doc_ref: "string"
    },
    constraints: ["CT-AG-29", "CT-AG-03"],
    testA: [
      "Espèce absente localement mais présente dans OBIS → absence_type déterminé selon biais connus.",
      "Zone arctique → sampling_bias_warnings contient avertissement données hivernales.",
      "C. glacialis dans zone de chevauchement → sampling_bias_warnings cite ambiguïté avec C. finmarchicus."
    ],
    testB: [
      "Prompt: 'compare ma couverture à OBIS' → rapport distingue absence confirmée / biais / incertaine (CT-AG-29).",
      "Prompt: 'pourquoi OBIS n'a pas de données hivernales arctiques ?' → agent explique le biais, pas d'invention."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-11 · Répondre aux questions de domaine copépodes
  //  UC : UC-SL-12
  //  RAG : copepodes_domaine
  // ──────────────────────────────────────────────────────────────

  "domain.answer": {
    capability: "AG-V1-11",
    usecases: ["UC-SL-12"],
    description: "Répond à une question biologique sur les copépodes en s'appuyant sur le corpus RAG.",
    input: {
      question: "string",
      context: "object | null"  // espèce, zone, stade si disponible
    },
    output: {
      answer: "string",
      confidence: "reliable | exploratory | uncertain",
      sources: ["string"],        // chunks RAG utilisés
      uncertainty_flags: ["string"],
      rag_doc_ref: "string"
    },
    constraints: ["CT-AG-19", "CT-AG-27", "CT-AG-02"],
    testA: [
      "Question sur C. glacialis → sources contient copepodes_domaine, uncertainty_flags cite ambiguïté C. finmarchicus si pertinent.",
      "Question hors corpus RAG → confidence='uncertain', answer signale explicitement la limite."
    ],
    testB: [
      "Prompt: 'quel est le rôle des lipides chez Calanus ?' → réponse ancrée dans copepodes_domaine, pas d'invention.",
      "Prompt: 'C. glacialis est-il présent en Atlantique Nord ?' → agent cite l'incertitude d'identification morphologique."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-12 · Exporter les résumés de session
  //  UC : UC-SL-16
  // ──────────────────────────────────────────────────────────────

  "session.build_summary": {
    capability: "AG-V1-12",
    usecases: ["UC-SL-16"],
    description: "Compile un résumé structuré de la session : contexte, sources, méthodes, résultats, limites.",
    input: {
      session_log: "object"  // historique des actions et résultats de la session
    },
    output: {
      summary: {
        context: "string",
        sources_used: ["string"],
        methods_applied: ["string"],
        results: ["object"],
        limitations: ["string"],
        analyses_incomplete: ["string"]
      },
      export_formats: ["string"]  // ex. ["markdown", "json"]
    },
    constraints: ["CT-AG-20", "CT-AG-01", "CT-AG-18"],
    testA: [
      "session_log avec 3 analyses → results contient 3 entrées, sources_used non vide.",
      "session_log vide → erreur explicite, pas de résumé généré."
    ],
    testB: [
      "Prompt: 'exporte le résumé de session' → réponse structurée sans narration excessive (CT-AG-18), toutes sources citées.",
      "Prompt: 'qu'est-ce qu'on a fait dans cette session ?' → résumé factuel, pas de paraphrase générative."
    ]
  },

  "session.export": {
    capability: "AG-V1-12",
    usecases: ["UC-SL-16"],
    description: "Exporte le résumé de session dans un format structuré (Markdown, JSON).",
    input: {
      summary: "object",  // sortie de session.build_summary
      format: "string"    // "markdown" | "json"
    },
    output: {
      file_path: "string",
      format: "string",
      size_bytes: "int"
    },
    constraints: ["CT-AG-20"],
    testA: [
      "format='markdown' → file_path se termine en .md, contenu non vide.",
      "format invalide → erreur avec liste des formats supportés."
    ],
    testB: [
      "Prompt: 'exporte en markdown' → agent génère le fichier et cite le chemin dans la réponse."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-13 · Préparer les livrables scientifiques
  //  UC : UC-SL-17
  //  RAG : copepodes_domaine, methodes_calcul, colonnes_sources
  // ──────────────────────────────────────────────────────────────

  "deliverable.build": {
    capability: "AG-V1-13",
    usecases: ["UC-SL-17"],
    description: "Génère un livrable structuré pour révision humaine ou demande de subvention.",
    input: {
      session_summary: "object",
      sections_to_include: ["string"],  // ex. ["context","results","methods","figures","citations","limitations"]
      target_use: "string"              // "review" | "grant_application"
    },
    output: {
      deliverable: {
        context: "string",
        results_by_usecase: ["object"],
        figures: ["string"],
        methods: "string",
        citations: ["string"],       // uniquement depuis données + RAG (CT-AG-15)
        limitations: ["string"],
        incomplete_analyses: ["string"]  // signalé explicitement
      },
      review_flags: ["string"]  // points nécessitant révision humaine
    },
    constraints: ["CT-AG-15", "CT-AG-28", "CT-AG-01", "CT-AG-20"],
    testA: [
      "citations contient uniquement des références présentes dans les données ou le corpus RAG.",
      "incomplete_analyses non vide si une analyse planifiée n'a pas abouti.",
      "target_use='grant_application' → review_flags contient au moins un point de révision humaine."
    ],
    testB: [
      "Prompt: 'prépare le livrable' → agent signale les analyses incomplètes dans incomplete_analyses, sans les inventer.",
      "Prompt: 'ajoute des citations' → agent utilise uniquement le corpus RAG, cite la source de chaque référence."
    ]
  },

  // ──────────────────────────────────────────────────────────────
  //  AG-V1-14 · Interface adaptée au mode de travail
  //  UC : UC-SL-02
  // ──────────────────────────────────────────────────────────────

  "session.set_mode": {
    capability: "AG-V1-14",
    usecases: ["UC-SL-02"],
    description: "Active le mode de travail (Contexte ou Analyse) et adapte le comportement de l'agent.",
    input: {
      mode: "string"  // "context" | "analysis"
    },
    output: {
      mode_active: "string",
      behavior_changes: ["string"],  // description des changements d'interface
      ui_constraints: {
        free_text_input: "boolean",   // false en mode Analyse
        streaming: "boolean",         // false toujours (CT-AG-24)
        form_required: "boolean"      // true en mode Analyse
      }
    },
    constraints: ["CT-AG-23", "CT-AG-24", "CT-AG-26"],
    testA: [
      "mode='analysis' → ui_constraints.free_text_input=false, ui_constraints.form_required=true.",
      "mode='context' → ui_constraints.free_text_input=true, ui_constraints.form_required=false.",
      "streaming toujours false quelle que soit le mode (CT-AG-24).",
      "mode invalide → erreur avec liste des modes supportés."
    ],
    testB: [
      "Prompt: 'passe en mode analyse' → agent confirme le changement, liste les contraintes d'interface actives.",
      "Prompt: 'c'est quoi la différence entre les deux modes ?' → réponse cite Mode Contexte = questions guidées, Mode Analyse = formulaire → rapport statique."
    ]
  },

  "session.get_mode": {
    capability: "AG-V1-14",
    usecases: ["UC-SL-02"],
    description: "Retourne le mode actif et les contraintes d'interface en cours.",
    input: {},
    output: {
      mode_active: "string",
      ui_constraints: "object"
    },
    constraints: ["CT-AG-23"],
    testA: [
      "Appel après set_mode('analysis') → mode_active='analysis'.",
      "Appel sans mode défini → mode_active='context' par défaut."
    ],
    testB: [
      "Prompt: 'dans quel mode suis-je ?' → réponse cite le mode actif et ses implications."
    ]
  }

};
