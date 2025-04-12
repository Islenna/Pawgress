from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.config.database import get_db
from backend.utils.auth import verify_password, create_access_token
from backend.models.User import User as UserModel

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(
    (UserModel.username == form_data.username) | (UserModel.email == form_data.username)
).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {"access_token": access_token, "token_type": "bearer"}

AuthRouter = router