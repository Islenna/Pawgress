from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

class SkillWithCategory(SkillBase):
    category: Optional[str] = None  # Include category name

    model_config = ConfigDict(from_attributes=True)
