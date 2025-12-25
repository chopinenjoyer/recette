from pathlib import Path

def read_ingredients() -> list:
    ingredients_file = Path(__file__).parent / "data" / "raw" / "ingredients.txt"

    if not ingredients_file.exists():
        return []

    with open(ingredients_file, "r", encoding="utf-8") as f:
        return [
            line.strip().lower()
            for line in f
            if line.strip()
        ]
