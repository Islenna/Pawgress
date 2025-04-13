# schemas/user_schema.py
from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional
from backend.schemas.proficiency_schema import Proficiency
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    license_number: Optional[str] = None
    license_expiry: Optional[date] = None

class UserCreate(BaseModel):
    email: str
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    license_number: Optional[str] = None
    license_expiry: Optional[date] = None


class UserSchema(UserBase):  # Renamed from `User` to avoid collision with models.User
    id: int
    is_active: bool = True
    role: str = "user"
    first_name: str
    last_name: str
    class Config:
        from_attributes = True

class UserWithProficiencies(UserSchema):
    skills: list = []  # Include skills in the response

    class Config:
        from_attributes = True
        from_attributes = True  # Enable ORM mode for SQLAlchemy compatibility

class PasswordUpdate(BaseModel):
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
    
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    license_number: Optional[str] = None
    license_expiry: Optional[datetime] = None
    role: Optional[str] = None
