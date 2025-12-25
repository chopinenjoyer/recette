from datetime import datetime
from agentia.utils.io import read_json, write_json

HISTORY_PATH = ("data", "state", "history.json")


def load_history():
    return read_json(*HISTORY_PATH, default={"shopping_lists": []})


def save_shopping_list(ingredients):
    history = load_history()

    history["shopping_lists"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "ingredients": sorted(set(ingredients))
    })

    write_json(history, *HISTORY_PATH)


def get_used_ingredients():
    history = load_history()
    used = set()

    for entry in history.get("shopping_lists", []):
        used.update(entry.get("ingredients", []))

    return list(used)
