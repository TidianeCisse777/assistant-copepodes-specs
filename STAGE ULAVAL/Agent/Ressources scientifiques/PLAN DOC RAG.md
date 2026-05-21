# Plan des documents RAG

Ce dossier sert de base de connaissance scientifique pour l'assistant copepodes. Les fichiers RAG ne décrivent pas le comportement général de l'agent : ils lui donnent les connaissances nécessaires pour répondre, vérifier les données, expliquer les colonnes et éviter les calculs non justifiés.

Les specs de comportement sont dans :

```text
STAGE ULAVAL/Agent/Spec de L'agent/
```

Les connaissances RAG sont dans :

```text
STAGE ULAVAL/Agent/Ressources scientifiques/Document RAG/
```

---

# À quoi sert colonnes_sources.md ?

Ce fichier explique les colonnes observées dans les sources réelles déjà testées :

```text
EcoTaxa 1165 — UVP5 Amundsen
EcoTaxa 2331 — LOKI copepod lipids
EcoPart 105 — UVP5 Amundsen 2018
Amundsen Science CTD
```

À utiliser quand l'utilisateur demande :

```text
- que contient cette source ?
- quelle colonne utiliser ?
- comment joindre EcoTaxa, EcoPart et Amundsen ?
- quelles variables CTD sont disponibles ?
- pourquoi une colonne est présente ou absente ?
```

Ce fichier est basé sur les exports et métadonnées réellement inspectés. Il doit rester proche des noms de colonnes réels.

---

# À quoi sert colonnes_instruments.md ?

Ce fichier décrit les colonnes EcoTaxa par instrument, surtout UVP5, UVP6 et ZooScan.

À utiliser quand l'utilisateur demande :

```text
- comment reconnaître un instrument depuis un export EcoTaxa ?
- que signifie une colonne sample_*, acq_*, process_* ou object_* ?
- quelles colonnes morphométriques sont disponibles ?
- comment interpréter acq_pixel, object_* ou fre_* ?
```

Ce fichier sert de dictionnaire technique EcoTaxa. Il complète `colonnes_sources.md`, mais il est plus général et orienté instrument.

---

# À quoi sert methodes_calcul.md ?

Ce fichier décrit les calculs que l'agent peut expliquer ou réaliser si les colonnes nécessaires existent.

À utiliser quand l'utilisateur demande :

```text
- calculer une concentration
- calculer une biomasse
- calculer un lipid fullness
- convertir fre_feret en taille biologique
- associer une variable CTD à un objet EcoTaxa
- savoir pourquoi un calcul n'est pas fiable
```

Ce fichier doit toujours distinguer :

```text
calcul fiable
calcul exploratoire avec avertissement
feedback si les colonnes manquent
```

L'objectif n'est pas de bloquer l'utilisateur, mais d'éviter d'inventer un résultat scientifique.

---

# À quoi sert copepodes_domaine.md ?

Ce fichier contient les connaissances biologiques sur les copépodes utiles au projet.

À utiliser quand l'utilisateur demande :

```text
- quelles espèces sont importantes ?
- quel est le rôle écologique d'une espèce ?
- que signifie diapause ?
- que représentent les lipides ?
- comment interpréter les stades de développement ?
- quels groupes fonctionnels sont pertinents ?
```

Ce fichier sert au contexte scientifique. Il ne remplace pas les données : il aide à interpréter les résultats.

---

# À quoi sert sources_en_ligne.md ?

Ce fichier indique où chercher les données ou métadonnées en ligne.

À utiliser quand l'utilisateur demande :

```text
- où trouver EcoTaxa ?
- où trouver EcoPart ?
- où trouver les données Amundsen ?
- quand utiliser OBIS ?
- quand utiliser CMEMS ?
- quelles sources nécessitent un compte ou une activation ?
```

Ce fichier guide les futurs tools ou MCP. Il ne doit pas contenir de secrets, tokens, mots de passe ou identifiants personnels.

---

# Quel est le format obligatoire d'un chunk RAG ?

Chaque chunk doit commencer par :

````markdown
---
# Titre sous forme de question ?
````

Le titre doit être une question claire, car l'agent récupère les chunks selon les questions utilisateur.

Format recommandé :

````markdown
---
# Question précise ?

Réponse courte.

Colonnes utiles :
```text
...
```

Unités :
```text
...
```

Limites :
- ...

Feedback si incomplet :
- ...
````

Pour un chunk de calcul, ajouter si nécessaire :

````markdown
Formule :
```text
...
```
````

Pour un chunk de source de données, ajouter si nécessaire :

````markdown
Source :
```text
...
```
````

---

# Quelles sont les règles d'écriture des chunks ?

Un chunk doit être autonome : il doit pouvoir être compris sans lire tout le fichier.

Un chunk doit être court : une question, une réponse, les colonnes ou limites utiles.

Un chunk ne doit pas mélanger plusieurs sujets. Si deux questions sont possibles, créer deux chunks.

Un chunk ne doit pas inventer des colonnes. Si une colonne est supposée mais non observée, l'écrire explicitement.

Un chunk doit garder les noms réels des colonnes quand ils sont connus.

Un chunk doit distinguer :

```text
donnée observée
donnée déduite
donnée attendue mais absente
```

---

# Quelles sont les règles scientifiques pour l'agent ?

L'agent doit citer la source utilisée quand il répond sur une donnée.

L'agent doit dire quand une information vient :

```text
- d'un export EcoTaxa
- d'un export EcoPart
- d'une métadonnée Amundsen
- d'une connaissance biologique générale
- d'une hypothèse de jointure
```

L'agent ne doit pas transformer un comptage EcoTaxa en concentration sans volume échantillonné.

L'agent ne doit pas transformer une mesure image en taille biologique sans calibration pixel.

L'agent ne doit pas transformer un biovolume ou une taille en biomasse carbone sans relation de conversion documentée.

L'agent doit donner un feedback utile quand un calcul n'est pas possible :

```text
- colonnes manquantes
- source à activer
- calcul alternatif possible
- niveau de fiabilité
```
