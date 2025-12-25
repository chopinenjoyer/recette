import random
from agentia.data.knowledge.food_groups import FOOD_GROUPS
from agentia.utils.history import get_used_ingredients


def select_ingredients(days: int, persons: int, objective: str):
    used = set(get_used_ingredients(limit=2))

    def pick(category, n):
        pool = [i for i in FOOD_GROUPS[category] if i not in used]
        if len(pool) < n:
            pool = FOOD_GROUPS[category]
        return random.sample(pool, n)

    return {
        "proteines": pick("proteines", 3 + persons),
        "feculents": pick("feculents", 2),
        "legumes": pick("legumes", 4),
        "fruits": pick("fruits", 2),
        "lipides": pick("matieres_grasses", 2),
    }
