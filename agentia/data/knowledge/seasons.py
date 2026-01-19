from datetime import datetime

from datetime import datetime

SEASONAL_PRODUCTS = {
    "hiver": {
        "legumes": [
            "chou_vert", "chou_fleur", "chou_rouge",
            "choux_bruxelles",
            "poireau", "carotte", "navet", "panais",
            "endive", "epinards",
            "courge", "potiron", "butternut",
            "celeri_rave", "betterave",
            "topinambour", "fenouil"
        ],
        "fruits": [
            "pomme", "poire",
            "orange", "mandarine",
            "pamplemousse",
            "kiwi",
            "citron"
        ]
    },

    "printemps": {
        "legumes": [
            "asperges", "radis",
            "epinards", "laitue", "roquette", "mache",
            "petits_pois", "feves",
            "artichaut",
            "poireau"
        ],
        "fruits": [
            "fraise",
            "cerise",
            "rhubarbe"
        ]
    },

    "ete": {
        "legumes": [
            "tomate", "tomate_cerise",
            "courgette", "aubergine",
            "poivron",
            "concombre",
            "haricots_verts",
            "mais"
        ],
        "fruits": [
            "abricot", "peche", "nectarine",
            "melon", "pasteque",
            "framboise", "myrtille",
            "mure",
            "raisin"
        ]
    },

    "automne": {
        "legumes": [
            "courge", "potiron", "butternut",
            "champignons", "champignon_paris",
            "shiitake", "pleurotes", "portobello",
            "brocoli",
            "epinards",
            "poireau",
            "fenouil"
        ],
        "fruits": [
            "pomme", "poire",
            "raisin",
            "figue",
            "prune"
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

def filter_by_season(
    items: list[str],
    category: str
) -> list[str]:
    """
    category = 'legumes' ou 'fruits'
    """
    season = current_season()
    allowed = SEASONAL_PRODUCTS.get(season, {}).get(category, [])
    return [i for i in items if i in allowed]