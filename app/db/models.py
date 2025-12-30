from sqlalchemy import Column, Integer, String, Text, JSON
from app.db.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    ingredients = Column(JSON, nullable=False)
    generated_by = Column(String, default="gpt")
