from agentia.nutrition.profiles import SPORT_PROFILES
from agentia.config.nutrition import CALORIES_PER_KG, MACRO_RATIOS


def calculate_macros(
    weight_kg: float,
    objective: str,
    days: int,
    persons: int
):
    profile = SPORT_PROFILES[objective]

    maintenance = weight_kg * 33
    calories = maintenance * profile["calorie_factor"]

    protein = profile["protein_g_per_kg"] * weight_kg
    fats = (calories * profile["fat_ratio"]) / 9
    carbs = (calories - (protein * 4 + fats * 9)) / 4

    return {
        "calories_per_day": round(calories),
        "protein_g_per_day": round(protein),
        "carbs_g_per_day": round(carbs),
        "fats_g_per_day": round(fats),
        "total_calories": round(calories * days * persons)
    }
