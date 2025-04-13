from pydantic import BaseModel
from typing import Optional, List
from backend.schemas.skill_schema import Skill  # if you want to nest skills in response

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    skills: List[Skill] = []

    class Config:
        from_attributes = True

class CategoryWithSkills(CategoryBase):
    skills: List[Skill] = []  # Include skills in the response

    class Config:
        from_attributes = True
        from_attributes = True  # Enable ORM mode for SQLAlchemy compatibility