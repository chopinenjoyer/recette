import random


def diversify_ingredients(all_ingredients: list, used_ingredients: list, ratio: float = 0.6) -> list:
    used = set(used_ingredients)
    fresh = [i for i in all_ingredients if i not in used]

    if not fresh:
        return all_ingredients

    keep_count = max(1, int(len(all_ingredients) * ratio))
    random.shuffle(fresh)

    return fresh[:keep_count]
