# schemas/user_schema.py

from pydantic import BaseModel
from datetime import date
from typing import Optional
from schemas.proficiency_schema import Proficiency

class UserBase(BaseModel):
    username: str
    email: str
    license_number: Optional[str] = None
    license_expiry: Optional[date] = None

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):  # Renamed from `User` to avoid collision with models.User
    id: int
    is_active: bool = True
    role: str = "user"

    class Config:
        from_attributes = True

class UserWithProficiencies(UserSchema):
    skills: list = []  # Include skills in the response

    class Config:
        from_attributes = True
        orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility
