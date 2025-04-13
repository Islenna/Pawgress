# backend/schemas/proficiency_schema.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProficiencyBase(BaseModel):
    user_id: int
    skill_id: int
    proficiency: int
    signed_off_by: Optional[int] = None
    signed_off_at: Optional[datetime] = None

class ProficiencyCreate(BaseModel):
    user_id: int
    skill_id: int
    proficiency: int
    signed_off_by: Optional[int] = None

class SignedOffByUser(BaseModel):
    id: int
    first_name: str
    last_name: str

class Proficiency(ProficiencyBase):
    id: int
    signed_off_by_user: Optional[SignedOffByUser]

    class Config:
        from_attributes = True

class ProficiencyWithSkill(ProficiencyBase):
    id: int
    skill_name: str
    signed_off_by_user: Optional[SignedOffByUser]

    class Config:
        from_attributes = True