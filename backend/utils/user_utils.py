from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.User import User as UserModel
from schemas.user_schema import UserCreate
from utils.auth import hash_password

def create_and_return_user(user_data: UserCreate, db: Session) -> UserModel:
    existing_user = db.query(UserModel).filter(
        (UserModel.username == user_data.username) | (UserModel.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    db_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        license_number=user_data.license_number,
        license_expiry=user_data.license_expiry
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
