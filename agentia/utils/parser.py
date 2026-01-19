import re
from agentia.data.knowledge.food_groups import FOOD_GROUPS
from agentia.utils.category_resolver import normalize_category


def remove_json_block(text: str) -> str:
    text = re.sub(r"```json.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"<json>.*?</json>", "", text, flags=re.DOTALL)
    return text.strip()


def extract_ingredients_from_response(text: str):
    match = re.search(r"\{.*?\}", text, flags=re.DOTALL)
    if not match:
        return []
    content = match.group(0)
    ingredients = re.findall(r'"([^"]+)"', content)
    return [i.lower() for i in ingredients]


def extract_disliked_ingredients(text: str):
    text = text.lower()
    found = set()

    patterns = [
        r"je n'aime pas (.+)",
        r"j'aime pas (.+)",
        r"sans (.+)",
        r"plus de (.+)",
        r"plus d'(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            raw = match.group(1)
            tokens = re.split(r",| et |;", raw)
            for t in tokens:
                found.add(t.strip())

    if not found:
        tokens = re.split(r",| et |;", text)
        for t in tokens:
            if len(t.strip()) > 2:
                found.add(t.strip())

    flat_foods = {
        item.replace("_", " "): item
        for group in FOOD_GROUPS.values()
        for item in group
    }

    resolved = []
    for f in found:
        if f in flat_foods:
            resolved.append(flat_foods[f])
        else:
            resolved.append(f.replace(" ", "_"))

    return list(set(resolved))


def extract_disliked_categories(text: str) -> list[str]:
    text = text.lower()
    found = set()

    patterns = [
        r"plus de ([a-z\s]+)",
        r"sans ([a-z\s]+)",
        r"je n'aime pas ([a-z\s]+)",
        r"je suis allergique aux? ([a-z\s]+)",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            cat = normalize_category(match.strip())
            if cat:
                found.add(cat)

    return list(found)
