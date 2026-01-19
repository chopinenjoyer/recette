from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[1]


def read_json(*path_parts, default=None):
    path = BASE_DIR.joinpath(*path_parts)
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(*path_parts, data):
    path = BASE_DIR.joinpath(*path_parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def ask_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
        except ValueError:
            pass
        print("Veuillez entrer un nombre valide.")
