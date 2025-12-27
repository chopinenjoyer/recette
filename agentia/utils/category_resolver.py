NORMALIZED_CATEGORIES = {
    "poisson": "poissons",
    "poissons": "poissons",
    "fruit de mer": "fruits de mer",
    "fruits de mer": "fruits de mer",
    "crustaces": "fruits de mer",
    "crustacés": "fruits de mer",
    "viande rouge": "viandes",
    "viande": "viandes",
    "volaille": "volailles",
    "lait": "produits laitiers",
    "fromage": "produits laitiers",
    "produits laitiers": "produits laitiers",
    "legumes": "legumes",
    "légumes": "legumes",
    "fruits": "fruits",
}

def normalize_category(raw: str) -> str | None:
    raw = raw.lower().strip()
    return NORMALIZED_CATEGORIES.get(raw)
