from agentia.tools import read_ingredients
from agentia.agent import build_chain
from agentia.prompts import SYSTEM_PROMPT, MEAL_PLANNER_WITH_RECIPES_PROMPT

mode = "planner"
days = 7


ingredients = read_ingredients()

if mode == "recipe":
    chain = build_chain(SYSTEM_PROMPT)
    user_input = f"""
Crée une recette avec les ingrédients suivants :
{ingredients}
"""

elif mode == "planner":
    chain = build_chain(MEAL_PLANNER_WITH_RECIPES_PROMPT)
    user_input = f"""
Voici les ingrédients disponibles :
{ingredients}

Crée un planning de repas pour {days} jours,
avec un déjeuner et un dîner par jour,
et fournis les recettes complètes.
"""

else:
    raise ValueError("Mode invalide. Choisis 'recipe' ou 'planner'.")

response = chain.invoke({"input": user_input})

print(response.content)
