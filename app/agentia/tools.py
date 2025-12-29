from pathlib import Path

def read_ingredients() -> str:
    """
    Lit le fichier data/ingredients.txt et retourne
    une chaîne prête à être utilisée par l'agent.
    """
    root_dir = Path(__file__).resolve().parents[1]
    ingredients_file = root_dir / "data" / "ingredients.txt"

    with open(ingredients_file, "r", encoding="utf-8") as f:
        ingredients = [line.strip() for line in f if line.strip()]

    return ", ".join(ingredients)