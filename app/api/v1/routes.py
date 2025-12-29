from fastapi import APIRouter, HTTPException, status
from typing import List
from app.api.v1.schemas import Recipe, RecipeCreate, Ingredient
from app.agentia.agent import generate_recipe

router = APIRouter()

_RECIPES: List[Recipe] = []
_next_id = 1

@router.get("/recipes/", response_model=List[Recipe])
def list_recipes():
    return _RECIPES

@router.post("/recipes/", response_model=Recipe, status_code=status.HTTP_201_CREATED)
def create_recipe(payload: RecipeCreate):
    global _next_id
    generated = generate_recipe([ing.name for ing in payload.ingredients])
    ingredients_out = generated.get("ingredients")
    if not ingredients_out:
        ingredients_out = [{"name": n, "quantity": "à convenance"} for n in [ing.name for ing in payload.ingredients]]

    recipe = Recipe(
        id=_next_id,
        title=generated.get("title", payload.title),
        description=generated.get("description"),
        ingredients=[Ingredient(**i) for i in ingredients_out],
        generated_by=generated.get("generated_by", "gpt")
    )
    _RECIPES.append(recipe)
    _next_id += 1
    return recipe

@router.get("/recipes/{recipe_id}", response_model=Recipe)
def get_recipe(recipe_id: int):
    for r in _RECIPES:
        if r.id == recipe_id:
            return r
    raise HTTPException(status_code=404, detail="Recipe not found")