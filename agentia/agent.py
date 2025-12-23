from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agentia.prompts import SYSTEM_PROMPT
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

llm = ChatOpenAI(
    temperature=0.6,
    model="gpt-4o-mini"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}")
])

chain = prompt | llm
