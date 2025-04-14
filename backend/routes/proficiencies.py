from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from config.database import get_db
from models.Proficiency import Proficiency as ProficiencyModel
from schemas.proficiency_schema import ProficiencyCreate, Proficiency as ProficiencySchema
from utils.dependencies import get_current_user  
from utils.logger import log_action
from models.Skill import Skill
from models.User import User
from datetime import datetime, timezone

router = APIRouter(
    prefix="/proficiencies",
    tags=["Proficiencies"],
)

# Create a proficiency entry
@router.post("/", response_model=ProficiencySchema)
def create_proficiency(
    prof: ProficiencyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_prof = ProficiencyModel(**prof.model_dump())
    skill = db.query(Skill).filter(Skill.id == prof.skill_id).first()
    target_user = db.query(User).filter(User.id == prof.user_id).first()
    db_prof.signed_off_by = current_user.id
    db_prof.signed_off_at = datetime.now(timezone.utc)

    db.add(db_prof)
    db.commit()
    db.refresh(db_prof)

    signed_by = db.query(User).filter(User.id == db_prof.signed_off_by).first()

    log_action(
        current_user,
        "create_proficiency",
        target=f"user:{target_user.full_name}" if target_user else f"id:{prof.user_id}",
        extra={
            "skill": skill.name if skill else f"id:{prof.skill_id}",
            "proficiency": prof.proficiency,
            "signed_off_by": signed_by.full_name if signed_by else None
        }
    )

    return {
        **db_prof.__dict__,
        "signed_off_by_user": {
    "id": signed_by.id,
    "first_name": signed_by.first_name,
    "last_name": signed_by.last_name
    }
    if signed_by else None
    }

# Get all proficiencies

@router.get("/", response_model=List[ProficiencySchema])
def get_proficiencies(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ProficiencyModel)
    if user_id:
        query = query.filter(ProficiencyModel.user_id == user_id)

    profs = query.all()

    enriched = []
    for p in profs:
        signed_by = db.query(User).filter(User.id == p.signed_off_by).first()

        enriched.append({
            "id": p.id,
            "user_id": p.user_id, 
            "skill_id": p.skill_id,
            "proficiency": p.proficiency,
            "signed_off_by": p.signed_off_by,
            "signed_off_at": p.signed_off_at,
            "signed_off_by_user": {
                "id": signed_by.id,
                "first_name": signed_by.first_name,
                "last_name": signed_by.last_name,
            } if signed_by else None
        })

    return enriched


# Get a specific proficiency
@router.get("/{prof_id}", response_model=ProficiencySchema)
def get_proficiency(
    prof_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prof = db.query(ProficiencyModel).filter(ProficiencyModel.id == prof_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Proficiency not found")
    return prof

# Update a proficiency
@router.put("/{prof_id}", response_model=ProficiencySchema)
def update_proficiency(
    prof_id: int,
    updated: ProficiencyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prof = db.query(ProficiencyModel).filter(ProficiencyModel.id == prof_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Proficiency not found")

    for key, value in updated.model_dump().items():
        setattr(prof, key, value)

    prof.signed_off_by = updated.signed_off_by
    if not prof.signed_off_at and prof.signed_off_by:
        prof.signed_off_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(prof)

    signed_by = db.query(User).filter(User.id == prof.signed_off_by).first()

    log_action(
        current_user,
        "update_proficiency",
        target=f"proficiency_id:{prof_id}",
        extra=updated.model_dump()
    )

    return {
        **prof.__dict__,
        "signed_off_by_user": {
            "id": signed_by.id,
            "first_name": signed_by.first_name,
            "last_name": signed_by.last_name
        } if signed_by else None
    }


# Delete a proficiency
@router.delete("/{prof_id}")
def delete_proficiency(
    prof_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prof = db.query(ProficiencyModel).filter(ProficiencyModel.id == prof_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Proficiency not found")

    skill = db.query(Skill).filter(Skill.id == prof.skill_id).first()
    target_user = db.query(User).filter(User.id == prof.user_id).first()

    log_action(
        current_user,
        "delete_proficiency",
        target=f"proficiency_id:{prof_id}",
        extra={
            "skill": skill.name if skill else f"id:{prof.skill_id}",
            "target_user": target_user.full_name if target_user else f"id:{prof.user_id}",
            "proficiency": prof.proficiency
        }
    )

    db.delete(prof)
    db.commit()
    return {"detail": "Proficiency deleted successfully"}

ProficiencyRouter = router
