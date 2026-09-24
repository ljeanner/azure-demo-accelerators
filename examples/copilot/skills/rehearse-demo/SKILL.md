---
name: rehearse-demo
description: Prépare et vérifie un parcours de démonstration rejouable avec remise à zéro et mode de secours explicite. À utiliser avant une restitution ou une présentation Tech for Retail.
---

# Préparer une démonstration rejouable

## Entrées

Scénario validé, commande de lancement, résultats attendus, modes réel/simulé,
durée de présentation et environnement de démo dédié.

## Procédure

1. Définir l'état initial : versions, configuration, données, identités fictives,
   services nécessaires et actions déjà réalisées.
2. Préparer un script court reliant chaque action à un résultat observable.
   Distinguer résultat mesuré, résultat attendu et simulation.
3. Examiner les effets externes avant d'exécuter : neutraliser les envois et
   les opérations métier non nécessaires. Toute action réelle requiert une
   autorisation pour sa cible et son effet.
4. Préparer la remise à zéro limitée aux données et ressources de démo nommées.
   Ne pas proposer de suppression globale. Demander confirmation avant toute
   suppression ou écrasement, même pour réinitialiser un jeu synthétique.
5. Si l'environnement est disponible et les actions autorisées, jouer le
   parcours deux fois depuis le même état initial. Vérifier les résultats,
   l'absence de doublons et la durée réelle. Ne pas relancer une action externe
   sans vérifier son état et son autorisation.
6. Vérifier le comportement en cas d'indisponibilité d'une dépendance dans un
   contexte contrôlé, sans couper un service partagé. Le message d'erreur doit
   être explicite et le repli sélectionné volontairement.
7. Préparer une capture, une vidéo ou un mode simulé comme secours, étiqueté
   clairement. Nettoyer tout secret ou donnée sensible avant de conserver un support.

## Livrable

- Script : étape, action, résultat attendu, résultat observé, durée, réel/simulé.
- Commandes de lancement et procédure de remise à zéro avec périmètre.
- Résultat des deux passages et différences éventuelles.
- Checklist avant présentation, limites et procédure de secours.

Conclure « prêt à présenter » seulement si les deux passages satisfont les
critères. Sinon indiquer « à répéter » ou « bloqué » et les contrôles manquants.
Si tu ne peux pas exécuter, fournir une checklist manuelle sans inventer de résultat.
