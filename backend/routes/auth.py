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
    # OAuth2PasswordRequestForm uses "username" field for backwards compatibility
    # So we treat form_data.username as the email input
    email = form_data.username.strip().lower()

    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(
        data={
            "sub": user.email,
            "name": f"{user.first_name} {user.last_name}",
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

AuthRouter = router
