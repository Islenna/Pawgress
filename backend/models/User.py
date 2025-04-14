from sqlalchemy import Column, Integer, String, Boolean, Date, Enum as SqlEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from config.database import Base

class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"
    superuser = "superuser"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(SqlEnum(RoleEnum), default=RoleEnum.user)

    license_number = Column(String(255), unique=True, nullable=True)
    license_expiry = Column(Date, nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    proficiencies = relationship(
        "Proficiency",
        back_populates="user",
        foreign_keys="Proficiency.user_id"
    )

    ce_records = relationship(
        "CERecord",
        back_populates="user",
        cascade="all, delete"
    )

    shoutouts = relationship(
        "Shoutout",
        foreign_keys="Shoutout.user_id",
        back_populates="user"
    )

    shoutouts_received = relationship(
        "Shoutout",
        foreign_keys="Shoutout.target_user_id",
        back_populates="target_user"
    )
