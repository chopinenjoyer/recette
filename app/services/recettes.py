from typing import List, Dict, Optional

class RecipeService:
    def __init__(self):
        self._store: Dict[int, Dict] = {}
        self._next_id = 1

    def create_recipe(self, title: str, description: Optional[str], ingredients: List[Dict], instructions: Optional[str], generated_by: Optional[str] = None) -> Dict:
        item = {
            "id": self._next_id,
            "title": title,
            "description": description,
            "ingredients": ingredients,
            "instructions": instructions,
            "generated_by": generated_by,
        }
        self._store[self._next_id] = item
        self._next_id += 1
        return item

    def get_recipe(self, recipe_id: int) -> Optional[Dict]:
        return self._store.get(recipe_id)

    def update_recipe(self, recipe_id: int, title: str, description: Optional[str], ingredients: List[Dict], instructions: Optional[str]) -> Optional[Dict]:
        if recipe_id not in self._store:
            return None
        item = self._store[recipe_id]
        item.update({"title": title, "description": description, "ingredients": ingredients, "instructions": instructions})
        return item

    def delete_recipe(self, recipe_id: int) -> bool:
        return self._store.pop(recipe_id, None) is not None

    def list_recipes(self) -> List[Dict]:
        return list(self._store.values())