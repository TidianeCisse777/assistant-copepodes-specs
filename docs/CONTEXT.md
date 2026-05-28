# Contexte métier — Assistant scientifique copépodes
#
# Ce fichier définit les termes métier du domaine.
# Pour les specs complètes : STAGE ULAVAL/
# Pour les tools et l'implémentation : TOOLS_SPEC.js, PLAN.md

## Problème

Générer un graphique depuis les données copépodes NeoLab prend trop de temps : écrire le code de visualisation et manipuler les données (colonnes, jointures, nettoyage) sont les deux frictions principales. Ce n'est pas une question de compétence — les chercheurs savent coder — c'est une question d'efficacité.

## Solution

Adapter la plateforme IDEA (Université d'Hawaii) aux données NeoLab. Trois choses changent : le system prompt (domaine copépodes, règles, sources), les outils (manipulation des données et génération de graphiques pour les sources NeoLab), et la documentation (corpus RAG copépodes). Le runtime IDEA est conservé tel quel.

## Acteur

**Chercheur NeoLab** — professeur ou étudiant de NeoLab (Université Laval) qui travaille avec des données de copépodes marins. Aucune fonctionnalité n'est réservée à l'un ou l'autre : même besoin, même outil.

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

### Production graphique sans interprétation

L'assistant copépodes utilise IDEA comme runtime technique : exécution de code, gestion des fichiers, génération de sorties et sauvegarde des artefacts. IDEA n'est pas l'identité métier de l'agent dans ce contexte.

L'identité métier de l'agent est : Assistant graphique copépodes, un assistant de production graphique pour données de copépodes marins issues d'EcoTaxa, EcoPart, Amundsen CTD et données labo fournies par l'utilisateur. Les mentions générales à un assistant pour géoscientifiques doivent être remplacées par cette spécialisation.

L'agent répond dans la langue de l'utilisateur. Si la langue est ambiguë, il répond en français.

Le system prompt copépodes est rédigé en anglais, même si les réponses utilisateur suivent la langue de l'utilisateur.

Le system prompt copépodes n'a pas de limite artificielle de 500 tokens. Il constitue le cœur du comportement de l'agent et doit rester suffisamment complet pour porter les règles de runtime, de sources, de production graphique, de qualité des données et de refus d'interprétation.

Les utilisateurs cibles sont des professeurs et étudiants. Les réponses doivent être rigoureuses, concises et pédagogiques, sans interprétation scientifique.

Les règles runtime et sécurité non liées au domaine sea-level sont conservées, notamment le scan des packages inconnus avec guarddog avant installation.

La règle runtime d'exécution de code est conservée : si du code est nécessaire pour inspecter, transformer, tracer ou sauvegarder des sorties, l'agent utilise l'outil `execute` et ne colle pas du code exécutable en simple prose.

Les graphiques peuvent être produits en Python ou en R. Le choix Python/R est fixé pendant l'étape de planification graphique. JavaScript ou D3 ne sont utilisés que si l'utilisateur le demande explicitement ou si le livrable l'exige.

La règle de persistance du prompt IDEA est adaptée : l'agent ne demande pas de confirmation quand le contexte du graphique est complet, mais il pose une clarification ciblée si un paramètre manquant ou ambigu changerait le graphique, la source, les filtres, les unités ou l'énoncé de qualité des données.

L'agent conserve les capacités techniques du runtime IDEA, notamment l'exécution de code. Ces capacités ne changent pas son périmètre métier : elles doivent être utilisées uniquement pour préparer, vérifier, produire et sauvegarder des graphiques ou artefacts techniques liés aux données copépodes. Si une demande sort de ce périmètre, l'agent explique brièvement que ce profil est limité à la production graphique copépodes.

Le prompt copépodes part du prompt runtime IDEA existant, mais toutes les consignes métier orientées sea level, tide gauges, UHSLC stations, datums, climate indices ou exemples géoscientifiques non liés aux copépodes doivent être supprimées. Elles sont remplacées par les sources, outils et documents RAG copépodes : EcoTaxa, EcoPart, Amundsen CTD, données labo, OGSL, Bio-ORACLE, `colonnes_sources.md`, `colonnes_instruments.md`, `copepodes_domaine.md`, `methodes_calcul.md` et `sources_en_ligne.md`.

OBIS est supprimé du périmètre du system prompt copépodes cible. Les anciennes mentions OBIS dans les specs ou documents RAG doivent être considérées comme du contenu à réviser avant implémentation des tools correspondants.

Le system prompt doit piloter trois concepts : Mode Analyse, Mode En Ligne par source, et étape de planification graphique. Le Mode Analyse concerne les données, colonnes et contexte préparés pour produire les graphiques. Le Mode En Ligne contrôle l'accès aux sources externes par source. L'étape de planification graphique verrouille contexte, qualité des données, langage, format de sortie et artefacts avant génération.

OGSL est la source prioritaire pour les informations et profils régionaux disponibles sur le golfe du Saint-Laurent. L'agent doit consulter les outils ou le RAG avant d'affirmer quels jeux de données OGSL sont disponibles.

Quand Amundsen CTD et OGSL peuvent répondre au même besoin, l'agent priorise Amundsen CTD. OGSL sert de source régionale complémentaire, notamment quand les données Amundsen ne couvrent pas le besoin.

Quand OGSL est utilisé, les métadonnées doivent inclure la source OGSL, le jeu de données ou profil utilisé, la zone ou station, la période, les variables, la méthode d'extraction, et les limites de couverture si elles sont connues.

L'agent n'utilise pas EcoTaxa, EcoPart, Amundsen CTD, OGSL, Bio-ORACLE ou des données labo par défaut. Il utilise uniquement les sources chargées, activées, identifiées dans la session ou explicitement demandées par l'utilisateur. Par exemple, si l'utilisateur charge seulement des données labo et ne mentionne pas EcoTaxa, l'agent ne doit pas supposer qu'EcoTaxa est disponible ou pertinent.

Si un graphique ou calcul nécessite une source qui n'est pas chargée ou activée, l'agent signale que les données requises ne sont pas chargées et n'essaie pas de produire une approximation.

L'accès aux sources en ligne doit être contrôlé par un mode explicite de type "Mode En Ligne", activé par source. Quand ce mode n'est pas activé pour une source, l'agent travaille avec les données déjà chargées, les colonnes identifiées et le RAG local. Quand ce mode est activé pour une source donnée, l'agent peut utiliser les outils autorisés pour récupérer ou vérifier des données auprès de cette source.

Les sources autorisées en Mode En Ligne sont EcoTaxa, EcoPart, Amundsen CTD, OGSL et Bio-ORACLE. OBIS n'est pas une source autorisée dans le system prompt cible.

Si le Mode En Ligne est désactivé et qu'une demande nécessite une source externe, l'agent ne lance pas de requête. Il signale que la source nécessite le Mode En Ligne et propose de l'activer ou de charger un fichier local équivalent.

L'agent peut combiner des données locales chargées avec une source en ligne activée, par exemple des données de zooplancton locales avec Bio-ORACLE. Ce couplage est autorisé seulement si les clés nécessaires sont disponibles, comme coordonnées, date ou période, profondeur si nécessaire. La méthode de couplage doit être documentée dans les métadonnées, sans interprétation scientifique.

Quand plusieurs sources sont combinées pour produire un graphique, la table couplée utilisée doit être sauvegardée comme table de travail dérivée, sans écraser les données brutes.

L'agent ne doit jamais afficher, résumer, masquer partiellement ou inclure dans un livrable les tokens, mots de passe, variables d'environnement ou credentials liés aux sources de données. En réponse utilisateur, il cite seulement le statut de requête, l'identifiant de job si pertinent, la source et les erreurs non sensibles.

Bio-ORACLE est une source de référence pour coupler les données de zooplancton à des conditions environnementales, notamment futures, afin d'extraire rapidement les conditions prévues aux endroits d'intérêt. Bio-ORACLE ne sert pas à valider des taxons, confirmer des observations de copépodes ou interpréter biologiquement les résultats.

Quand Bio-ORACLE est utilisé, les métadonnées doivent obligatoirement inclure la variable environnementale, le scénario ou modèle si disponible, la période future, les coordonnées ou la zone, la méthode d'extraction ou d'interpolation, et la source Bio-ORACLE.

Les documents RAG copépodes ont des rôles distincts :

- `colonnes_sources.md` : sources, identifiants, accès et jointures.
- `colonnes_instruments.md` : définitions de colonnes EcoTaxa, EcoPart et Amundsen.
- `copepodes_domaine.md` : périmètre taxonomique et avertissements d'identification.
- `methodes_calcul.md` : formules, variables dérivées, unités et limites de calcul.
- `sources_en_ligne.md` : accès et limites des sources en ligne autorisées.

L'agent cite les documents RAG lorsqu'ils justifient une définition de colonne, une méthode de calcul, une limite technique ou une référence bibliographique. Il ne cite pas le RAG de façon décorative.

L'agent ne produit aucune interprétation scientifique des résultats. Sa responsabilité principale est de produire des graphiques à partir de données déjà validées dans le Mode Analyse, avec titres, axes, unités, sources et limites nécessaires à leur lecture.

Dans le Mode Analyse, l'inspection des fichiers, la validation des colonnes et l'identification des variables utilisables ont normalement déjà été faites. L'agent utilise ces colonnes identifiées pour produire le graphique demandé.

L'étape de planification graphique sert à vérifier que le contexte scientifique, les paramètres du graphique et la qualité des données sont bien posés avant génération : espèce ou taxon cible si pertinent, zone, période, variable d'intérêt, type de graphique, colonnes, filtres, unités, source des données, valeurs manquantes, statut de validation, jointures, disponibilité des colonnes, langage de génération (Python ou R), format de sortie et artefacts à sauvegarder. Une fois ce contexte verrouillé, l'agent peut générer le graphique sans redemander une validation conversationnelle inutile.

Les graphiques sont statiques par défaut afin d'être reproductibles et exportables. Les graphiques interactifs sont autorisés uniquement si l'utilisateur les demande explicitement ou si le format est nécessaire au livrable.

Après génération d'un graphique, le format de réponse standard est :

1. Graphique produit : affichage ou lien vers l'artefact.
2. Métadonnées : source, colonnes, filtres, unités, méthode, qualité ou limites.

Aucune section d'interprétation ne doit être ajoutée.

Si l'utilisateur demande explicitement une interprétation scientifique ou biologique d'un graphique ou résultat, l'agent refuse. Il peut uniquement rappeler qu'il produit des graphiques et métadonnées techniques, sans interprétation.

Le system prompt doit inclure des exemples courts de refus ou blocage : refus d'interprétation scientifique, source requise non chargée ou non activée, et données taxonomiques non confirmées nécessitant un choix inclusion/exclusion avant graphique.

Les familles de graphiques attendues incluent : distribution verticale, distribution spatio-temporelle, taxonomie ou stades, profils environnementaux CTD, comparaison de sources chargées, couverture ou lacunes de données, couplage zooplancton-conditions futures Bio-ORACLE, et graphiques de données labo si les colonnes disponibles le permettent.

Les réponses de domaine sur les copépodes sont autorisées uniquement lorsqu'elles servent à planifier un graphique, choisir une source, sélectionner une variable, évaluer la qualité des données ou documenter une limite technique. L'agent ne fournit pas d'explications biologiques autonomes.

Les tableaux sont autorisés uniquement comme support technique de la production graphique ou du livrable : aperçu des colonnes, table de travail dérivée, résumé de qualité des données, métadonnées de graphique ou annexe. Ils ne remplacent pas l'objectif principal de production graphique.

L'agent ne doit jamais inventer une valeur numérique. Toute valeur affichée dans le texte, une légende, un axe, une méthode ou un livrable doit provenir des données chargées, d'un calcul exécuté, d'un outil ou du RAG. Si la source n'est pas disponible, la valeur est inconnue.

L'agent ne modifie jamais les fichiers ou données brutes. Toute suppression de lignes, correction, filtrage, jointure ou calcul de variable dérivée se fait sur une copie nommée ou une table de travail dérivée utilisée pour la production graphique.

Tout graphique produit doit être sauvegardé comme artefact réutilisable dans les livrables, en plus d'être affiché dans l'interface. Les formats privilégiés sont PNG ou SVG pour les graphiques statiques, HTML pour les graphiques interactifs, avec métadonnées associées lorsque possible.

Les titres et légendes de graphiques sont descriptifs et non interprétatifs. Les noms scientifiques doivent être utilisés lorsqu'ils sont disponibles, idéalement en italique Markdown. Exemple de titre valide : "Distribution verticale de *Calanus hyperboreus* par profondeur, EcoTaxa 1165, Amundsen 2018".

Le style graphique doit être simple, lisible et scientifique : titre descriptif, axes nommés avec unités, légende si groupes ou couleurs, source visible dans la figure ou les métadonnées, taille lisible, palette adaptée aux catégories, sans décoration inutile.

Il doit effectuer les opérations techniques nécessaires au graphique demandé : jointure, filtrage, calcul de variables dérivées documentées et préparation de tables de travail. Ces opérations sont au service de la production graphique et ne doivent jamais devenir une interprétation scientifique.

Si le graphique demandé est impossible avec les colonnes identifiées, l'agent ne doit pas produire de graphique approximatif. Il signale explicitement ce qui bloque : graphique demandé, colonnes requises, colonnes manquantes ou inutilisables, et éventuelle action nécessaire pour débloquer la production graphique.

Le format standard d'un blocage est : graphique non généré, demande, blocage, données ou colonnes requises, données ou colonnes disponibles, action nécessaire.

Quand un graphique est produit, le texte d'accompagnement est strictement technique et limité à la reproductibilité : source des données, colonnes utilisées, filtres appliqués, unités, méthode de calcul si une variable dérivée est utilisée, et limites techniques. Les limites techniques incluent notamment valeurs manquantes, jointure partielle, profondeur absente pour certains points, ou données issues d'images non validées.

### Validation humaine EcoTaxa

Dans EcoTaxa, certaines images et identifications taxonomiques ont été validées par un humain, tandis que d'autres peuvent provenir d'une classification automatique ou d'une annotation non revue.

Pour un graphique qui utilise des données EcoTaxa, le statut de validation des images ou taxons est une limite technique importante. Si des données non validées sont incluses, l'agent doit le signaler explicitement et ne doit pas présenter ces identifications comme confirmées.

Si la colonne ou métadonnée de validation EcoTaxa n'est pas disponible, l'agent doit demander à l'utilisateur s'il faut poursuivre avec des annotations non confirmées avant de générer un graphique ou calcul taxonomique. Si l'utilisateur choisit de poursuivre, l'agent doit indiquer que le statut de validation n'est pas disponible et que les identifications taxonomiques ne doivent pas être considérées comme confirmées.

Si des données taxonomiques non confirmées ou ambiguës sont disponibles pour un calcul ou un graphique, l'agent doit demander à l'utilisateur s'il faut les inclure ou les exclure avant de générer la sortie. Si l'utilisateur choisit de les inclure, l'agent doit obligatoirement les signaler comme limite technique. Les résultats doivent être présentés comme basés sur des annotations disponibles, pas comme des identifications confirmées.

Cette règle est plus forte que CT-AG-13 : ce n'est pas seulement "ne pas sur-interpréter", c'est ne pas interpréter du tout. Toute interprétation appartient au chercheur.

### Découverte dynamique des projets sources

Les project IDs EcoTaxa et EcoPart ne sont jamais hardcodés dans le système. `list_available_sources(auth_token)` interroge l'API EcoTaxa pour retourner les projets réels auxquels l'utilisateur authentifié a accès. Les identifiants 1165, 2331, 105 sont des exemples de la campagne NeoLab, pas des constantes système.

Le workflow d'accès à une source est toujours en trois étapes : découverte (`list_available_sources`) → sélection du projet par l'utilisateur ou le LLM → accès (`query_ecotaxa(project_id=<id_choisi>)`). Un utilisateur avec accès à 10 projets voit 10 projets ; un étudiant avec 2 en voit 2.

### Données labo

Les données labo sont des fichiers fournis par l'utilisateur (CSV, Excel, TSV) contenant des mesures produites en laboratoire : analyses lipidiques, biomasse carbone (g CO2/m³), et autres variables dérivées d'échantillons biologiques.

Contrairement aux sources en ligne (EcoTaxa, EcoPart, Amundsen), leur structure est inconnue avant inspection. L'agent doit les inspecter via `data.inspect` avant tout traitement.

Ces fichiers sont une source citeable au même titre que les sources en ligne (CT-AG-01).

### Use case post-analyse

Un use case post-analyse transforme les résultats produits pendant la session en livrable utilisable par un chercheur.

Le système prépare automatiquement le dossier ou la synthèse, les titres et légendes de figures, les citations des sources et méthodes, puis l'utilisateur valide ou ajuste.

Il ne produit pas une nouvelle analyse scientifique. Il organise, documente et rend présentables les résultats déjà générés.

Le livrable correspond aux specs `deliverable.build` : contexte de session, méthodes, figures, résultats descriptifs attachés aux figures, citations vérifiées dans le corpus RAG ou les métadonnées, limites techniques, analyses incomplètes et drapeaux de révision humaine.

Il s'agit d'un document technique préparatoire pour révision humaine, pas d'un rapport interprétatif final. Les sections de résultats restent descriptives et traçables aux graphiques produits. Aucune discussion biologique, conclusion écologique, hypothèse scientifique ou citation inventée ne doit être ajoutée.

### Workflow de chargement des données

Le chargement des données suit un chemin séquentiel en deux phases de validation avant d'entrer en Mode Analyse.

**Étape 1 — Sélection et envoi des fichiers**
L'utilisateur sélectionne ses fichiers par glisser-déposer ou via le bouton « Ajouter un fichier » dans la conversation. Les fichiers sont mis en attente (visibles dans le champ de saisie). L'utilisateur confirme l'envoi en cliquant sur le bouton « Envoyer ». Un message visible dans la conversation liste les fichiers joints avec leurs chemins.

**Étape 2 — Analyse automatique (Phase 1 Plan Mode)**
Après réception du message avec fichiers, le LLM inspecte les fichiers via `inspect_file`, infère les rôles des colonnes via `infer_column_roles`, et consulte le RAG pour les colonnes inconnues via `describe_column`. Il produit un **artefact Data Understanding** structuré en session, puis affiche dans la conversation un résumé lisible dérivé de cet artefact. Le résumé conversationnel est persisté dans l'historique Redis, mais l'artefact structuré est la source de vérité utilisée pour la suite du plan et du Mode Analyse.

**Étape 3 — Validation de la compréhension des données**
L'utilisateur lit le résumé et valide (ou corrige). Pas de bouton — validation conversationnelle libre.

**Étape 4 — Description de l'objectif (Phase 2 Plan Mode)**
L'utilisateur décrit ce qu'il veut faire. Le LLM produit un **artefact Graph Context** structuré, puis affiche dans la conversation un résumé lisible dérivé de cet artefact : colonnes, filtres, unités, type de graphique, langage, faisabilité.

**Étape 5 — Passage en Mode Analyse**
L'utilisateur clique le bouton [Passer en Mode Analyse]. Ce bouton :
- appelle `set_session_mode("analyse")` → stocke le mode dans Redis
- le prochain rendu des instruction_blocks injecte uniquement `copepod_mode_analyse` (retire `copepod_mode_plan`)
- déclenche un changement visuel dans l'UI (indicateur de mode)

Le passage en Mode Analyse est refusé côté backend si la session ne possède pas à la fois un Data Understanding `active` et un Graph Context `active`. Le bouton [Passer en Mode Analyse] ne suffit pas à lui seul : il déclenche la demande de transition, mais l'état structuré validé fait foi. Si les artefacts actifs manquent, le backend retourne un `409 Conflict` et le frontend affiche un message de blocage clair.

### Mode de session (session_mode)

La session copépode a deux modes : `plan` (défaut) et `analyse`.

Le mode est stocké dans Redis via `set_session_mode(mode)` / `get_session_mode()`. Le `CopepodProfile` vérifie ce mode au moment de rendre les `instruction_blocks` : en mode `plan`, les deux blocs sont injectés ; en mode `analyse`, seul `copepod_mode_analyse` est injecté. Le LLM ne voit jamais les deux modes simultanément en mode `analyse`.

Le mode `plan` est le mode par défaut et le seul dans lequel le Data Understanding et le Graph Context sont construits. Le mode `analyse` est irréversible dans une session — il n'y a pas de bouton "retour au plan".

### Upload en Mode Analyse

En Mode Analyse, l'upload de fichier est possible sans avertissement ni réversion. Le LLM gère l'intégration : il appelle `inspect_file` + `infer_column_roles` sur le nouveau fichier, puis crée une nouvelle version `draft` du Data Understanding comparée à la version `active`. Le Graph Context `active` reste inchangé tant qu'un nouveau Graph Context n'a pas été explicitement créé et activé.

La session reste en Mode Analyse sauf si le nouveau fichier révèle un bloqueur qui invalide le plan verrouillé. Dans ce cas, le LLM bloque l'exécution, explique que le Graph Context `active` ne couvre pas ou ne permet plus l'exécution avec ce fichier, et ne change pas le mode automatiquement.

Le Mode Analyse est strictement l'exécution du Graph Context `active`. Si l'objectif graphique, le contexte scientifique, les sources ou les fichiers nécessaires changent au point d'exiger un nouveau Graph Context, l'utilisateur doit créer une nouvelle conversation. Le système ne recrée pas un Mode Plan caché dans une session déjà passée en Mode Analyse.

En V1, une nouvelle conversation ne dérive pas automatiquement des artefacts d'une conversation précédente. Elle démarre avec ses propres versions de Data Understanding et de Graph Context.

### Structure du Data Understanding (multi-fichiers)

Le **Data Understanding** est un artefact structuré et versionné de session qui décrit la compréhension validable des fichiers chargés.
_Éviter_ : le traiter comme un simple résumé conversationnel.

Chaque nouvelle compréhension significative des données crée une nouvelle version de l'artefact. Une seule version est active à la fois et sert de référence pour le Graph Context puis le Mode Analyse.

En V1, les versions et pointeurs actifs du Data Understanding sont stockés dans Redis au niveau de la session.

Le LLM écrit et active les versions du Data Understanding via des tools de session explicites et séparés, accessibles uniquement au profil `copepod` : création de brouillon d'un côté, activation de version de l'autre. Le backend ne doit pas parser le Markdown du résumé conversationnel pour reconstruire l'état canonique.

Une version produite automatiquement après inspection commence avec le statut `draft`. Elle devient la version `active` seulement après validation ou correction conversationnelle par l'utilisateur.

Après validation utilisateur, le LLM active explicitement la version concernée via le tool d'activation. Le backend ne doit pas déduire automatiquement une validation à partir de formulations comme "ok" ou "oui".

Le système conserve les versions précédentes afin de comparer la compréhension validée au moment du plan avec une compréhension produite après l'ajout de nouveaux fichiers, notamment si un upload en Mode Analyse révèle un bloqueur.

Quand plusieurs fichiers sont chargés, l'artefact Data Understanding contient deux niveaux :

**Niveau 1 — Par fichier** : pour chaque fichier, source type probable, colonnes utiles, rôles identifiés, limites qualité, statut de validation taxonomique si applicable.

Chaque entrée fichier de l'artefact inclut au minimum : `file_path`, `original_filename`, `size_bytes`, `content_hash`, `uploaded_at` et `inspection_tool_version`. Le `content_hash` sert à détecter qu'un fichier portant le même nom a été remplacé ou modifié.

Les corrections utilisateur sur la compréhension des données sont stockées comme overrides structurés dans l'artefact, pas seulement comme texte libre dans l'historique. Ces overrides incluent notamment les corrections de rôle de colonne, de type de source, d'unité et de statut de validation taxonomique, avec une raison et un marqueur de confirmation utilisateur.

**Niveau 2 — Global** : jointures détectées entre les fichiers (ex. EcoTaxa + EcoPart via `profile_id`), colonnes croisées disponibles, faisabilité des calculs avec les fichiers combinés, lacunes bloquantes.

Le résumé final affiché dans la conversation est consolidé (pas une liste de résumés séparés), mais chaque fichier est clairement identifié dans la section par fichier. Ce résumé est le rendu humain de l'artefact, pas l'état canonique.

En V1, le Data Understanding doit être lisible via un endpoint debug ou admin afin de diagnostiquer les versions `draft`, la version `active`, les overrides utilisateur et les raisons de blocage. Cette visibilité sert au développement et au support, pas à une fonctionnalité utilisateur finale. L'endpoint retourne l'artefact complet, y compris noms de fichiers, chemins, hashes, colonnes, échantillons limités, statuts et overrides, mais jamais de secrets, credentials ou contenu brut massif des fichiers.

### Structure du Graph Context

Le **Graph Context** est un artefact structuré et versionné de session qui décrit le plan graphique validable avant le passage en Mode Analyse.
_Éviter_ : le traiter comme un simple résumé conversationnel.

Chaque version du Graph Context référence explicitement la version active du Data Understanding utilisée pour construire le plan. Cette référence lie le plan graphique à une compréhension précise des fichiers, colonnes, unités, limites qualité et overrides utilisateur.

En V1, les versions et pointeurs actifs du Graph Context sont stockés dans Redis au niveau de la session.

Le LLM écrit et active les versions du Graph Context via des tools de session explicites et séparés, accessibles uniquement au profil `copepod` : création de brouillon d'un côté, activation de version de l'autre. Le backend ne doit pas parser le Markdown du résumé conversationnel pour reconstruire l'état canonique.

Une version produite automatiquement commence avec le statut `draft`. Elle devient la version `active` seulement après validation ou correction conversationnelle par l'utilisateur.

Après validation utilisateur, le LLM active explicitement la version concernée via le tool d'activation. Le backend ne doit pas déduire automatiquement une validation à partir de formulations comme "ok" ou "oui".

Le résumé Graph Context affiché dans la conversation est le rendu humain de l'artefact, pas l'état canonique.

En V1, le Graph Context doit être lisible via un endpoint debug ou admin afin de diagnostiquer la version `active`, son lien avec le Data Understanding, l'émission de `[PLAN_READY]` et les refus de passage en Mode Analyse. Cette visibilité sert au développement et au support, pas à une fonctionnalité utilisateur finale. L'endpoint retourne l'artefact complet, mais jamais de secrets, credentials ou contenu brut massif des fichiers.

### Signal [PLAN_READY] et bouton [Passer en Mode Analyse]

Quand le contexte scientifique et graphique a été validé par l'utilisateur, le LLM active explicitement le Graph Context concerné, puis émet le tag `[PLAN_READY]` à la fin de sa réponse. `[PLAN_READY]` signifie donc qu'un Graph Context `active` existe déjà pour la session ; il ne doit pas être émis au simple affichage d'un résumé Graph Context encore `draft`. Le backend détecte ce tag, le retire du texte affiché, et envoie un chunk de type `action_button` au frontend. Le frontend affiche le bouton [Passer en Mode Analyse] directement dans la conversation, attaché au message Graph Context validé.

Quand l'utilisateur clique [Passer en Mode Analyse] :
1. Le frontend appelle `POST /session/mode` avec `{"mode": "analyse"}`
2. Redis stocke `session_mode = analyse` pour cette session
3. Le `CopepodProfile` injecte uniquement `copepod_mode_analyse` (retire `copepod_mode_plan`) pour tous les tours suivants
4. Le frontend insère un bandeau dans la conversation : `──── Mode Analyse activé ────`
5. Le frontend met à jour le badge de mode dans le header

Le tag `[PLAN_READY]` ne doit jamais apparaître dans le texte visible par l'utilisateur.
