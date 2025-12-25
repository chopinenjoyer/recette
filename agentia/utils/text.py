def normalize(text: str) -> str:
    return (
        text.lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

def pretty(text: str) -> str:
    return text.replace("_", " ").capitalize()

def list_to_text(items: list) -> str:
    return ", ".join(pretty(i) for i in items)
