# models/Category.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from config.database import Base  # You can abstract Base into a common base module

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True)
    description = Column(String(255), nullable=True)

    skills = relationship("Skill", back_populates="category")