from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CERecordBase(BaseModel):
    ce_type: str
    ce_date: datetime
    ce_hours: float
    ce_description: str
    ce_file_path: Optional[str] = None  # S3 or local path

class CERecordCreate(CERecordBase):
    pass

class CERecord(CERecordBase):
    id: int
    user_id: int  # Still returned in response
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
