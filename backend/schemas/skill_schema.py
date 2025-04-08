from pydantic import BaseModel
from typing import Optional

class SkillBase(BaseModel):
    name: str
    description: Optional[str] = None  # Optional field for description

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    category_id: int
    user_id: int

    class Config:
        from_attributes = True

