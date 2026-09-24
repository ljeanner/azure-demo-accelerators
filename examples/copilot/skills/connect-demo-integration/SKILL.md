---
name: connect-demo-integration
description: Remplace une intégration simulée par une source réelle validée dans le HLD. À utiliser pour connecter un service à la démo sans masquer les erreurs ni exposer les secrets.
---

# Connecter une intégration

## Entrées

Identifier la source, le contrat de données existant, le composant appelant,
le mode d'authentification prévu et une opération minimale à démontrer.
Ne pas choisir un nouveau service ou connecteur sans validation du groupe.

## Procédure

1. Lire l'implémentation simulée et le HLD. Rechercher les clients, adaptateurs
   et mécanismes de configuration déjà utilisés par le projet.
2. Vérifier dans la documentation publique du service l'API ou le connecteur,
   ses prérequis, les permissions et ses limites. Ne pas inventer une API SAP,
   Fabric ou M365 ni supposer qu'un outil MCP est installé.
3. Contrôler les prérequis en lecture seule. S'il manque un accès, signaler
   le blocage et fournir les étapes à l'administrateur ; ne pas élargir les droits.
4. Implémenter la connexion derrière le contrat existant avec validation des
   réponses, délais d'attente bornés et erreurs explicites. Réutiliser la gestion
   des secrets du projet ; ne pas journaliser de credentials ou de données sensibles.
5. Garder un mode simulé sélectionné explicitement et visible à l'écran.
   En mode réel, une panne doit être affichée, pas remplacée par un faux succès.
6. Commencer par une lecture minimale autorisée. Avant un envoi, une écriture,
   un transfert de stock ou une autre action externe, présenter la cible et
   l'effet puis obtenir une confirmation explicite.
7. Pour les actions, empêcher les doublons selon les capacités du service
   (idempotence ou contrôle d'état). Ne pas réessayer aveuglément une écriture.
   Conserver l'approbation humaine prévue dans le scénario.
8. Tester le contrat, la configuration manquante, le refus d'accès, le timeout,
   la réponse invalide et le succès. Séparer tests simulés et vérification réelle.

## Livrables

Connexion implémentée, configuration sans secrets, tests ciblés, procédure de
lancement et tableau des modes réel/simulé. Indiquer la preuve de l'appel réel
ou « connexion réelle non vérifiée » si aucun environnement n'est accessible.
Ne pas qualifier une intégration de fonctionnelle sur la seule base d'un mock.
