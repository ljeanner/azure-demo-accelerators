---
applyTo: "**/*.bicep,**/*.bicepparam,**/*.tf,**/*.tfvars,**/azure.yaml,**/infra/**,**/deploy/**"
---

# Notre environnement Azure

Adapter `applyTo` aux fichiers de déploiement du projet.

- Environnement du groupe : << souscription et groupe de ressources, sans secret >>
- Région : << région >>
- Budget et durée de vie : << montant indicatif et date de nettoyage >>
- Outil de déploiement : << outil existant ou étapes manuelles >>

Réutiliser l'environnement préparé. Vérifier la cible, les accès et les prérequis ;
les accès Azure ne garantissent pas les accès Fabric ou M365.
Ne pas enregistrer de secrets, de plans sensibles ou d'état Terraform dans le dépôt.
Présenter les changements et les coûts estimés avant de demander confirmation pour déployer.
Faire aussi confirmer les changements de droits, l'exposition publique et les suppressions.
Ne pas supprimer de ressources partagées. Vérifier le fonctionnement après déploiement.
