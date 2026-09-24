# Azure Demo Accelerators

Ce dépôt public rassemble des recettes de démonstration Azure, Fabric et IA.
Dans le cadre du hackathon RCG, elles servent à construire des démonstrations
réutilisables pour Tech for Retail, pas des solutions de production.

## Repères du dépôt

- `README.md` : catalogue et démarrage rapide.
- `CONTRIBUTING.md` : règles de contribution et de publication.
- `_template\README.md` : modèle pour un nouvel accélérateur.
- `accelerators\` : recettes, prompts et checklists par accélérateur.
- `examples\copilot\` : exemples pédagogiques à adapter ; ils ne constituent
  pas des agents, skills ou instructions automatiquement activés dans ce dépôt.
- Le dépôt est actuellement documentaire : ne pas inventer de commande de build
  ou de test. Pour du code ajouté, documenter et exécuter la validation adaptée.

## Règles communes

- Partir du problème métier, des personas, du parcours et du résultat attendu.
  Ne pas imposer Fabric, SAP, Foundry ou un autre service sans besoin validé.
- Réutiliser les recettes et composants existants avant d'en créer de nouveaux.
  Garder le périmètre réalisable pendant la session.
- Utiliser uniquement des entreprises et personnes fictives, des données
  synthétiques et des sources publiques. Ne pas ajouter de notes internes,
  données client, informations personnelles ou contenu confidentiel.
- Ne jamais écrire de secrets, jetons ou chaînes de connexion sensibles dans
  les fichiers ou les journaux. Documenter les noms des paramètres, pas leurs valeurs.
- Rendre les données reproductibles : graine, dates, volumes et hypothèses explicites.
- Distinguer ce qui est réel, simulé, prévu et non vérifié. Ne pas présenter
  une réponse préparée comme le résultat d'un service réellement appelé.
- Relier les affirmations produit à une documentation Microsoft Learn publique.
  Vérifier les capacités, licences, régions et prérequis avant de les affirmer ;
  signaler explicitement ce qui n'a pas pu être vérifié.
- Ne pas annoncer de ROI mesuré à partir de données synthétiques : indiquer
  les hypothèses, la formule et le caractère illustratif des gains.
- Avant une création de ressource payante, un changement de droits, une
  publication externe ou une suppression, expliquer le périmètre et les effets
  puis demander une confirmation explicite. Ne pas déployer par défaut.
- Préserver le travail existant. Ne pas committer ou pousser sans demande.
- Conserver la langue des documents existants ; les exemples du kit RCG sont
  en français. Documenter les prérequis, le lancement et les limites des ajouts.
