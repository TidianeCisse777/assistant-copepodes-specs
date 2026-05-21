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

## Ajouter un use case — checklist complète

### 1. `USE_CASES` dans `data.js`

```js
"UC-SL-XX": {
  title: "Titre court",
  category: "science",          // "platform" | "data" | "science" | "output"
  description: "Description affichée dans le panneau de détail.",
  actors: ["Chercheur", "Étudiant gradué"],
  preconditions: "Ce qui doit être vrai avant.",
  flow: "Étapes du scénario principal.",
  postconditions: "Ce qui est vrai après.",
  scope: "Périmètre ou limites éventuelles."
}
```

### 2. `TREE_DATA` dans `data.js` (section tout en bas)

Ajouter le nœud dans le bon objectif (`SLA` ou `SLB`) :

```js
{
  id: "UC-SL-XX",
  type: "usecase",
  children: [
    {
      id: "AG-V1-YY",          // capacité déclenchée
      type: "capability",
      children: [
        { id: "nom_doc", type: "ragdoc" }   // doc RAG consulté
      ]
    }
  ]
}
```

Si le même UC apparaît dans SLA **et** SLB, dupliquer le nœud avec un `id` suffixé `_slb` et ajouter `ucId: "UC-SL-XX"` :

```js
{ id: "UC-SL-XX_slb", ucId: "UC-SL-XX", type: "usecase", children: [...] }
```

### 3. `CAPABILITIES` dans `data.js` (si nouvelle capacité)

```js
"AG-V1-XX": {
  title: "Titre de la capacité",
  description: "Ce que l'agent fait concrètement.",
  usecases: ["UC-SL-XX"],
  ragdocs: ["nom_doc"]
}
```

### 4. `RAG_DOCS` dans `data.js` (si nouveau document RAG)

```js
"nom_doc": {
  title: "Titre du document",
  description: "Ce que le document contient.",
  path: "STAGE ULAVAL/Agent/Ressources scientifiques/Document RAG/fichier.md"
}
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
