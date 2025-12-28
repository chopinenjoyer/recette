from agentia.agent import build_chain
from agentia.pricing.selector import get_price_provider
from agentia.nutrition.calculator import calculate_macros
from agentia.prompts import (
    SYSTEM_PROMPT,
    MEAL_PLANNER_WITH_RECIPES_PROMPT,
    SHOPPING_LIST_PROMPT,
)
from agentia.utils.io import ask_int
from agentia.utils.history import save_shopping_list
from agentia.utils.ingredient_selector import select_ingredients
from agentia.utils.parser import (
    remove_json_block,
    extract_ingredients_from_response,
    extract_disliked_ingredients,
    extract_disliked_categories,
)
from agentia.utils.preferences import (
    load_preferences,
    add_excluded_ingredient,
    add_allergy,
    add_excluded_category,
)


def onboarding_preferences():
    prefs = load_preferences()
    if prefs["excluded_ingredients"] or prefs["allergies"] or prefs["excluded_categories"]:
        return

    print("\nPremière utilisation – personnalisation")

    disliked = input(
        "Ingrédients que vous n'aimez pas (séparés par des virgules, ou Entrée) : "
    ).strip()

    if disliked:
        for i in disliked.split(","):
            add_excluded_ingredient(i.strip().lower())

    allergies = input(
        "Allergies alimentaires (séparées par des virgules, ou Entrée) : "
    ).strip()

    if allergies:
        for i in allergies.split(","):
            add_allergy(i.strip().lower())

    categories = input(
        "Catégories à exclure (ex: fruits, poissons, fruits de mer) : "
    ).strip()

    if categories:
        for c in categories.split(","):
            add_excluded_category(c.strip().lower())


def ask_mode():
    print("\nChoisis un mode :")
    print("1 - Créer une recette")
    print("2 - Prévoir des repas sur plusieurs jours")
    print("3 - Générer une liste de courses (sportif + budget)")
    choice = input("> ").strip()

    if choice == "1":
        return "recipe"
    if choice == "2":
        return "planner"
    if choice == "3":
        return "shopping"
    return ask_mode()


def ask_duration():
    return input("Durée (ex : 1 semaine à 2 semaines) : ").strip()


def ask_budget():
    return input("Budget maximum (€) : ").strip()


def ask_goal():
    print("Objectif sportif :")
    print("1 - Prise de masse")
    print("2 - Maintien")
    print("3 - Sèche")
    choice = input("> ").strip()

    if choice == "1":
        return "prise"
    if choice == "2":
        return "maintien"
    if choice == "3":
        return "seche"
    return ask_goal()


def ask_store():
    print("Choisis une enseigne :")
    print("1 - Intermarché (prix réels)")
    print("2 - Estimation IA")
    choice = input("> ").strip()

    if choice == "1":
        return "intermarche"
    if choice == "2":
        return "estimation"
    return ask_store()


def main():
    mode = ask_mode()

    if mode == "recipe":
        chain = build_chain(SYSTEM_PROMPT)
        result = chain.invoke({"input": "Crée une recette équilibrée."})
        print(remove_json_block(result.content))
        return

    if mode == "planner":
        duration = ask_duration()
        chain = build_chain(MEAL_PLANNER_WITH_RECIPES_PROMPT)
        result = chain.invoke({"input": f"Planifie des repas pour {duration}."})
        print(remove_json_block(result.content))
        return

    if mode == "shopping":
        onboarding_preferences()

        duration = ask_duration()
        budget = ask_budget()
        people = ask_int("Nombre de personnes : ")
        goal = ask_goal()
        store = ask_store()

        days = 7 if "semaine" in duration else 30

        macros = calculate_macros(
            weight_kg=70,
            objective=goal,
            days=days,
            persons=people,
        )

        ingredient_pool = select_ingredients(
            days=days,
            persons=people,
            objective=goal,
        )

        provider = get_price_provider(store)
        prices = provider.get_prices(
            ingredient_pool["proteines"]
            + ingredient_pool["feculents"]
            + ingredient_pool["legumes"]
            + ingredient_pool["fruits"]
            + ingredient_pool["lipides"]
        )

        prices_text = "\n".join(
            f"- {p['ingredient']} : {p.get('price', 'N/A')} €"
            for p in prices
        )

        chain = build_chain(SHOPPING_LIST_PROMPT)
        result = chain.invoke(
            {
                "input": f"""
Objectif sportif : {goal}
Calories par jour : {macros['calories_per_day']}
Protéines (g/jour) : {macros['protein_g_per_day']}
Glucides (g/jour) : {macros['carbs_g_per_day']}
Lipides (g/jour) : {macros['fats_g_per_day']}
Nombre de personnes : {people}
Durée : {duration}
Budget maximum : {budget} €

Ingrédients autorisés :

Protéines : {ingredient_pool['proteines']}
Glucides : {ingredient_pool['feculents']}
Légumes : {ingredient_pool['legumes']}
Fruits : {ingredient_pool['fruits']}
Lipides : {ingredient_pool['lipides']}

Prix observés :
{prices_text}
"""
            }
        )

        print(remove_json_block(result.content))

        feedback = input(
            "\nSouhaitez-vous exclure un ingrédient ou une catégorie ?\n> "
        ).strip()

        if feedback:
            for ing in extract_disliked_ingredients(feedback):
                add_excluded_ingredient(ing)

            for cat in extract_disliked_categories(feedback):
                add_excluded_category(cat)

            print("\nPréférences mises à jour. Relancez pour une nouvelle liste.")

        extracted = extract_ingredients_from_response(result.content)
        if extracted:
            save_shopping_list(extracted)


if __name__ == "__main__":
    main()
