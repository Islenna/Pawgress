# backend/schemas/shoutout_schema.py

from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ShoutoutBase(BaseModel):
    message: str

class ShoutoutCreate(ShoutoutBase):
    pass

class Shoutout(ShoutoutBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
