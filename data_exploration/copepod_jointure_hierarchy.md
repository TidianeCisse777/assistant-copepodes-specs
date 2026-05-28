# Hiérarchie des jointures et couplages Copepod

Ce document décrit l'ordre de priorité et la logique de couplage entre les sources utilisées dans les probes Copepod.

Il sert à répondre à une seule question pratique:

> Si plusieurs sources sont disponibles, dans quel ordre doit-on les combiner et avec quelles clés ou proximités de match ?

## Principe général

La hiérarchie dépend du type de besoin.

1. Si les données locales chargées par l'utilisateur suffisent, on évite toute source externe.
2. Si un besoin taxonomique ou de morphométrie concerne les objets individuels, EcoTaxa est la base.
3. Si un volume échantillonné, un bin de profondeur ou une concentration est nécessaire, EcoPart devient la source de support naturelle.
4. Si une CTD officielle de campagne est disponible, Amundsen CTD est prioritaire sur OGSL pour le même besoin physico-chimique.
5. Si on veut un contexte régional du golfe du Saint-Laurent, OGSL sert de complément régional.
6. Si on veut des conditions environnementales actuelles ou futures à des coordonnées, Bio-ORACLE sert de couplage environnemental, pas de jointure tabulaire classique.

## Ordre de priorité recommandé

### 1. Données labo locales

**Rôle**
- Données chargées par l'utilisateur: comptage filet, biomasse, lipides, mesures manuelles, tables dérivées.

**Quand les utiliser**
- Quand le besoin est déjà couvert localement.
- Quand la source externe n'est pas nécessaire.
- Quand on veut éviter une jointure fragile.

**Principe**
- Toujours les traiter en premier.
- Si une jointure est nécessaire, elle doit être documentée comme pour les autres sources.

**Sortie attendue**
- Table de travail dérivée locale, si besoin.
- Pas de supposition sur EcoTaxa/EcoPart/CTD si ces sources ne sont pas chargées.

---

### 2. EcoTaxa + EcoPart

**Rôle**
- EcoTaxa: objets individuels, taxons, morphométrie image.
- EcoPart: profils UVP, profondeur, volume échantillonné, variables associées au profil.

**Quand les utiliser**
- Pour compter des objets, mesurer une concentration, ou relier un objet individuel à un volume échantillonné.

**Hiérarchie de jointure**
1. `profile_id` ou équivalent harmonisé.
2. `object_depth` vs `Depth [m]`.
3. `depth_delta_m` pour documenter le rapprochement.

**Colonnes de match usuelles**
- EcoTaxa: `obj_orig_id`, `sample_profileid`, `obj_depth_min`, `obj_depth_max`
- EcoPart: `Profile`, `Depth [m]`, `Sampled volume [L]`

**Sortie attendue**
- Table couplée avec colonnes de match:
  - `profile_id`
  - `object_depth`
  - `ecopart_depth`
  - `depth_delta_m`
  - `depth_match_quality`

---

### 3. Amundsen CTD

**Rôle**
- CTD officielle de campagne.
- Température, salinité, oxygène, fluorescence, nitrate, pression/profondeur.

**Quand l'utiliser**
- Quand le besoin demande la CTD officielle.
- Quand la précision source/campagne est importante.

**Priorité**
- Prioritaire sur OGSL si les deux couvrent le même besoin.

**Hiérarchie de couplage**
1. `station` / `stationID`
2. `cast_number`
3. `time`
4. `latitude` / `longitude`
5. `PRES` ou `depth`
6. `depth_delta_m`, `time_delta`, `distance_km`

**Sortie attendue**
- Table dérivée avec:
  - identifiant de cast/profil CTD;
  - variable CTD retenue;
  - indicateurs de qualité du match.

---

### 4. OGSL

**Rôle**
- Source régionale du golfe du Saint-Laurent.
- Profils environnementaux et données complémentaires selon les jeux disponibles.

**Quand l'utiliser**
- Quand on veut un contexte régional du Saint-Laurent.
- Quand Amundsen CTD n'est pas la bonne source ou n'est pas disponible pour le besoin demandé.

**Hiérarchie de couplage**
1. Identifiant de mission / station / cast si présent.
2. `time`
3. `latitude` / `longitude`
4. `PRES` / `depth`
5. deltas de match à conserver.

**Règle métier**
- Si Amundsen CTD couvre le même besoin, Amundsen passe avant OGSL.
- OGSL reste une source complémentaire régionale.

**Sortie attendue**
- Table couplée annotée avec la méthode de rapprochement et ses limites.

---

### 5. Bio-ORACLE

**Rôle**
- Variables environnementales actuelles ou futures.
- Couplage environnemental, pas jointure relationnelle classique.

**Quand l'utiliser**
- Pour contextualiser des observations locales avec des variables environnementales.
- Pour extraire des conditions à des coordonnées ou dans une zone.

**Hiérarchie de couplage**
1. Variable environnementale.
2. Période ou scénario.
3. Coordonnées ou zone.
4. Méthode d'extraction ou d'interpolation.

**Règle métier**
- Bio-ORACLE ne valide pas les taxons.
- Bio-ORACLE ne confirme pas des observations de copépodes.
- Bio-ORACLE ne doit pas être présenté comme une table comparable à EcoTaxa/EcoPart/CTD.

**Sortie attendue**
- Table enrichie avec:
  - variable Bio-ORACLE;
  - période/scénario;
  - coordonnées;
  - méthode de couplage.

---

## Hiérarchie résumée

Dans le doute, l'ordre de décision est:

1. Données labo locales.
2. EcoTaxa + EcoPart.
3. Amundsen CTD.
4. OGSL.
5. Bio-ORACLE.

## Règles de sécurité méthodologique

- Ne pas inventer une jointure sans clé ou proximité suffisante.
- Toujours conserver les deltas de match:
  - `depth_delta_m`
  - `time_delta`
  - `distance_km`
- Si la jointure est incertaine, le signaler dans la table dérivée et dans le DU/GC.
- Si une source manque, poser une question ciblée plutôt que de remplir un placeholder.
- Ne jamais écraser les données brutes; produire une table de travail dérivée.

## Cas typiques

### Cas A — objet EcoTaxa + volume EcoPart

- base: EcoTaxa;
- support: EcoPart;
- clé: `profile_id` + profondeur proche;
- sortie: concentration ou abondance documentée.

### Cas B — EcoTaxa + CTD officielle

- base: EcoTaxa;
- support: Amundsen CTD;
- clé: `station` / `cast` + proximité temps/position + profondeur;
- sortie: profil environnemental associé à l'objet ou au profil.

### Cas C — EcoTaxa / EcoPart + OGSL

- base: source locale;
- support: OGSL;
- clé: station / cast / temps / position / profondeur selon disponibilité;
- sortie: contexte régional du golfe du Saint-Laurent.

### Cas D — données labo + Bio-ORACLE

- base: fichier labo;
- support: Bio-ORACLE;
- clé: coordonnées et période;
- sortie: table environnementale dérivée.

## Statut de ce document

Ce document est destiné aux probes, aux tests et à la conception des joins/couplages Copepod.
Il ne décrit pas le code d'implémentation, seulement la logique métier et l'ordre de priorité des sources.
