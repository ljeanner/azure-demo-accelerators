---
name: demo-preflight
description: Vérifie les prérequis d'une démonstration Azure avant le build ou le déploiement. À utiliser pour contrôler les accès, ressources, licences, quotas et connexions d'un HLD sans modifier l'environnement.
---

# Vérifier les prérequis

## Entrées

Scénario, HLD, services retenus, environnement du groupe et temps disponible.
Demander uniquement les informations manquantes qui empêchent la vérification.
Ne jamais demander de copier un secret dans la conversation.

## Procédure

1. Lire le contexte du projet et lister les dépendances réellement utiles au
   parcours. Écarter les services simplement cités comme possibilités.
2. Vérifier les outils et versions requis par les commandes du projet.
3. Identifier séparément les périmètres Azure, Fabric et M365 concernés :
   souscription, groupe de ressources, workspace, tenant et identités.
   Une connexion Azure ne prouve pas un accès à Fabric ou M365.
4. Avec les outils disponibles, effectuer uniquement des contrôles de lecture :
   contexte connecté, existence des ressources, droits observables, connectivité
   et quota/capacité si consultables. Ne pas afficher de jetons ni de secrets.
5. Vérifier les prérequis produit dans Microsoft Learn. Distinguer prérequis
   documenté et disponibilité effectivement constatée dans cet environnement.
6. Pour chaque contrôle impossible, indiquer « non vérifié », la raison et une
   procédure manuelle précise. Ne pas interpréter l'absence d'erreur comme une preuve.
7. Proposer, sans l'appliquer, une réduction du périmètre ou une simulation
   explicite si le groupe ne peut pas résoudre un blocage pendant la session.

## Résultat attendu

| Prérequis | Statut | Preuve datée ou source | Action suivante |
|---|---|---|---|
| Élément contrôlé | OK / bloqué / non vérifié / non applicable | Observation sans secret | Action et responsable à désigner |

Conclure « prêt », « prêt sous conditions » ou « bloqué » pour le parcours
concerné. Un prérequis critique non vérifié empêche de conclure « prêt ».
Ne pas provisionner, installer, changer les droits, se connecter avec de
nouveaux identifiants ou activer un service dans cette procédure.
