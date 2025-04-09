from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProficiencyBase(BaseModel):
    user_id: int
    skill_id: int
    proficiency: int  # 0-5 scale
    signed_off_by: Optional[int] = None
    signed_off_at: Optional[datetime] = None

class ProficiencyCreate(ProficiencyBase):
    pass

class Proficiency(ProficiencyBase):
    id: int

    class Config:
        from_attributes = True
