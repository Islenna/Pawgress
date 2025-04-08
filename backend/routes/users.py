from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from models.User import User as UserModel
from schemas.user_schema import UserSchema, UserCreate
from utils.auth import hash_password


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# Create a new user

@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(user.password)
    db_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        license_number=user.license_number,
        license_expiry=user.license_expiry
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Get all users
@router.get("/", response_model=List[UserSchema])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

# Get a user by ID
@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get a user by username
@router.get("/username/{username}", response_model=UserSchema)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update a user by ID
@router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user.dict()
    if 'password' in user_data:
        user_data['hashed_password'] = hash_password(user_data.pop('password'))

    for key, value in user_data.items():
        setattr(db_user, key, value)

    
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete a user by ID
@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return db_user

UserRouter = router
