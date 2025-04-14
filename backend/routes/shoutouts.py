# backend/routes/shoutouts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from backend.models.Shoutout import Shoutout as ShoutoutModel
from backend.schemas.shoutout_schema import Shoutout, ShoutoutCreate
from backend.config.database import get_db
from backend.utils.dependencies import get_current_user
from backend.models.User import User
from datetime import datetime, timezone
from typing import List

router = APIRouter(
    prefix="/shoutouts",
    tags=["Shoutouts"],
)

@router.post("/", response_model=Shoutout)
def create_shoutout(
    shoutout: ShoutoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_shoutout = ShoutoutModel(
        message=shoutout.message,
        user_id=current_user.id,
        target_user_id=shoutout.target_user_id,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_shoutout)
    db.commit()
    db.refresh(db_shoutout)

    target_user = db.query(User).filter(User.id == shoutout.target_user_id).first() if shoutout.target_user_id else None

    return {
        **db_shoutout.__dict__,
        "sender_first_name": current_user.first_name,
        "recipient_first_name": target_user.first_name if target_user else None
    }


@router.get("/", response_model=List[Shoutout])
def get_shoutouts(db: Session = Depends(get_db)):
    shoutouts = db.query(ShoutoutModel).options(
        joinedload(ShoutoutModel.user),
        joinedload(ShoutoutModel.target_user)
    ).order_by(ShoutoutModel.created_at.desc()).all()

    results = []
    for s in shoutouts:
        results.append(Shoutout(
            id=s.id,
            message=s.message,
            user_id=s.user_id,
            created_at=s.created_at.isoformat() + "Z",
            target_user_id=s.target_user_id,
            sender_first_name=s.user.first_name if s.user else None,
            recipient_first_name=s.target_user.first_name if s.target_user else None
        ))
    return results


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

ShoutoutRouter = router