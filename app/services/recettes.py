from typing import List
from app.agentia.main import RecipeAgent
from app. import RecipeRepository


class RecipeService:
    def __init__(self, repo: RecipeRepository, agent: RecipeAgent):
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
