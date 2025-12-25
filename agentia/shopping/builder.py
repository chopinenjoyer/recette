from agentia.data.state.history import load_history

def penalize_used_ingredients(candidates, history):
    used = set()
    for entry in history.get("shopping_lists", []):
        used.update(entry["ingredients"])

    return [
        ing for ing in candidates
        if ing not in used
    ]
