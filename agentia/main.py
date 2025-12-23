from agentia.tools import read_ingredients
from agentia.agent import build_chain
from agentia.prompts import (
    SYSTEM_PROMPT,
    MEAL_PLANNER_WITH_RECIPES_PROMPT
)

def ask_mode() -> str:
    print("\nChoisis un mode :")
    print("1 - Créer une recette")
    print("2 - Prévoir des repas sur plusieurs jours")
    choice = input("> ").strip()

    if choice == "1":
        return "recipe"
    elif choice == "2":
        return "planner"
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

def main():
    ingredients = read_ingredients()
    mode = ask_mode()

    if mode == "recipe":
        chain = build_chain(SYSTEM_PROMPT)
        user_input = f"""
Crée une recette avec les ingrédients suivants :
{ingredients}
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
