# backend/schemas/shoutout_schema.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ShoutoutBase(BaseModel):
    message: str

class ShoutoutCreate(ShoutoutBase):
    target_user_id: Optional[int] = None

class Shoutout(ShoutoutBase):
    id: int
    user_id: int
    created_at: datetime
    target_user_id: Optional[int] = None

    sender_first_name: Optional[str] = None
    recipient_first_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
