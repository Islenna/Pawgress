# models/Category.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Date, Text
from sqlalchemy.orm import relationship
from config.database import Base  
from datetime import datetime, timezone


class CERecord(Base):
    __tablename__ = "ce_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    ce_type = Column(Text, nullable=False)
    ce_description = Column(Text, nullable=False)
    ce_date = Column(Date, nullable=False)
    ce_hours = Column(Float, nullable=False)
    ce_file_path = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("User", back_populates="ce_records", passive_deletes=True)
