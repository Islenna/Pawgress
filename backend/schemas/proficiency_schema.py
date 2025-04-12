# schemas/proficiency_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SignedOffByUser(BaseModel):
    id: int
    username: str

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
    signed_off_by_user: Optional[SignedOffByUser]

    class Config:
        orm_mode = True

class ProficiencyWithSkill(ProficiencyBase):
    id: int
    skill_name: str
    signed_off_by_user: Optional[SignedOffByUser]

    class Config:
        orm_mode = True