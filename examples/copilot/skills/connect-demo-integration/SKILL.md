---
name: connect-demo-integration
description: Connecte un service réel à la démo en remplacement d'une source simulée.
---

# Connecter un service

Demander quel service connecter et quelle opération démontrer.

1. Lire le HLD et le code existant ; réutiliser le contrat de données.
2. Vérifier l'API et les prérequis dans la documentation officielle.
3. Ajouter la connexion sans écrire de secrets dans le code ou les logs.
4. Tester un appel simple, puis le comportement en cas d'erreur.
5. Documenter la configuration et ce qui a réellement été vérifié.

Conserver un mode simulé explicite, sans bascule automatique qui masque une panne.
Demander confirmation avant toute écriture ou action externe.
Ne pas relancer aveuglément une action qui pourrait créer un doublon.
Si l'accès manque, signaler le blocage plutôt qu'inventer un résultat.
