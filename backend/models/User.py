from sqlalchemy import Column, Integer, String, Boolean, Date, Enum as SqlEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum  # This is Python's Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime
from config.database import Base

# Define your role enum using Python's Enum
class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"
    superuser = "superuser"

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(SqlEnum(RoleEnum), default=RoleEnum.user)  # <-- SQLAlchemy Enum
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    license_number = Column(String(255), unique=True, nullable=True)
    license_expiry = Column(Date, nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    skills = relationship("Skill", back_populates="user")
