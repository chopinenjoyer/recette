from dotenv import load_dotenv
from pathlib import Path
import os
import json
import re
from typing import List, Dict, Optional

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def _get_llm_and_prompt():
    if not OPENAI_API_KEY:
        return None, None
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
    except Exception:
        return None, None
    llm = ChatOpenAI(temperature=0.6, model="gpt-4o-mini")
    def build_chain(system_prompt: str):
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        return prompt | llm
    return llm, build_chain

LLM, _build_chain = _get_llm_and_prompt()

def generate_recipe(ingredients: List[str]) -> Dict:
    """
    Appelle le LLM si configuré, sinon retourne un fallback déterministe.
    """
    system_prompt = ""
    try:
        from .prompts import SYSTEM_PROMPT
        system_prompt = SYSTEM_PROMPT
    except Exception:
        system_prompt = ""

    if _build_chain is not None:
        try:
            chain = _build_chain(system_prompt)
            user_input = (
                "Génère une recette au format JSON avec les champs: "
                "title, description, ingredients (name+quantity), instructions, generated_by.\n"
                "Ingrédients:\n" + "\n".join(f"- {i}" for i in ingredients)
            )
            resp = chain.invoke({"input": user_input})
            text = getattr(resp, "content", str(resp))
            try:
                return json.loads(text)
            except Exception:
                pass
            m = re.search(r"\{(?:[^{}]|(?R))*\}", text, re.S)
            if m:
                try:
                    return json.loads(m.group(0))
                except Exception:
                    pass
        except Exception:
            pass

    return {
        "title": "Recette avec " + ", ".join(ingredients[:3]) if ingredients else "Recette",
        "description": f"Recette générée à partir des ingrédients: {', '.join(ingredients)}",
        "ingredients": [{"name": n, "quantity": "à convenance"} for n in ingredients],
        "instructions": "Mélanger les ingrédients et ajuster l'assaisonnement. Cuire selon goût.",
        "generated_by": "gpt" if OPENAI_API_KEY else "fallback"
    }
