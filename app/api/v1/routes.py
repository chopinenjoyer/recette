from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.api.v1.schemas import RecipeCreate, RecipeOut
from app.services.recettes import RecipeService

router = APIRouter(prefix="/api/v1/recipes")
service = RecipeService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RecipeOut, status_code=201)
def create_recipe_endpoint(data: RecipeCreate, db: Session = Depends(get_db)):
    return service.create_recipe(db, data.ingredients)