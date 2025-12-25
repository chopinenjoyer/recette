from datetime import datetime

SEASONAL_PRODUCTS = {
    "hiver": {
        "legumes": [
            "chou_vert", "chou_fleur", "poireau",
            "carotte", "navet", "panais",
            "endive", "epinards", "courge",
            "potiron", "butternut"
        ],
        "fruits": [
            "pomme", "poire", "kiwi",
            "orange", "mandarine"
        ]
    },
    "printemps": {
        "legumes": [
            "asperges", "radis", "epinards",
            "laitue", "petits_pois",
            "artichaut"
        ],
        "fruits": [
            "fraise", "cerise"
        ]
    },
    "ete": {
        "legumes": [
            "tomate", "tomate_cerise", "courgette",
            "aubergine", "poivron", "concombre"
        ],
        "fruits": [
            "melon", "pasteque", "abricot",
            "peche", "nectarine", "framboise"
        ]
    },
    "automne": {
        "legumes": [
            "courge", "potiron", "butternut",
            "champignons", "brocoli",
            "epinards"
        ],
        "fruits": [
            "pomme", "poire", "raisin", "figue"
        ]
    }
}

def current_season() -> str:
    month = datetime.now().month
    if month in (12, 1, 2):
        return "hiver"
    if month in (3, 4, 5):
        return "printemps"
    if month in (6, 7, 8):
        return "ete"
    return "automne"

def seasonal_legumes(all_legumes: list) -> list:
    season = current_season()
    allowed = SEASONAL_PRODUCTS.get(season, {}).get("legumes", [])
    return [l for l in all_legumes if l in allowed]
