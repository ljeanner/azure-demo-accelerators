# Données synthétiques → Fabric Lakehouse → Fabric Data Agent

**Objectif :** produire en quelques heures un jeu de données synthétique crédible et un **Fabric Data Agent**
capable de répondre en langage naturel à des questions métier, avec un scénario qui porte la narration commerciale.

**Durée :** 2-3 h · **Prérequis :** capacité Fabric **F2 ou supérieure**, droits de création dans un workspace Fabric.

> Méthode utilisée pour la démo **Zava Retail** (distributeur d'articles de sport fictif).
> Copiez le prompt ci-dessous dans Copilot / Claude / un notebook Fabric,
> remplissez les blocs `<< ... >>` et laissez l'agent produire le notebook.

---

## 1. Le prompt (à copier-coller)

```
Tu es data engineer. Génère-moi un notebook PySpark, exécutable dans un notebook Microsoft Fabric
avec un Lakehouse attaché, qui crée un jeu de données SYNTHÉTIQUE mais RÉALISTE et COHÉRENT,
puis l'écrit en tables Delta dans le Lakehouse. Ces données serviront à démontrer un
Fabric Data Agent (questions en langage naturel → SQL) devant des décideurs.

### CONTEXTE MÉTIER (à remplir)
- Entreprise fictive       : << nom, secteur, pays/HQ, année de création >>
- Taille / échelle affichée: << CA, nb de magasins/sites, nb de clients, nb de pays >>
- Marques / lignes produit : << ... >>
- Domaines à couvrir       : << ventes, stock, achats, production, marges, prévisions, concurrence, RH... >>
- Période des données      : << date_debut >> → << date_fin >>
- Devise / langue          : << EUR, libellés FR ou EN >>

### SCÉNARIO DE DÉMO (le plus important)
Les données doivent contenir un SIGNAL EXPLOITABLE que l'agent pourra détecter et expliquer :
- Événement déclencheur : << ex. un concurrent lance -30% sur une catégorie pendant 3 semaines >>
- Fenêtre de l'événement : << date_debut_event >> → << date_fin_event >>
- Effet attendu dans les données : << baisse de volume/prix moyen sur la catégorie X,
  tension de stock sur les références Y, marge sous le seuil Z >>
- Questions auxquelles la démo doit savoir répondre (5 à 10) :
  1. << ex. Quelle est l'évolution des ventes de la catégorie X sur les 8 dernières semaines ? >>
  2. << ex. Quels produits sont sous le seuil de marge de 35% ? >>
  3. << ... >>

### EXIGENCES SUR LES DONNÉES
1. Modèle en étoile : tables `dim_*` (référentiels) et `fact_*` (transactions), clés étrangères valides,
   aucune ligne orpheline.
2. `SEED = 42` et seeds fixés (random + numpy) → données reproductibles par tous les collègues.
3. Réalisme obligatoire :
   - saisonnalité mensuelle par catégorie, effet week-end, tendance annuelle ;
   - prix cohérents avec les coûts (marge plausible, historique de prix avec quelques changements) ;
   - promotions calendaires, canaux multiples (magasin / e-commerce) ;
   - un peu de bruit et quelques valeurs manquantes, mais JAMAIS d'incohérence (pas de quantité négative,
     pas de date hors période, pas de remise > 100%).
4. Le scénario de démo doit être VISIBLE en agrégé : si on groupe par semaine/catégorie, l'écart doit sauter aux yeux.
5. Volumétrie : viser quelques centaines de milliers à quelques millions de lignes de faits
   (paramètres en haut du notebook : NUB_SITES, NUM_PRODUCTS, NUM_CUSTOMERS, AVG_DAILY_TRANSACTIONS...).
6. AUCUNE donnée réelle, aucun nom de client/fournisseur/concurrent existant, aucune PII réelle.

### STRUCTURE DU NOTEBOOK ATTENDUE
- Cellule 0 : bloc `# Configuration` avec toutes les constantes (seed, dates, volumétrie, fenêtre du scénario).
- Section 1 : dimensions (produits, sites, clients, fournisseurs, concurrents).
- Section 2 : prix & promotions (historique de prix, calendrier promo).
- Section 3..N : faits (ventes, stock, commandes, production, marges, prévisions, activité concurrente).
- Section « Write to Lakehouse » : dictionnaire `TABLES = {"dim_...": df, "fact_...": df}` puis, pour chaque table,
  `df.write.format("delta").mode("overwrite").saveAsTable(table_name)` avec fallback sur `.save(f"Tables/{name}")`,
  et affichage du nombre de lignes écrites par table.
- Section « Validation » : compte de lignes, contrôle d'intégrité référentielle, et 3 requêtes d'agrégation
  qui PROUVENT que le signal du scénario est présent.

### LIVRABLES SUPPLÉMENTAIRES (en plus du notebook)
A. Un **dictionnaire de données** en markdown : pour chaque table, sa granularité, ses colonnes,
   leur type et leur sens métier.
B. Les **instructions du Data Agent** (< 15 000 caractères) : rôle, description de chaque table,
   quand utiliser quelle table, règles métier (seuils de marge, définition du CA net, fiscal vs calendaire),
   ton de réponse et obligation de citer les chiffres.
C. **10 example queries** au format paire « question en langage naturel → requête SQL validée »,
   couvrant les questions de la démo.
D. Un **script de démo** : 5 questions posées à l'agent, dans l'ordre, avec la réponse attendue.
```

---

## 2. Après la génération : mise en place dans Fabric

1. **Workspace + Lakehouse** — capacité F2 minimum ; créer le Lakehouse (`<Nom>LH`).
2. **Notebook** — importer le notebook généré, l'attacher au Lakehouse, `Run all`.
   Vérifier les tables Delta sous `Tables/`.
3. **Data agent** — *New item → Data agent*, le nommer, puis ajouter le Lakehouse depuis le catalogue OneLake
   (jusqu'à 5 sources : lakehouse, warehouse, modèle sémantique Power BI, base KQL, ontologie, Microsoft Graph).
   Cocher uniquement les tables utiles à la démo (moins de tables = SQL plus juste).
4. **Instructions** — coller le livrable **B** dans *Data agent instructions*.
5. **Example queries** — coller le livrable **C** dans *Example queries* (non supporté pour les modèles
   sémantiques Power BI ; c'est le levier n°1 de précision pour lakehouse/warehouse/KQL).
6. **Tester puis Publier** — rejouer le script **D**, corriger instructions/exemples, puis *Publish*.
   Le data agent publié est consommable depuis Azure AI Foundry / Copilot Studio / M365 Copilot,
   ou via le SDK `fabric-data-agent-sdk`.
7. **Versionner** — activer l'intégration Git du workspace : les dossiers `draft/` et `published/`
   contiennent la config du data agent (dossiers `lakehouse-tables-*`), donc les collègues peuvent la rejouer.

---

## 3. Règles d'or (ce qui fait rater les démos)

- **Le scénario avant les données.** Écrire d'abord les 5 questions de la démo, générer ensuite.
- **Le signal doit être macro-visible**, sinon l'agent ne le « voit » pas.
- **Seed fixé** : tout le monde doit avoir exactement les mêmes chiffres.
- **Peu de tables exposées à l'agent** et des noms explicites (`fact_sales`, pas `t1`).
- **Les example queries valent mieux que de longues instructions** pour la qualité du SQL.
- **Zéro donnée réelle / zéro PII**, noms de concurrents inventés.

Sources : [Create a Fabric data agent](https://learn.microsoft.com/fabric/data-science/how-to-create-data-agent) ·
[Data agent end-to-end tutorial](https://learn.microsoft.com/fabric/data-science/data-agent-end-to-end-tutorial) ·
[Source control & ALM](https://learn.microsoft.com/fabric/data-science/data-agent-source-control)
