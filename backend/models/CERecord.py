# models/Category.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Date
from sqlalchemy.orm import relationship
from config.database import Base  
from datetime import datetime


class CERecord(Base):
    __tablename__ = "ce_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    ce_type = Column(String, nullable=False)
    ce_description = Column(String, nullable=False)
    ce_date = Column(Date, nullable=False)
    ce_hours = Column(Float, nullable=False)
    ce_file_path = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="ce_records")
