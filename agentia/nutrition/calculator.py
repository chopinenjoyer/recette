from agentia.nutrition.profiles import SPORT_PROFILES

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

    calories = round(calories)
    protein = round(protein)
    carbs = round(carbs)
    fats = round(fats)

    return {
        "objective": objective,

        "calories_per_day": calories,
        "protein_g_per_day": protein,
        "carbs_g_per_day": carbs,
        "fats_g_per_day": fats,

        "total_calories": calories * days * persons,
        "total_protein_g": protein * days * persons,
        "total_carbs_g": carbs * days * persons,
        "total_fats_g": fats * days * persons,
    }
