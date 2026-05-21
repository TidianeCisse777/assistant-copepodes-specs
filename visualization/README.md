# Visualisation — Assistant copépodes NeoLab

Arbre interactif D3.js représentant la chaîne :
**Utilisateur → Objectif → Use Case → Capacité agent → Document RAG**

---

## Lancer la visualisation

Ne pas ouvrir `index.html` directement dans le Finder (le navigateur bloque les scripts externes via `file://`).

```bash
cd visualization/
python3 -m http.server 8080
# puis ouvrir http://localhost:8080
```

---

## Fichiers

| Fichier | Rôle |
|---|---|
| `data.js` | **Seul fichier à modifier.** Contient toutes les données : use cases, capacités, docs RAG, contraintes, arbre. |
| `index.html` | Rendu D3.js uniquement. Ne pas toucher sauf bug de rendu. |

---

## Utiliser la visualisation

- **Cliquer sur un nœud** : ouvre le panneau de détail à droite (description complète, acteurs, flux, contraintes associées).
- **Cliquer à nouveau** : ferme le panneau.
- **Cliquer sur un nœud parent** : expand / collapse ses enfants.
- **Scroll / drag** : zoom et déplacement dans l'arbre.
- **Bouton "Contraintes"** : affiche la liste des 29 contraintes agent (CT-AG-01 à CT-AG-29).
- **Filtres en haut** : filtrer par catégorie (Plateforme / Données / Science / Livrables).

---

## Code couleur des nœuds

| Couleur | Type de nœud |
|---|---|
| Bleu foncé | Utilisateur (racine) |
| Bleu-violet | Objectif (SLA / SLB) |
| Gris | Use Case Plateforme (UC-SL-00, UC-SL-01) |
| Orange | Use Case Données |
| Violet | Use Case Flux scientifique |
| Rouge | Use Case Livrable |
| Teal | Capacité agent (AG-V1-XX) |
| Jaune ocre | Document RAG |
| Gris clair | Contrainte (CT-AG-XX) |

---

## Modifier un titre ou une description existante

Ouvrir `data.js` et éditer la section correspondante :

- Titre d'un use case → `USE_CASES["UC-SL-XX"].title`
- Description d'une capacité → `CAPABILITIES["AG-V1-XX"].description`
- Description d'un doc RAG → `RAG_DOCS["..."].description`
- Texte d'une contrainte → `CONSTRAINTS` (tableau, chercher par `id`)

Sauvegarder et recharger le navigateur.

---

## Modifier un use case existant — checklist d'impact

### Principe de cascade

Un UC n'existe pas seul. Il est lié à des **capacités agent**, qui sont elles-mêmes liées à des **documents RAG** et à des **contraintes**. Modifier un UC peut donc déclencher une cascade sur plusieurs niveaux :

```
UC change
  → les capacités liées changent-elles de périmètre ?
      → les docs RAG consultés changent-ils ?
      → une nouvelle contrainte est-elle nécessaire ?
          → les fichiers de validation sont-ils à jour ?
```

Exemple réel : UC-SL-14 a été réécrit → AG-V1-10 a été réécrit → CT-AG-29 a été créée → sources_en_ligne.md a été enrichi → 7 fichiers touchés au total.

**Règle : toujours commencer par les specs `.md`, finir par `data.js`.**  
Si tu fais l'inverse (data.js en premier), la visualisation est à jour mais les specs de référence ne le sont pas — incohérence silencieuse.

### Ordre recommandé — étape par étape

**Étape 1 — Spec Use Case**
Fichier : `Use Cases — Assistant scientifique copépodes V1.md`
- Modifier le titre, le scénario, les extensions ou les critères d'acceptation du UC
- Vérifier que chaque extension a au moins un critère d'acceptation

**Étape 2 — Validation Use Case**
Fichier : `Validation rédactionnelle — Use Cases V1.md`
- Mettre à jour la ligne du UC dans le tableau de statut (statut → "OK (V1.x)")
- Ajouter une note dans la section "Révision" si le changement est substantiel

