from agentia.agent import build_chain
from agentia.tools import read_ingredients
from agentia.pricing.selector import get_price_provider
from agentia.nutrition.calculator import calculate_macros
from agentia.data.knowledge.seasons import current_season
from agentia.utils.io import ask_int
from agentia.prompts import (
    SYSTEM_PROMPT,
    MEAL_PLANNER_WITH_RECIPES_PROMPT,
    SHOPPING_LIST_PROMPT,
)
from agentia.data.state.history import (
    save_shopping_list,
    get_used_ingredients
)


def ask_mode() -> str:
    print("\nChoisis un mode :")
    print("1 - Créer une recette")
    print("2 - Prévoir des repas sur plusieurs jours")
    print("3 - Générer une liste de courses (sportif + budget)")
    choice = input("> ").strip()

    if choice == "1":
        return "recipe"
    elif choice == "2":
        return "planner"
    elif choice == "3":
        return "shopping"
    else:
        print("Choix invalide.")
        return ask_mode()

def ask_duration() -> str:
    return input("Durée (ex : 1 semaine, 2 semaines, 1 mois) : ").strip()

def ask_budget() -> str:
    return input("Budget maximum (€) : ").strip()

def ask_people() -> int:
    while True:
        try:
            people = int(input("Nombre de personnes : "))
            if people > 0:
                return people
        except ValueError:
            pass
        print("Veuillez entrer un nombre valide.")

def ask_goal() -> str:
    print("Objectif sportif :")
    print("1 - Prise de masse")
    print("2 - Maintien")
    print("3 - Sèche")
    choice = input("> ").strip()

    if choice == "1":
        return "prise"
    elif choice == "2":
        return "maintien"
    elif choice == "3":
        return "seche"
    else:
        print("Choix invalide.")
        return ask_goal()

def ask_store() -> str:
    print("Choisis une enseigne :")
    print("1 - Intermarché (prix réels)")
    print("2 - Estimation IA")
    choice = input("> ").strip()

    if choice == "1":
        return "intermarché"
    elif choice == "2":
        return "estimation"
    else:
        print("Choix invalide.")
        return ask_store()

def main():
    mode = ask_mode()
    ingredients = read_ingredients()

    if mode == "recipe":
        chain = build_chain(SYSTEM_PROMPT)
        user_input = f"Ingrédients disponibles : {ingredients}"
        result = chain.invoke({"input": user_input})
        print("\n" + result.content)

    elif mode == "planner":
        duration = ask_duration()
        chain = build_chain(MEAL_PLANNER_WITH_RECIPES_PROMPT)
        user_input = f"""
Ingrédients disponibles : {ingredients}
Durée : {duration}
"""
        result = chain.invoke({"input": user_input})
        print("\n" + result.content)

    elif mode == "shopping":
        duration = ask_duration()
        budget = ask_budget()
        people = ask_int("Nombre de personnes : ")
        goal = ask_goal()
        store = ask_store()

        macros = calculate_macros(
            weight_kg=70,
            objective=goal,
            days=7 if "semaine" in duration else 30,
            persons=people
        )

        provider = get_price_provider(store)
        prices = provider.get_prices(ingredients)

        prices_text = "\n".join(
            f"- {p['ingredient']} : {p.get('price', 'N/A')} €"
            if "price" in p else f"- {p['ingredient']} : NON TROUVÉ"
            for p in prices
        )

        chain = build_chain(SHOPPING_LIST_PROMPT)
        used_ingredients = get_used_ingredients()

        user_input = f"""
Objectif sportif : {goal}
Calories par jour : {macros['calories_per_day']}
Protéines (g/jour) : {macros['protein_g_per_day']}
Glucides (g/jour) : {macros['carbs_g_per_day']}
Lipides (g/jour) : {macros['fats_g_per_day']}
Calories totales période : {macros['total_calories']}
Nombre de personnes : {people}
Durée : {duration}
Budget maximum global : {budget} €

Voici les prix observés ({store}) :

{prices_text}

INGRÉDIENTS DÉJÀ UTILISÉS DANS LES LISTES PRÉCÉDENTES
(À ÉVITER AUTANT QUE POSSIBLE) :
{used_ingredients}

CONTRAINTES OBLIGATOIRES :
- Évite au maximum les ingrédients déjà utilisés
- Introduis de nouvelles sources de protéines
- Varie féculents et légumes
- Aucun ingrédient ne doit apparaître plus de 2 fois
- Propose plusieurs styles culinaires

À partir de ces données :
- optimise la liste de courses
- respecte le budget
"""

        result = chain.invoke({"input": user_input})
        print("\n" + result.content)
        save_shopping_list(ingredients)

if __name__ == "__main__":
    main()
