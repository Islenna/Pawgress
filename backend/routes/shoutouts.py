# backend/routes/shoutouts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.Shoutout import Shoutout as ShoutoutModel
from backend.schemas.shoutout_schema import Shoutout, ShoutoutCreate
from backend.config.database import get_db
from backend.utils.dependencies import get_current_user
from backend.models.User import User

router = APIRouter(
    prefix="/shoutouts",
    tags=["Shoutouts"],
)

@router.post("/", response_model=Shoutout)
def create_shoutout(shoutout: ShoutoutCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_shoutout = ShoutoutModel(message=shoutout.message, user_id=current_user.id)
    db.add(db_shoutout)
    db.commit()
    db.refresh(db_shoutout)
    return db_shoutout

@router.get("/", response_model=list[Shoutout])
def get_shoutouts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(ShoutoutModel).order_by(ShoutoutModel.created_at.desc()).all()

@router.delete("/{shoutout_id}")
def delete_shoutout(shoutout_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    shoutout = db.query(ShoutoutModel).filter_by(id=shoutout_id).first()
    if not shoutout:
        raise HTTPException(status_code=404, detail="Shoutout not found")
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete shoutouts")
    db.delete(shoutout)
    db.commit()
    return {"detail": "Shoutout deleted"}
