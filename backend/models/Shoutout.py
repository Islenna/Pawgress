from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime, timezone

class Shoutout(Base):
    __tablename__ = "shoutouts"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    user_id = Column(Integer, ForeignKey("users.id"))  # creator
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # recipient

    user = relationship("User", foreign_keys=[user_id], back_populates="shoutouts")
    target_user = relationship("User", foreign_keys=[target_user_id])
