# schemas/user_schema.py

from pydantic import BaseModel
from datetime import date
from typing import Optional

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

