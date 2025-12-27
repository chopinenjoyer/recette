import random
from agentia.data.knowledge.food_groups import FOOD_GROUPS
from agentia.data.knowledge.category_map import CATEGORY_MAP
from agentia.utils.preferences import load_preferences
from agentia.utils.history import get_used_ingredients


def select_ingredients(days: int, persons: int, objective: str):
    prefs = load_preferences()

    excluded_ingredients = set(
        prefs["excluded_ingredients"] + prefs["allergies"]
    )

    excluded_categories = set(prefs["excluded_categories"])

    excluded_from_categories = set()
    for cat in excluded_categories:
        excluded_from_categories.update(CATEGORY_MAP.get(cat, []))

    used = set(get_used_ingredients(limit=2))

    blocked = excluded_ingredients | excluded_from_categories | used

    def pick(category: str, n: int):
        pool = [
            i for i in FOOD_GROUPS[category]
            if i not in blocked
        ]

        if len(pool) < n:
            pool = [
                i for i in FOOD_GROUPS[category]
                if i not in excluded_ingredients
                and i not in excluded_from_categories
            ]

        return random.sample(pool, min(n, len(pool)))

    return {
        "proteines": pick("proteines", 3 + persons),
        "feculents": pick("feculents", 2),
        "legumes": pick("legumes", 4),
        "fruits": [] if "fruits" in excluded_categories else pick("fruits", 2),
        "lipides": pick("matieres_grasses", 2),
    }
