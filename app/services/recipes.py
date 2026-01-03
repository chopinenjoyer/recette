from typing import List
from app.agentia.agent import generate_recipe
from app.repositories.recipes_repo import RecipeRepository


class RecipeService:
    def __init__(self, repo: RecipeRepository, agent: generate_recipe):
        self.repo = repo
        self.agent = agent

    def create_recipe(self, ingredients: List[dict]) -> dict:
        generated = self.agent.generate_recipe(ingredients)
        recipe = {
            "title": generated["title"],
            "description": generated["description"],
            "instructions": generated["instructions"],
            "ingredients": ingredients,
            "generated_by": "gpt",
        }
        return self.repo.create(recipe)
