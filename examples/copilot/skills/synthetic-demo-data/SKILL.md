---
name: synthetic-demo-data
description: Produit des données synthétiques reproductibles pour une démonstration retail, luxe ou supply chain. À utiliser pour créer clients fictifs, produits, stocks et ventes contenant un signal métier vérifiable.
---

# Créer un jeu de données de démonstration

## Entrées

Obtenir le scénario, les questions de démo, la période, les volumes, les unités
et la cible (fichiers locaux, base ou Lakehouse). Ne pas supposer que Fabric
est obligatoire. Chercher un générateur ou un accélérateur existant à réutiliser.

## Procédure

1. Écrire les questions métier et les résultats attendus avant de générer.
   Pour chaque signal, définir une mesure, une période de référence et un
   seuil d'acceptation explicite à faire valider.
2. Définir le grain des tables, les identifiants et les relations. Conserver
   des clés stables entre les composants communs de la démo.
3. Générer uniquement des entreprises et personnes fictives. Utiliser
   `example.com` pour les adresses illustratives et neutraliser les envois.
   Ne pas copier ni anonymiser des données client réelles comme point de départ.
4. Paramétrer graine aléatoire, dates fixes, devise, volumes et signal. Éviter
   les dépendances cachées à la date du jour. Documenter les versions nécessaires.
5. Produire d'abord un petit jeu local. Vérifier clés uniques, relations,
   intervalles de dates et règles métier de quantité, prix et marge.
6. Calculer les agrégats qui prouvent le signal, puis comparer chaque valeur
   au seuil convenu. Échouer explicitement si les critères ne sont pas atteints ;
   ne pas remplacer les mesures par les chiffres attendus.
7. Préparer l'export adapté. Avant toute écriture distante ou remplacement
   de tables, confirmer la destination et l'effet avec le participant.
   Privilégier un espace dédié ; ne pas contourner silencieusement un échec d'écriture.

## Livrables et acceptation

- Générateur ou notebook paramétré, petit jeu produit et dictionnaire des données.
- Questions de démo associées aux requêtes, résultats calculés et seuils.
- Commande de régénération et contrôles exécutables.
- Vérification que deux générations avec les mêmes paramètres produisent les
  mêmes données logiques, indépendamment de l'ordre des lignes.

Si l'exécution n'est pas possible, livrer le générateur et les contrôles en les
marquant « non exécutés ». Les gains métier calculés sont illustratifs, jamais
des résultats client mesurés.
