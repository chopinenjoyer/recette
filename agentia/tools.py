from pathlib import Path

def read_ingredients() -> list:
    base_dir = Path(__file__).resolve().parent
    ingredients_file = base_dir / "data" / "raw" / "ingredients.txt"

    with open(ingredients_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
