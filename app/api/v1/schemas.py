from pydantic import BaseModel
from typing import List


class Ingredient(BaseModel):
    name: str
    quantity: str
    
class RecipeCreate(BaseModel):
    ingredients: List[Ingredient]

class RecipeOut(BaseModel):
    id: int
    title: str
    description: str
    instructions: str
    ingredients: List[Ingredient]
    generated_by: str