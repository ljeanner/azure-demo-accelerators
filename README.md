# Azure Demo Accelerators

Recettes réutilisables pour construire **rapidement** des démos Azure / Fabric / AI crédibles devant un client.
Chaque accélérateur = un dossier, un `README.md`, un prompt prêt à copier-coller, et un checklist de mise en place.

> Repo interne Microsoft. **Aucune donnée client, aucune PII, aucun secret.** Tout est synthétique.

---

## Accélérateurs disponibles

| Accélérateur | Ce que ça débloque | Temps estimé |
|---|---|---|
| [`fabric-data-agent-synthetic-data`](accelerators/fabric-data-agent-synthetic-data/) | Générer un jeu de données synthétique cohérent, l'écrire en tables Delta dans un Lakehouse Fabric, et le brancher sur un **Fabric Data Agent** (questions en langage naturel → SQL) | 2-3 h |

---

## Démarrage rapide (hackathon)

1. Choisis l'accélérateur qui correspond à ta démo.
2. Ouvre son `README.md` et copie le prompt dans ton assistant (Copilot, Claude, ChatGPT…).
3. Remplis les blocs `<< ... >>` avec **ton** scénario client.
4. Suis le checklist de mise en place à la fin du README.
5. Répète la démo 2 fois avant de la montrer. Une démo non répétée est une démo ratée.

### Les 3 règles qui font la différence

1. **Le scénario avant la donnée.** Écris d'abord les 5 questions que tu vas poser en live, génère la donnée ensuite.
2. **Le signal doit être visible en agrégé.** Si l'écart ne saute pas aux yeux sur un graphe hebdo, l'agent ne le « verra » pas non plus.
3. **Reproductibilité.** Seed fixé, paramètres en haut du notebook : tes collègues doivent obtenir exactement tes chiffres.

---

## Contribuer

Tu as monté une démo qui a marché ? Publie-la ici.

1. Copie [`_template/`](_template/) vers `accelerators/<nom-court-kebab-case>/`.
2. Remplis le README (contexte, prompt, checklist, sources Microsoft Learn).
3. Ajoute une ligne au tableau ci-dessus.
4. Ouvre une PR.

Voir [CONTRIBUTING.md](CONTRIBUTING.md).
