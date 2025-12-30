from sqlalchemy.orm import Session
from app.db.models import Recipe


class RecipeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> dict:
        recipe = Recipe(**data)
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        return self._to_dict(recipe)

    def get(self, recipe_id: int) -> dict | None:
        recipe = self.db.query(Recipe).filter(Recipe.id == recipe_id).first()
        return self._to_dict(recipe) if recipe else None

    def _to_dict(self, recipe: Recipe) -> dict:
        return {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "instructions": recipe.instructions,
            "ingredients": recipe.ingredients,
            "generated_by": recipe.generated_by,
        }
