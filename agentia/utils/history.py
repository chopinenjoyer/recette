from agentia.utils.io import read_json, write_json

HISTORY_PATH = ("data", "state", "history.json")


def get_used_ingredients(limit=2):
    history = read_json(*HISTORY_PATH, default={"shopping_lists": []})
    used = []
    for entry in history["shopping_lists"][-limit:]:
        used.extend(entry.get("ingredients", []))
    return list(set(used))


def save_shopping_list(ingredients):
    history = read_json(*HISTORY_PATH, default={"shopping_lists": []})
    history["shopping_lists"].append({
        "ingredients": ingredients
    })
    write_json(*HISTORY_PATH, data=history)

