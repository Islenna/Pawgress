from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from config.database import Base


# models/UserSkill.py
class Proficiency(Base):
    __tablename__ = "proficiencies"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)

    proficiency = Column(Integer)  # 0-5 scale
    signed_off_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    signed_off_at = Column(DateTime, default=None, nullable=True)

    signed_off_by_user = relationship("User", foreign_keys=[signed_off_by])

    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="proficiencies",
        passive_deletes=True
    )

    skill = relationship("Skill", back_populates="proficiencies", passive_deletes=True)


