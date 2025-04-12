from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from schemas.skill_schema import Skill  # Assuming you already have this

class ProficiencyBase(BaseModel):
    user_id: int
    skill_id: int
    proficiency: int
    signed_off_by: Optional[int] = None
    signed_off_at: Optional[datetime] = None

class ProficiencyCreate(ProficiencyBase):
    pass

class Proficiency(ProficiencyBase):
    id: int

    class Config:
        from_attributes = True
        
class SkillShort(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
class ProficiencyWithSkill(BaseModel):
    id: int
    user_id: int
    skill_id: int
    proficiency: int
    signed_off_by: Optional[int] = None
    signed_off_at: Optional[datetime] = None
    skill: SkillShort

    class Config:
        from_attributes = True