# Recipe

Recipe generator built on a LangChain agent. The script builds a chef prompt, sends the ingredient list to the OpenAI model, then prints a structured recipe that uses only those ingredients.

## Prerequisites

- Python 3.10+
- An OpenAI API key

## Installation

```bash
sudo apt update
sudo apt install -y python3-full python3-venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file at the project root:

```env
OPENAI_API_KEY=...
```

## Usage

Run the main script:

```bash
python agentia/main.py
```

By default, the ingredient list is loaded from `data/ingredients.txt`. Edit that file (one ingredient per line) to generate a new recipe.

## Structure

- `agentia/main.py`: entry point, sends ingredients to the agent.
- `agentia/agent.py`: model and prompt configuration.
- `agentia/prompts.py`: “chef” system prompt.
- `agentia/tools.py`: helper to load ingredients from file.
- `data/ingredients.txt`: list of ingredients, one per line.

## Notes

The model used is `gpt-4o-mini` with a temperature of 0.6 (defined in `agentia/agent.py`).
