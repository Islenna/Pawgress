from pydantic import BaseModel
from typing import Optional

class SkillBase(BaseModel):
    name: str
    description: Optional[str] = None  # Optional field for description
    category_id: Optional[int] = None  # Optional field for category ID

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    category_id: Optional[int]

    class Config:
        from_attributes = True

