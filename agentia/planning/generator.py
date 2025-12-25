import json
import random
from pathlib import Path
from agentia.data.knowledge.food_groups import FOOD_GROUPS
from agentia.planning.profiles import MEAL_PROFILES, MAX_HISTORY
from agentia.data.knowledge.seasons import seasonal_legumes


HISTORY_FILE = Path("agentia/data/history.json")

def load_history():
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text())
    return {
        "proteines": [],
        "styles": [],
        "profiles": []
    }

def save_history(history):
    HISTORY_FILE.write_text(json.dumps(history, indent=2))

def pick_excluding(options, excluded):
    filtered = [o for o in options if o not in excluded]
    return random.choice(filtered if filtered else options)

def generate_meal_plan(days: int):
    history = load_history()
    plan = []

    for day in range(days):
        profile = pick_excluding(
            list(MEAL_PROFILES.keys()),
            history["profiles"]
        )
        profile_data = MEAL_PROFILES[profile]

        protein = pick_excluding(
            profile_data["proteines"],
            history["proteines"]
        )

        style = pick_excluding(
            profile_data["styles"],
            history["styles"]
        )

        feculent = random.choice(FOOD_GROUPS["feculents"])
        season_legumes = seasonal_legumes(FOOD_GROUPS["legumes"])
        legume_pool = season_legumes if season_legumes else FOOD_GROUPS["legumes"]
        legume = random.choice(legume_pool)

        plan.append({
            "day": day + 1,
            "profile": profile,
            "protein": protein,
            "feculent": feculent,
            "legume": legume,
            "style": style
        })

        history["profiles"].append(profile)
        history["proteines"].append(protein)
        history["styles"].append(style)

    history["profiles"] = history["profiles"][-MAX_HISTORY:]
    history["proteines"] = history["proteines"][-MAX_HISTORY:]
    history["styles"] = history["styles"][-MAX_HISTORY:]

    save_history(history)
    return plan
