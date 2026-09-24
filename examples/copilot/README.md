# Kit Copilot pour le hackathon RCG

Des **exemples à copier et à adapter**, pas une architecture imposée.
Objectif : passer d'une maquette et d'un HLD à une démonstration Azure
rejouable pour Tech for Retail.

Ces agents aident les participants à concevoir et construire leur application.
Ce ne sont pas les agents métier exécutés dans la démonstration.

## Choisir son point d'entrée

| Besoin | Exemple | Demande à Copilot |
|---|---|---|
| Challenger le HLD pendant la première heure | [Relecteur d'architecture](agents/azure-architecture-reviewer.agent.md) | « Relis notre HLD joint. Identifie les blocages et le plus petit parcours réalisable aujourd'hui. » |
| Construire après validation | [Constructeur de démo](agents/demo-builder.agent.md) | « Implémente le premier parcours validé, du stock à la recommandation, sans déployer. » |
| Préparer la restitution | [Coach de démonstration](agents/demo-coach.agent.md) | « Prépare une présentation de cinq minutes et indique ce qui reste simulé. » |
| Vérifier les accès et ressources | [Vérifier les prérequis](skills/demo-preflight/SKILL.md) | « Utilise demo-preflight pour vérifier les prérequis de notre HLD, sans modifier l'environnement. » |
| Préparer des données cohérentes | [Créer les données](skills/synthetic-demo-data/SKILL.md) | « Utilise synthetic-demo-data pour créer des stocks et ventes fictifs montrant une rupture imminente. » |
| Passer du mock à une connexion réelle | [Connecter une intégration](skills/connect-demo-integration/SKILL.md) | « Utilise connect-demo-integration pour remplacer notre stock simulé par la source validée dans le HLD. » |
| Répéter et recommencer la démo | [Rendre la démo rejouable](skills/rehearse-demo/SKILL.md) | « Utilise rehearse-demo pour préparer le parcours, les contrôles et la remise à zéro. » |

Un agent définit un **rôle** ; un skill décrit une **procédure** chargeable lorsque
la demande correspond ; les instructions donnent les **règles de contexte**.
Il n'est pas nécessaire de tout installer. Un skill ne nécessite pas un agent
personnalisé, et installer un agent ne lance pas automatiquement une équipe d'agents.

## Installer uniquement les exemples utiles

Les exemples sous `examples\copilot\` ne sont pas automatiquement découverts comme
personnalisations Copilot. Dans le dépôt de votre démo :

| Source dans ce kit | Destination dans votre dépôt |
|---|---|
| `agents\<nom>.agent.md` | `.github\agents\<nom>.agent.md` |
| `skills\<nom>\` (dossier entier) | `.github\skills\<nom>\` |
| `instructions\use-case.instructions.md` | `.github\instructions\use-case.instructions.md` |
| `instructions\azure-deployment.instructions.md` | `.github\instructions\azure-deployment.instructions.md` |

1. Lire les fichiers choisis avant de les copier. Ne pas écraser une personnalisation
   existante : intégrer les éléments utiles.
2. Remplacer les champs `<< ... >>` des instructions par les décisions du groupe.
   Les agents et skills sont génériques : leur fournir votre scénario et votre HLD.
3. Adapter `applyTo` aux chemins réels du projet. Le modèle de use case vise
   `demos/mon-use-case/**` : ce dossier est illustratif et n'existe pas dans ce kit.
   Les glob patterns utilisent `/`, même sous Windows.
4. Conserver des règles communes courtes dans `.github\copilot-instructions.md`.
   Celui de ce dépôt est un exemple actif, à adapter plutôt qu'à copier aveuglément.
5. Dans votre client Copilot, vérifier que les agents et skills copiés sont
   découverts. Sélectionner l'agent souhaité ou demander le skill par son nom.
   Vérifier le contexte des instructions lorsque vous travaillez sur un fichier ciblé.

La disponibilité et le chargement des personnalisations dépendent du client
Copilot et de sa version. Si une personnalisation n'est pas reconnue, fournir
explicitement son fichier dans la conversation ; ne pas supposer qu'elle est active.
Les instructions par chemin s'appliquent aux fichiers correspondants, pas
nécessairement à une discussion sans fichier : joindre alors le contexte du use case.

Les agents relecteur et coach demandent uniquement des outils de lecture/recherche.
Le constructeur demande aussi l'édition et l'exécution. Vérifier les outils
effectivement exposés par votre client ; une consigne n'est pas une frontière
de sécurité et ne remplace pas les permissions de l'environnement.
Aucun exemple n'installe un serveur MCP, n'accorde de droits Azure ou ne provisionne
de ressources. Aucun modèle d'IA spécifique n'est imposé.

## Personnaliser le contexte du groupe

Commencer par [les instructions de use case](instructions/use-case.instructions.md) :
persona employé et persona client, résultat métier, parcours minimum, HLD,
services retenus, intégrations réelles ou simulées et critères de réussite.
Ajouter [les instructions Azure](instructions/azure-deployment.instructions.md)
uniquement pour les fichiers de déploiement concernés.

La cible de réutilisation de 70 à 80 % est une ambition, pas une obligation
qui justifierait une architecture plus complexe. Réutiliser les données, contrats
et composants utiles tout en gardant des parcours distincts.

Pour Fabric, consulter aussi l'[accélérateur de données synthétiques](../../accelerators/fabric-data-agent-synthetic-data/README.md).
Il reste optionnel ; ses prérequis doivent être vérifiés pour votre environnement.

## Parcours suggéré pendant la session

1. **Validation** : présenter la maquette et le HLD, utiliser le relecteur et le
   skill de prérequis, puis faire valider le périmètre par le groupe.
2. **Construction** : réaliser une tranche de bout en bout avec le constructeur ;
   générer les données ou connecter un service seulement si nécessaire.
3. **Restitution** : vérifier les résultats, répéter deux fois et préparer une
   présentation courte avec le coach. Montrer clairement les simulations.

## Références de format

- [Configuration des agents personnalisés](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Création de skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [Instructions de dépôt et par chemin](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)

Ces liens documentent les formats Copilot, pas la faisabilité technique de votre HLD.
