from fastapi.testclient import TestClient
from app.apimain import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bievenue sur l'API de Recette"}

def test_get_recipes():
    response = client.get("/api/v1/recipes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_recipe():
    recipe_data = {
        "title": "Test Recipe",
        "description": "Test description",
        "ingredients": [
            {"name": "ingredient1", "quantity": "1"},
            {"name": "ingredient2", "quantity": "2"}
        ]
    }
    response = client.post("/api/v1/recipes/", json=recipe_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == recipe_data["title"]
    assert "id" in data
    assert "generated_by" in data