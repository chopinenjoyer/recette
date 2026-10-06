from sqlalchemy.orm import Session
from app.db.models import Recipe

class RecipeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_recipe(self, title, description, ingredients, instructions=None, generated_by=None):
        recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            generated_by=generated_by
        )
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        return recipe

    def get_recipe(self, recipe_id):
        return self.db.query(Recipe).filter(Recipe.id == recipe_id).first()
    
    def list_recipes(self):
        return self.db.query(Recipe).all()