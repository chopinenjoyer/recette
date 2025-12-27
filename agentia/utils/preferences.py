from agentia.utils.io import read_json, write_json

PREFERENCES_PATH = ("data", "state", "preferences.json")

DEFAULT_PREFERENCES = {
    "excluded_ingredients": [],
    "allergies": [],
    "excluded_categories": [],
}

def load_preferences():
    return read_json(*PREFERENCES_PATH, default=DEFAULT_PREFERENCES.copy())


def save_preferences(prefs):
    write_json(*PREFERENCES_PATH, data=prefs)


def add_excluded_ingredient(ingredient: str):
    prefs = load_preferences()
    ingredient = ingredient.lower()

    if ingredient not in prefs["excluded_ingredients"]:
        prefs["excluded_ingredients"].append(ingredient)

    save_preferences(prefs)


def add_allergy(ingredient: str):
    prefs = load_preferences()
    ingredient = ingredient.lower()

    if ingredient not in prefs["allergies"]:
        prefs["allergies"].append(ingredient)

    save_preferences(prefs)


def add_excluded_category(category: str):
    prefs = load_preferences()
    category = category.lower()

    if category not in prefs["excluded_categories"]:
        prefs["excluded_categories"].append(category)

    save_preferences(prefs)


def get_forbidden_ingredients():
    prefs = load_preferences()
    return (
        prefs["excluded_ingredients"]
        + prefs["allergies"]
    )


def get_excluded_categories():
    prefs = load_preferences()
    return prefs["excluded_categories"]

def confirm_category_exclusion(category: str) -> bool:
    print(
        f"\n⚠️ Attention : vous êtes sur le point d'exclure toute la catégorie '{category}'."
    )
    choice = input("Confirmer ? (o/n) > ").strip().lower()
    return choice == "o"