**Étape 3 — Spec Capacités agent** *(si le UC touche une capacité)*
Fichier : `Capacites agent V1.md`
- Vérifier la section "Use cases liés" de chaque capacité impactée
- Si une capacité change de périmètre : réécrire son scénario principal
- Si une nouvelle capacité est nécessaire : l'ajouter (AG-V1-XX)

**Étape 4 — Validation Capacités agent** *(si étape 3 faite)*
Fichier : `Validation rédactionnelle — Capacités agent V1.md`
- Mettre à jour la ligne de chaque capacité modifiée dans le tableau
- Ajouter une note dans la section "Révision" si la capacité a été réécrite

**Étape 5 — Contraintes** *(si le changement impose une nouvelle règle de comportement)*
Fichier : `Contraintes agent V1.md`
- Ajouter CT-AG-XX à la suite des contraintes existantes
- Préciser : identifiant, titre, description, use cases concernés

**Étape 6 — Sources en ligne** *(si une nouvelle source de données est mobilisée)*
Fichier : `sources_en_ligne.md`
- Ajouter la ligne dans le tableau "Quelle source pour quelle question"
- Ajouter la section détaillée de la source (accès, paramètres, limites)

**Étape 7 — Visualisation** *(toujours en dernier)*
Fichier : `data.js`
- Mettre à jour `USE_CASES`, `CAPABILITIES`, `CONSTRAINTS`, `TREE_DATA` selon les changements
- La visualisation reflète les specs — jamais l'inverse

---

### Par type de modification — ce qui est impacté :

### Titre du UC

