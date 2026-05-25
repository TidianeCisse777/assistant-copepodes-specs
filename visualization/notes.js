// ================================================================
//  notes.js — Brief de révision
//  Assistant scientifique copépodes · NeoLab · Université Laval
//
//  CE FICHIER EST LE POINT D'ENTRÉE DE CHAQUE SESSION DE RÉVISION.
//  Lire ce fichier en premier pour savoir quoi réviser et dans quel
//  ordre avant d'ouvrir les specs .md ou data.js.
//
// ----------------------------------------------------------------
//  FORMAT
// ----------------------------------------------------------------
//
//  Clé     : identifiant exact (UC-SL-XX, AG-V1-XX, CT-AG-XX,
//             ou nom de doc RAG : colonnes_sources, etc.)
//
//  status  : "ok"     → validé, stable
//            "review" → point ouvert, révision nécessaire
//            "draft"  → ébauche, pas encore discuté
//
//  note    : texte libre — contexte, décision, question ouverte.
//            Laisser "" si rien à dire pour l'instant.
//
//  Absence d'une clé = draft implicite (pas encore discuté).
//  Ne lister que ce qui a quelque chose à dire.
//
// ----------------------------------------------------------------
//  UTILISATION PAR CLAUDE
// ----------------------------------------------------------------
//
//  En début de session de révision, donner ce fichier à Claude :
//  → Il traite d'abord tous les "review" (points ouverts)
//  → Il pose des questions sur les "draft" explicites
//  → Il confirme les "ok" sans les modifier
//  → Il ignore les clés absentes sauf si demandé explicitement
//
// ----------------------------------------------------------------
//  VERSION
// ----------------------------------------------------------------
//  V1.1 (mai 2026) — initialisation post-révision axe lacunes
// ================================================================

const NOTES = {

  // ── Use Cases ──────────────────────────────────────────────────

  "UC-SL-11": {
    status: "ok",
    note: "Enrichi V1.1 — extension 4a ajoutée (carte des lacunes + timeline gaps). Critères d'acceptation mis à jour."
  },
  "UC-SL-12": {
    status: "ok",
    note: "Enrichi V1.1 — extension 3b ajoutée (absences taxonomiques via source de référence autorisée + corpus RAG). CT-AG-29 associée."
  },
  "UC-SL-14": {
    status: "ok",
    note: "Réécrit V1.1 — périmètre resserré : complétude des variables + synthèse globale. Lacunes spatio-temporelles → UC-SL-11, absences taxonomiques → UC-SL-12."
  },

  // ── Capacités agent ────────────────────────────────────────────

  "AG-V1-10": {
    status: "ok",
    note: "Réécrit V1.1 en cohérence avec UC-SL-14. Use cases liés mis à jour : UC-SL-11 ext.4a, UC-SL-12 ext.3b, UC-SL-14."
  },
  "AG-V1-11": {
    status: "ok",
    note: "V1.1 — UC-SL-14 retiré des use cases liés (le nouveau UC-SL-14 ne mobilise pas le corpus domaine copépodes)."
  },

  // ── Contraintes ────────────────────────────────────────────────

  "CT-AG-29": {
    status: "ok",
    note: "Nouvelle contrainte V1.1 — contextualiser les absences lors des comparaisons de couverture (confirmée / biais / incertaine). Déclenché par UC-SL-12 ext.3b."
  }

};
