from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from config.database import Base
from typing import Optional
from models.Proficiency import Proficiency 


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=True)

    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="skills")
    proficiencies = relationship("Proficiency", back_populates="skill", passive_deletes=True)
