---
applyTo: "**/*.bicep,**/*.bicepparam,**/*.tf,**/*.tfvars,**/azure.yaml,**/infra/**,**/deploy/**"
---

# Déploiement de démonstration Azure — à adapter

Adapter les chemins `applyTo` aux fichiers réellement concernés, y compris
les workflows de déploiement éventuels. Ces instructions ne sont pas un
contrôle d'accès ; conserver les garde-fous des outils et de l'environnement.

## Cible du groupe

- Environnement autorisé : << environnement de démonstration dédié >>
- Souscription et groupe de ressources : << références locales, sans secret >>
- Région envisagée : << région à vérifier pour chaque service >>
- Convention de nommage et tags : << groupe, projet, propriétaire, expiration >>
- Budget indicatif et durée de vie : << montant, devise, durée >>
- Outil existant : << Bicep / Terraform / azd / étapes manuelles >>
- Services Fabric ou M365 associés : << références ou non applicable >>

## Règles

- Réutiliser l'environnement préparé et l'outillage existant. Ne pas automatiser
  la création de tenants pour ce hackathon ni migrer d'outil sans demande.
- Vérifier le contexte cible, les services disponibles, les quotas, les licences
  et les permissions avant de proposer un déploiement.
- Séparer les ressources Azure des éléments Fabric/M365 : ne pas supposer
  qu'un template Azure configure automatiquement ces derniers.
- Paramétrer les valeurs propres au groupe. Ne pas conserver de secrets ni
  d'état Terraform ou de plans susceptibles d'en contenir dans le dépôt.
- Privilégier les identités et permissions minimales adaptées au service.
  Ne pas ouvrir un accès public ou élargir des droits pour contourner un blocage.
- Avant toute application, présenter les ressources ajoutées, modifiées ou
  supprimées, la cible, les conséquences et le coût estimé avec sa source
  et ses hypothèses. Si le coût est inconnu, le signaler.
- Utiliser la validation ou prévisualisation disponible avant application.
  Un plan ou un what-if ne prouve ni le succès futur ni le coût exact.
- Obtenir une confirmation explicite avant création payante, changement de
  droits, exposition publique, écrasement ou suppression. Un champ renseigné
  ci-dessus n'est pas une autorisation d'exécution.
- Ne pas considérer une alerte budgétaire comme un plafond de dépense.
- Après application autorisée, vérifier l'état puis le parcours applicatif.
  Ne pas déclarer la démo fonctionnelle sur le seul succès du provisionnement.
- Documenter l'arrêt et le nettoyage avec la liste exacte des ressources.
  Ne jamais supprimer un groupe partagé ; demander confirmation du périmètre.
