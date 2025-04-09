from pydantic import BaseModel
from typing import Optional, List
from schemas.skill_schema import Skill  # if you want to nest skills in response

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
