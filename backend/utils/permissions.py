from fastapi import HTTPException
from models.User import User

def prevent_demo_changes(user: User):
    if user.is_demo_user:
        raise HTTPException(status_code=403, detail="Demo user cannot perform this action")
