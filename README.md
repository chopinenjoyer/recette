# Recette

Générateur de recettes basé sur un agent LangChain. Le script assemble un prompt de chef cuisinier, envoie la liste d’ingrédients au modèle OpenAI, puis affiche une recette structurée qui n’utilise que ces ingrédients.

## Prérequis

- Python 3.10+
- Une clé API OpenAI

## Installation

```bash
pip install langchain-openai langchain-core python-dotenv
```

## Configuration

Créer un fichier `.env` à la racine du projet :

```env
OPENAI_API_KEY=...
```

## Utilisation

Exécuter le script principal :

```bash
python agentia/main.py
```

Par défaut, la liste d’ingrédients est définie dans `agentia/main.py`. Modifiez la variable `ingredients` pour générer une nouvelle recette.

## Structure

- `agentia/main.py` : point d’entrée, envoie les ingrédients à l’agent.
- `agentia/agent.py` : configuration du modèle et du prompt.
- `agentia/prompts.py` : prompt système “chef cuisinier”.

## Notes

Le modèle utilisé est `gpt-4o-mini` avec une température de 0.6 (définis dans `agentia/agent.py`).
