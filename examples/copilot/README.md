# Exemples Copilot pour le hackathon RCG

Choisissez les fichiers utiles à votre démo, copiez-les dans votre projet
et adaptez-les. Rien dans ce dossier n'est activé par défaut.

## Agents : choisir un rôle

- [Relecteur d'architecture](agents/azure-architecture-reviewer.agent.md) : challenger votre HLD.
- [Constructeur de démo](agents/demo-builder.agent.md) : implémenter votre scénario.
- [Coach de démo](agents/demo-coach.agent.md) : préparer votre présentation orale.

Copier les fichiers choisis dans `.github\agents\`, puis sélectionner l'agent dans Copilot.

## Skills : réaliser une tâche

- [Prérequis](skills/demo-preflight/SKILL.md) : repérer les blocages avant de commencer.
- [Données synthétiques](skills/synthetic-demo-data/SKILL.md) : créer les données de votre scénario.
- [Intégration](skills/connect-demo-integration/SKILL.md) : connecter un service à votre application.
- [Répétition](skills/rehearse-demo/SKILL.md) : vérifier que la démo peut être rejouée.
- [PowerPoint](skills/demo-ppt/SKILL.md) : préparer cinq slides de restitution.

Copier chaque dossier choisi dans `.github\skills\`, puis demander par exemple :
« Utilise demo-ppt pour préparer la restitution de notre démo. »
La création du fichier PPTX nécessite un outil compatible ; sinon le skill fournit le contenu des slides.

## Instructions : donner le contexte

- [Use case](instructions/use-case.instructions.md) : votre scénario et vos choix techniques.
- [Déploiement Azure](instructions/azure-deployment.instructions.md) : votre environnement et ses limites.

Copier dans `.github\instructions\`, remplir les champs `<< ... >>` et adapter
`applyTo` aux chemins de votre projet (les glob patterns utilisent `/`).
Les [règles communes](../../.github/copilot-instructions.md) sont déjà actives dans ce dépôt.

**Pour démarrer :** renseigner le use case, relire le HLD, puis construire.
Si votre client Copilot ne reconnaît pas un fichier, le joindre directement à la conversation.
