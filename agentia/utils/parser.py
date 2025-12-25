import json
import re


def extract_ingredients_from_response(text: str) -> list:
    match = re.search(r"\{[\s\S]*?\}", text)
    if not match:
        return []

    try:
        data = json.loads(match.group())
        return [
            i.strip().lower()
            for i in data.get("ingredients", [])
            if isinstance(i, str)
        ]
    except json.JSONDecodeError:
        return []


def remove_json_block(text: str) -> str:
    text = re.sub(r"```json[\s\S]*?```", "", text)
    text = re.sub(r"\{[\s\S]*?\}", "", text)
    return text.strip()
