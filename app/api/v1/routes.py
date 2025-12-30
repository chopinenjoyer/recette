from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.api.v1.schemas import RecipeCreate, RecipeOut
from app.repositories.recipes_repo import RecipeRepository
from app.services.recettes import RecipeService
from app.agentia.agent import RecipeAgent

router = APIRouter(prefix="/api/v1/recipes")


@router.post("/", response_model=RecipeOut, status_code=201)
def create_recipe(
    payload: RecipeCreate,
    db: Session = Depends(get_db),
):
    repo = RecipeRepository(db)
    agent = RecipeAgent()
    service = RecipeService(repo=repo, agent=agent)

    return service.create_recipe(
        ingredients=[i.dict() for i in payload.ingredients]
    )
