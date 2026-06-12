---
title: "Assistant copépodes — Mémoire courte et longue terme"
author: "Tidiane Cissé"
date: "2026-06-10"
version: "0.1"
lang: fr
status: "Draft"
---

# PRD — Mémoire de l’agent copépodes

## Problem Statement

L’agent oublie les corrections, décisions et préférences utiles dès qu’on change de `thread_id`. Aujourd’hui, le thread est la seule ancre réellement stable dans le runtime, alors que les ajustements donnés par un utilisateur devraient survivre à plusieurs threads et rester exploitables dans un nouveau contexte de travail.

Le besoin n’est pas de conserver tout l’historique brut. Le besoin est de retenir les corrections durables, les décisions de projet et le contexte utile pour que l’agent s’adapte au fil des conversations sans redemander les mêmes informations.

## Solution

Mettre en place une mémoire hybride pour l’agent copépodes :

- une mémoire courte terme liée au thread courant, pour garder l’état immédiat de la conversation et un résumé vivant de la session ;
- une mémoire longue terme séparée en scopes utilisateur et projet, pour retenir les corrections, préférences, décisions et contexte de travail qui doivent survivre à plusieurs threads ;
- une résolution d’identité applicative pour dériver ou injecter un `user_key` et un `project_key`, puisque ces identités ne sont pas encore portées de manière canonique dans le flux actuel ;
- une politique de lecture/écriture mémoire qui n’écrit que des faits durables, jamais le transcript brut complet.

La lecture mémoire doit se faire avant la génération d’une réponse. L’écriture mémoire doit se faire après détection d’une correction, d’une décision, d’un ajustement de préférence ou d’un contexte projet utile.

## User Stories

1. As a user, I want the agent to remember a correction I gave in a previous thread, so that I do not need to repeat it.
2. As a user, I want the agent to keep my preferences separate from other users, so that my style and constraints are not mixed with theirs.
3. As a user, I want the agent to retain project decisions across multiple threads, so that a new discussion continues from the same working context.
4. As a user, I want the agent to remember what was already decided in a project, so that I do not reopen settled points by accident.
5. As a user, I want the agent to keep short-term context for the current thread, so that follow-up messages stay coherent.
6. As a user, I want the agent to reload relevant memory when I start a new thread, so that the conversation does not restart from zero.
7. As a user, I want the agent to distinguish between a personal preference and a project decision, so that the right memory is updated.
8. As a user, I want the agent to ignore raw chat noise and only keep durable adjustments, so that memory stays useful and compact.
9. As a user, I want the agent to avoid leaking one project’s context into another project, so that discussions stay isolated.
10. As a user, I want the agent to avoid leaking one user’s preferences into another user’s session, so that memory stays private.
11. As a user, I want the agent to retain “do not do this again” instructions, so that repeated mistakes stop recurring.
12. As a user, I want the agent to remember how a project is structured, so that future threads can resume with the right assumptions.
13. As a user, I want the agent to keep track of corrections about terminology and workflow, so that it adapts its phrasing and process over time.
14. As a user, I want the agent to separate short-lived conversation state from long-lived memory, so that one does not overwrite the other.
15. As a user, I want the agent to recover the relevant context even after a restart, so that memory survives process restarts.
16. As a user, I want the agent to be able to say what it remembered and why, so that memory remains auditable.
17. As a user, I want the agent to update memory only when the information is clearly durable, so that accidental or speculative details are not persisted.
18. As a user, I want the agent to treat the same project opened in different threads as one shared working context, so that work can continue fluidly.

## Implementation Decisions

- Introduire une couche de mémoire explicite distincte de la gestion de session actuelle.
- Garder `thread_id` comme clé d’exécution et de mémoire courte terme uniquement.
- Ajouter une résolution d’identité applicative pour obtenir un `user_key` et un `project_key`.
- Utiliser un mécanisme de mémoire courte terme pour l’état du thread et son résumé.
- Utiliser un store pour la mémoire longue terme entre threads.
- Stocker les mémoires sous forme de records structurés, pas comme transcript brut, avec au minimum type, source, scope, timestamp et confiance.
- Séparer les namespaces de mémoire pour les préférences utilisateur, les décisions de projet, le contexte de projet et les instructions négatives.
- Fusionner la mémoire courte terme et la mémoire longue terme pertinente avant l’assemblage du prompt.
- Écrire en mémoire longue terme seulement quand l’agent détecte une correction durable, une préférence, une décision ou un contexte de projet utile.
- Prévoir un comportement de secours pour les cas où l’identité n’est pas résolue, afin d’éviter tout mélange entre utilisateurs.
- Définir des règles d’overwrite et de supersession pour que les corrections récentes puissent remplacer des mémoires plus anciennes lorsque c’est justifié.
- Conserver la traçabilité des entrées mémoire utilisées par l’agent.
- Garder cette mémoire indépendante du plumbing de feedback existant et du store de session déjà présent pour les artefacts d’exécution.

## Testing Decisions

- Tester le feature par le comportement externe, pas par les détails d’implémentation.
- Ajouter des tests qui vérifient qu’une correction écrite dans un thread est disponible dans un thread ultérieur avec le même scope utilisateur et projet.
- Ajouter des tests qui vérifient qu’une mémoire utilisateur ne fuit pas vers un autre utilisateur.
- Ajouter des tests qui vérifient qu’une mémoire projet ne fuit pas vers un autre projet.
- Ajouter des tests qui vérifient que la mémoire courte terme survit à une conversation reprise.
- Ajouter des tests qui vérifient que seules les corrections durables sont persistées, pas le bruit brut du chat.
- Ajouter des tests qui vérifient que la recherche mémoire se fait avant la génération de la réponse.
- S’aligner sur le style des tests d’intégration déjà présents dans le dépôt pour les endpoints et le comportement de conversation.
- Privilégier des tests ciblés sur la résolution de scope, la persistance, la récupération et les règles de reset.

## Out of Scope

- Les changements UI dans Open WebUI.
- Une refonte de l’authentification ou un provider d’identité complet.
- Une mémoire globale partagée entre tous les utilisateurs.
- L’interprétation scientifique automatique des discussions.
- Le backfill de tout l’historique des conversations vers le nouveau système de mémoire.
- Une interface de revue manuelle des entrées mémoire.
- Le partage de mémoire entre projets sans scope explicite.
- Le remplacement du store de session existant utilisé pour les artefacts de runtime.

## Further Notes

LangGraph sait déjà séparer ce besoin en deux parties : mémoire courte terme via checkpointer, mémoire longue terme via store. Le point manquant dans l’app actuelle est une couche d’identité stable capable d’alimenter ces scopes de manière fiable.

Le runtime expose aujourd’hui `thread_id`, `chat_id` et `session_id`, mais pas de `user_id` ou `project_id` canonique. L’identité applicative fait donc partie de la feature, pas d’un détail à repousser.

Slice de départ recommandé :

1. résoudre `user_key` et `project_key` ;
2. persister un résumé court terme du thread ;
3. persister une correction durable côté utilisateur ;
4. recharger les deux sur un nouveau thread ;
5. vérifier l’isolation entre scopes.
