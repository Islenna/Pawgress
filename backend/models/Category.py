# models/Category.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.base import Base  # You can abstract Base into a common base module

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String, nullable=True)

    skills = relationship("Skill", back_populates="category")

category_id = Column(Integer, ForeignKey("categories.id"))
category = relationship("Category", back_populates="skills")