- `USE_CASES["UC-SL-XX"].title` dans `data.js`
- `Use Cases — Assistant scientifique copépodes V1.md` (titre dans l'entête du UC)
- `Validation rédactionnelle — Use Cases V1.md` (ligne dans le tableau de statut)

### Description / scénario principal / postconditions

- `USE_CASES["UC-SL-XX"].description` et `.flow` dans `data.js`
- `Use Cases — Assistant scientifique copépodes V1.md` (corps du UC)
- Aucun autre fichier impacté si les capacités liées ne changent pas.

### Ajout ou suppression d'une extension au UC

Une extension = nouvelle branche de scénario (ex. ext. 4a, ext. 3b).

- `Use Cases — Assistant scientifique copépodes V1.md` (section Extensions)
- `Validation rédactionnelle — Use Cases V1.md` (vérifier que les critères d'acceptation couvrent l'extension)
- Si l'extension mobilise une capacité agent : vérifier `Capacites agent V1.md` (section Use cases liés de la capacité concernée)
- Si l'extension mobilise une nouvelle source : `sources_en_ligne.md`
- Si l'extension impose une nouvelle règle de comportement : `Contraintes agent V1.md` + `CONSTRAINTS` dans `data.js`

### Changement de capacité(s) liée(s) au UC

Ex. on retire AG-V1-10 et on ajoute AG-V1-07 pour un UC.

- `TREE_DATA` dans `data.js` : modifier les nœuds enfants du UC concerné
- `CAPABILITIES["AG-V1-XX"].usecases` dans `data.js` pour chaque capacité touchée
- `Capacites agent V1.md` (section Use cases liés de chaque capacité touchée)
- `Validation rédactionnelle — Capacités agent V1.md` (tableau de statut)

### Changement de catégorie du UC (platform / data / science / output)

- `USE_CASES["UC-SL-XX"].category` dans `data.js` (change la couleur du nœud)
- Vérifier que le UC est bien rattaché au bon objectif (SLA / SLB) dans `TREE_DATA`

### Changement de document RAG consulté

Ex. un UC mobilisait `colonnes_sources.md`, maintenant il mobilise aussi `sources_en_ligne.md`.

- `TREE_DATA` dans `data.js` : modifier les nœuds RAG enfants de la capacité concernée
- `CAPABILITIES["AG-V1-XX"].ragdocs` dans `data.js`
- `Capacites agent V1.md` (section Documents RAG de la capacité)

### Suppression d'un UC

- Retirer l'entrée de `USE_CASES` dans `data.js`
- Retirer le nœud de `TREE_DATA` dans `data.js`
- Vérifier dans `CAPABILITIES` que aucune capacité ne référence encore ce UC
- Mettre à jour les 2 fichiers de validation (Use Cases + Capacités)
- Mettre à jour `Contraintes agent V1.md` si des contraintes référençaient ce UC

---

## Ajouter un use case — checklist complète

### 1. `USE_CASES` dans `data.js`

```js
"UC-SL-XX": {
  title: "Titre court",
  category: "science",              // "platform" | "data" | "science" | "output"
  objectives: ["SLA"],              // ["SLA"] | ["SLB"] | ["SLA","SLB"] | []
  description: "Description affichée dans le panneau de détail.",
  actors: ACTORS.chercheur,         // ACTORS.chercheur | .chercheur_etudiant |
                                    // .chercheur_technicien | .tous
  preconditions: "Ce qui doit être vrai avant.",
  flow: "Étapes du scénario principal.",
  postconditions: "Ce qui est vrai après.",
  scope: "Périmètre ou limites éventuelles."
}
```

Le champ `objectives` détermine dans quel(s) objectif(s) (SLA / SLB) le UC apparaît dans l'arbre. `TREE_DATA` est dérivé automatiquement — pas besoin de le toucher.

### 2. `CAPABILITIES` dans `data.js` — ajouter le UC dans `usecases`

Si une capacité existante sert ce UC, ajouter `"UC-SL-XX"` dans son champ `usecases` :

```js
"AG-V1-YY": {
  ...
  usecases: ["UC-SL-AA", "UC-SL-XX"],  // ← ajouter ici
  ragDocs: ["nom_doc"]
}
```

Si une **nouvelle capacité** est nécessaire :

```js
"AG-V1-XX": {
  title: "Titre de la capacité",
  description: "Ce que l'agent fait concrètement.",
  usecases: ["UC-SL-XX"],
  constraints: ["CT-AG-01"],
  ragDocs: ["nom_doc"]
}
```

### 3. `RAG_DOCS` dans `data.js` (si nouveau document RAG)

```js
"nom_doc": {
  title: "Titre du document",
  shortTitle: "Titre court",
  description: "Ce que le document contient.",
  chunks: 5,
  usage: "Quand utiliser ce doc.",
  keyContent: "Contenu clé."
}
```

### 4. Modifier un acteur partout

Ouvrir `ACTORS` en haut de `data.js` et changer la valeur une seule fois :

```js
const ACTORS = {
  chercheur: ["Professeur"],   // ← changer ici = effet sur tous les UCs qui l'utilisent
  ...
};
```

### 5. Fichiers specs à synchroniser manuellement

Quand un UC change, les fichiers suivants doivent être mis à jour pour rester cohérents avec les specs :

| Fichier | Quand |
|---|---|
| `Use Cases — Assistant scientifique copépodes V1.md` | Toujours |
| `Validation rédactionnelle — Use Cases V1.md` | Toujours |
| `Capacites agent V1.md` | Si nouvelle capacité ou capacité modifiée |
| `Validation rédactionnelle — Capacités agent V1.md` | Si capacité modifiée |
| `Contraintes agent V1.md` | Si nouvelle contrainte |
| `sources_en_ligne.md` | Si nouvelle source de données activée |

---

## Périmètre actuel (V1.1 — mai 2026)

- 18 use cases : UC-SL-00 à UC-SL-17
- 14 capacités agent : AG-V1-01 à AG-V1-14
- 5 documents RAG
- 29 contraintes agent : CT-AG-01 à CT-AG-29
