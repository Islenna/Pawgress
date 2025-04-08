from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from config.database import Base

class Skill(Base):
    __tablename__ = "skills"
    
    # Primary key for the skill
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic fields
    name = Column(String)
    description = Column(String, nullable=True)
    proficiency = Column(Integer, nullable=True)  # Assuming proficiency is an integer value

    # Foreign keys to associate the skill with a user and category
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    
    # Timestamp fields for created_at and updated_at
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships to User and Category
    user = relationship("User", back_populates="skills")
    category = relationship("Category", back_populates="skills")
