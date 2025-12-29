from fastapi import FastAPI
from app.api.v1.routes import router as api_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bievenue sur l'API de Recette"}

app.include_router(api_router, prefix="/api/v1")