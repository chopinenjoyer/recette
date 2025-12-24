from agentia.tools import read_ingredients
from agentia.agent import build_chain
from agentia.prompts import (
    SYSTEM_PROMPT,
    MEAL_PLANNER_WITH_RECIPES_PROMPT,
    SHOPPING_LIST_PROMPT
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
        print("Choix invalide. Réessaie.")
        return ask_mode()

def ask_days() -> int:
    while True:
        try:
            days = int(input("Combien de jours veux-tu prévoir ? "))
            if days > 0:
                return days
        except ValueError:
            pass
        print("Entre un nombre valide.")

def ask_duration() -> str:
    return input("Durée (ex : 1 semaine, 2 semaines, 1 mois) : ")

def ask_budget() -> str:
    return input("Budget maximum (€) : ")

def ask_people() -> int:
    while True:
        try:
            people = int(input("Nombre de personnes : "))
            if people > 0:
                return people
        except ValueError:
            pass
        print("Entre un nombre valide (ex : 1, 2, 4).")

def ask_goal() -> str:
    print("Objectif sportif :")
    print("1 - Prise de masse")
    print("2 - Maintien")
    print("3 - Sèche")
    choice = input("> ").strip()

    if choice == "1":
        return "prise de masse"
    elif choice == "2":
        return "maintien"
    elif choice == "3":
        return "sèche"
    else:
        print("Choix invalide.")
        return ask_goal()

def ask_store() -> str:
    print("Choisis une enseigne :")
    print("1 - Carrefour (prix moyens)")
    print("2 - Auchan (souvent moins cher)")
    print("3 - Monoprix (plus cher, urbain)")
    choice = input("> ").strip()

    if choice == "1":
        return "Carrefour"
    elif choice == "2":
        return "Auchan"
    elif choice == "3":
        return "Monoprix"
    else:
        print("Choix invalide.")
        return ask_store()

def main():
    ingredients = read_ingredients()
    mode = ask_mode()

    if mode == "recipe":
        chain = build_chain(SYSTEM_PROMPT)
        user_input = f"""
Crée une recette avec les ingrédients suivants :
{ingredients}
"""
    elif mode == "shopping":
        duration = ask_duration()
        budget = ask_budget()
        people = ask_people()
        goal = ask_goal()
        store = ask_store()

        chain = build_chain(SHOPPING_LIST_PROMPT)
        user_input = f"""
Crée une liste de courses avec les paramètres suivants :

Objectif sportif : {goal}
Nombre de personnes : {people}
Durée : {duration}
Budget maximum global : {budget} €
Enseigne cible : {store}

IMPORTANT :
- Les prix doivent être des ESTIMATIONS réalistes
- Basées sur les prix moyens observés chez {store} en France
- Indique clairement que les prix sont indicatifs
"""


    else:
        days = ask_days()
        chain = build_chain(MEAL_PLANNER_WITH_RECIPES_PROMPT)
        user_input = f"""
Voici les ingrédients disponibles :
{ingredients}

Crée un planning de repas pour {days} jours,
avec un déjeuner et un dîner par jour,
et fournis les recettes complètes.
"""

    response = chain.invoke({"input": user_input})
    print("\n===== RÉSULTAT =====\n")
    print(response.content)

if __name__ == "__main__":
    main()
