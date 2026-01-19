# Recipe

Interactive French CLI for generating recipes, multi-day meal plans, and budget-aware shopping lists. Built on LangChain + OpenAI, with nutrition targets, ingredient diversity, and optional real price lookups.

## Prerequisites

- Python 3.10+
- An OpenAI API key

## Installation

```bash
sudo apt update
sudo apt install -y python3-full python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file at the project root:

```env
OPENAI_API_KEY=...
INTERMARCHE_API_KEY=... # optional, only needed for real prices
```

## Usage

Run the main script and choose a mode:

```bash
python3 -m agentia.main
```

Modes:
- Recipe: one-off structured recipe.
- Planner: multi-day meal plan with full recipes for each meal.
- Shopping list: sports goal + budget + macros, seasonal ingredients, and optional pricing.

## Structure

- `agentia/main.py`: CLI entry point and mode selection.
- `agentia/agent.py`: OpenAI model and prompt wiring.
- `agentia/prompts.py`: recipe, planner, and shopping list prompts.
- `agentia/nutrition/`: macro calculator and sport profiles.
- `agentia/pricing/`: pricing providers (Intermarché API or estimation).
- `agentia/utils/`: preferences, parsing, history, ingredient selection.
- `agentia/data/knowledge/`: food groups, seasons, and category map.
- `agentia/data/state/preferences.json`: saved dislikes/allergies/categories.
- `agentia/data/state/history.json`: last shopping lists for variety.

## Notes

- The model used is `gpt-4o-mini` with a temperature of 0.6 (defined in `agentia/agent.py`).
- Intermarché pricing requires `INTERMARCHE_API_KEY` and makes API calls.
