# Contribuer un accélérateur

## Ce qui fait un bon accélérateur

- **Rejouable par quelqu'un d'autre** sans te poser de question.
- **Paramétrable** : le scénario métier est un bloc à remplir, pas du code en dur.
- **Ancré** : chaque affirmation produit est liée à une page Microsoft Learn.
- **Honnête sur le coût** : prérequis, capacité nécessaire, temps de mise en place.

## Procédure

```bash
cp -r _template accelerators/mon-accelerateur
```

Puis remplis `accelerators/mon-accelerateur/README.md` :

| Section | Contenu attendu |
|---|---|
| Objectif | En une phrase, ce que l'accélérateur permet de démontrer |
| Prérequis | Licences, capacité (ex. Fabric F2+), rôles, accès |
| Le prompt | Bloc ```` ``` ```` copiable, avec des placeholders `<< ... >>` |
| Mise en place | Étapes numérotées dans le portail / CLI |
| Script de démo | Les questions posées en live et les réponses attendues |
| Règles d'or | Les pièges qui font rater la démo |
| Sources | Liens Microsoft Learn (titre + URL) |

## Règles non négociables

- ❌ Aucune donnée client, aucun nom de client réel, aucune PII.
- ❌ Aucun secret, clé, connection string, token — même expiré.
- ❌ Aucun contenu sous NDA ou non annoncé publiquement.
- ✅ Noms d'entreprises, concurrents et personnes **inventés**.
- ✅ Seeds fixés pour que la donnée synthétique soit reproductible.

## Review

Une PR = un accélérateur. Un relecteur vérifie qu'il a pu le rejouer de zéro.
