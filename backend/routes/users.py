from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session, joinedload
from typing import List
from config.database import get_db
from models.User import User as UserModel
from schemas.user_schema import UserSchema, UserCreate
from utils.user_utils import create_and_return_user
from utils.auth import hash_password
from utils.dependencies import get_current_user
from utils.logger import log_action
from schemas.user_schema import UserWithProficiencies
from models.Proficiency import Proficiency as ProficiencyModel
from schemas.proficiency_schema import ProficiencyWithSkill

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# Create a new user (protected, optional — mostly for admin use)
@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return create_and_return_user(user, db)

# Register a new user (public route)
@router.post("/register", response_model=UserSchema)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create the user once
    created = create_and_return_user(user, db)

    # Log the action
    log_action(created, "register", extra={"username": created.username})
    
    return created

# Get all users (protected)
@router.get("/", response_model=List[UserSchema])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return db.query(UserModel).offset(skip).limit(limit).all()

# Get me (protected)
@router.get("/me", response_model=UserWithProficiencies)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

# Get user with proficiencies (protected)
@router.get("/mine", response_model=List[ProficiencyWithSkill])
def get_my_proficiencies(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    proficiencies = (
        db.query(ProficiencyModel)
        .options(joinedload(ProficiencyModel.skill))
        .filter(ProficiencyModel.user_id == current_user.id)
        .all()
    )
    return proficiencies

# Get a user by ID (protected)
@router.get("/{user_id}", response_model=UserWithProficiencies)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get a user by username (protected)
@router.get("/username/{username}", response_model=UserSchema)
def get_user_by_username(username: str, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update a user by ID (protected)
@router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.dict()
    if "password" in user_data:
        user_data["hashed_password"] = hash_password(user_data.pop("password"))

    for key, value in user_data.items():
        setattr(db_user, key, value)

    log_action(current_user, "update", target=f"user {user_id}", extra={"updated_fields": user_data})

    db.commit()
    db.refresh(db_user)
    return db_user

# Delete a user by ID (protected)
@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    log_action(current_user, "delete", target=f"user {user_id}", extra={"username": db_user.username})
    db.delete(db_user)
    db.commit()
    return db_user

UserRouter = router