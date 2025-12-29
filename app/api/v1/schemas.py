from pydantic import BaseModel
from typing import List, Optional

class Ingredient(BaseModel):
    name: str
    quantity: str

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    ingredients: List[Ingredient]

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int

    class Config:
        orm_mode = True