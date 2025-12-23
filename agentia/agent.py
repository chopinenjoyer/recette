from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(
    temperature=0.6,
    model="gpt-4o-mini"
)

def build_chain(system_prompt: str):
    """
    Construit une chaîne IA à partir du prompt système fourni.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    return prompt | llm
