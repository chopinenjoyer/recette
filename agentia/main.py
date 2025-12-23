from agentia.agent import chain

ingredients = "oeufs, tomates, fromage, oignons, huile d'olive"

response = chain.invoke(
    {"input": f"Crée une recette avec les ingrédients suivants : {ingredients}"}
)

print(response.content)
