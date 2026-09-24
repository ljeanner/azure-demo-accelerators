---
applyTo: "demos/mon-use-case/**"
---

# Contexte du use case — à adapter avant activation

Remplacer les champs et adapter `applyTo` au chemin réel du projet.
Un champ non renseigné est une décision manquante, pas une autorisation
pour inventer un besoin. Joindre ce fichier lors d'une discussion sans fichier ciblé.

## Scénario

- Entreprise fictive et secteur : << nom fictif, retail / luxe / biens de consommation >>
- Problème métier : << problème concret >>
- Persona employé : << rôle et décision à prendre >>
- Persona client : << besoin et résultat visible >>
- Parcours minimum : << déclencheur -> analyse -> action -> résultat >>
- Durée de restitution et temps de construction : << durées >>
- Maquette et HLD de référence : << chemins ou liens publics >>
- État de validation du HLD : << validé par le groupe / décisions restantes >>

## Choix techniques validés

| Composant | Service ou technologie retenue | Réel / simulé / prévu | Justification |
|---|---|---|---|
| Interface | << choix >> | << mode >> | << besoin >> |
| Données | << choix >> | << mode >> | << besoin >> |
| Traitement / IA | << choix ou non applicable >> | << mode >> | << besoin >> |
| Action / notification | << choix ou non applicable >> | << mode >> | << besoin >> |

- Composants communs à réutiliser : << chemins et contrats >>
- Fonctionnalités prioritaires : << périmètre de la session >>
- Hors périmètre : << éléments explicitement reportés >>
- Étapes nécessitant une approbation humaine : << actions ou non applicable >>

Ne pas ajouter de service pour remplir une liste technologique. Respecter les
choix validés ; faire confirmer toute modification structurante.
Afficher les simulations. Ne pas basculer silencieusement du réel vers le mock.

## Valeur et acceptation

- Indicateur métier : << nom, unité et formule >>
- Hypothèses illustratives : << valeur de référence et hypothèses du gain >>
- Critères observables : << actions et résultats précis attendus >>
- Lancement et contrôles : << commandes existantes ou à définir >>
- État initial et remise à zéro : << données et procédure >>

Utiliser uniquement des données synthétiques. Ne pas présenter les hypothèses
de ROI comme des gains client prouvés. Si un critère n'est pas vérifiable,
le signaler explicitement plutôt que déclarer la démo terminée.
