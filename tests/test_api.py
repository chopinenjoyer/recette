from fastapi.testclient import TestClient
from app.apimain import app
import app.agentia.agent as agent_module

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bievenue sur l'API de Recette"}

def test_get_recipes():
    response = client.get("/api/v1/recipes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.headers["content-type"].startswith("application/json")

def fake_generate_recipe(*args, **kwargs):
    return {
        "title": "Recette test IA",
        "instructions": "Étape 1, Étape 2",
        "generated_by": "test-agent"
    }
    
def test_create_recipe(monkeypatch):
    monkeypatch.setattr(
        agent_module,
        "generate_recipe",
        fake_generate_recipe
    )

    recipe_data = {
        "description": "Test description",
        "ingredients": [
            {"name": "ingredient1", "quantity": "1"},
            {"name": "ingredient2", "quantity": "2"}
        ]
    }

    response = client.post("/api/v1/recipes/", json=recipe_data)

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Recette test IA"
    assert data["generated_by"] == "test-agent"
    assert isinstance(data["id"], int)
    assert len(data["instructions"]) > 0

def test_create_recipe_invalid_payload():
    response = client.post("/api/v1/recipes/", json={})
    assert response.status_code == 422
