from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from models.Proficiency import Proficiency as ProficiencyModel
from schemas.proficiency_schema import ProficiencyCreate, Proficiency as ProficiencySchema
from utils.dependencies import get_current_user  
from utils.logger import log_action
from models.Skill import Skill
from models.User import User

router = APIRouter(
    prefix="/proficiencies",
    tags=["Proficiencies"],
)

# Create a proficiency entry
@router.post("/", response_model=ProficiencySchema)
def create_proficiency(prof: ProficiencyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_prof = ProficiencyModel(**prof.dict())

    skill = db.query(Skill).filter(Skill.id == prof.skill_id).first()
    target_user = db.query(User).filter(User.id == prof.user_id).first()

    log_action(
        current_user,
        "create_proficiency",
        extra={
            "skill": skill.name if skill else f"id:{prof.skill_id}",
            "target_user": target_user.username if target_user else f"id:{prof.user_id}",
            "proficiency": prof.proficiency
        }
    )

    db.add(db_prof)
    db.commit()
    db.refresh(db_prof)

    signed_by = db.query(User).filter(User.id == db_prof.signed_off_by).first()
    return {
        **db_prof.__dict__,
        "signed_off_by_user": {
            "id": signed_by.id,
            "username": signed_by.username
        } if signed_by else None
    }

# Get all proficiencies
@router.get("/", response_model=List[ProficiencySchema])
def get_proficiencies(
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)
):
    profs = db.query(ProficiencyModel).all()

    enriched = []
    for p in profs:
        signed_by = db.query(User).filter(User.id == p.signed_off_by).first()
        enriched.append({
            **p.__dict__,
            "signed_off_by_user": {
                "id": signed_by.id,
                "username": signed_by.username
            } if signed_by else None
        })

    return enriched
# Get a specific proficiency
@router.get("/{prof_id}", response_model=ProficiencySchema)
def get_proficiency(prof_id: int, 
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    prof = db.query(ProficiencyModel).filter(ProficiencyModel.id == prof_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Proficiency not found")
    return prof

# Update a proficiency
@router.put("/{prof_id}", response_model=ProficiencySchema)
def update_proficiency(prof_id: int, updated: ProficiencyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    prof = db.query(ProficiencyModel).filter(ProficiencyModel.id == prof_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Proficiency not found")

    for key, value in updated.dict().items():
        setattr(prof, key, value)

    log_action(current_user, "update_proficiency", target=f"proficiency {prof_id}", extra={"updated_fields": updated.dict()})
    
    db.commit()
    db.refresh(prof)

    signed_by = db.query(User).filter(User.id == prof.signed_off_by).first()
    return {
        **prof.__dict__,
        "signed_off_by_user": {
            "id": signed_by.id,
            "username": signed_by.username
        } if signed_by else None
    }

# Delete a proficiency
@router.delete("/{prof_id}", response_model=ProficiencySchema)
def delete_proficiency(prof_id: int, 
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    prof = db.query(ProficiencyModel).filter(ProficiencyModel.id == prof_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Proficiency not found")

    skill = db.query(Skill).filter(Skill.id == prof.skill_id).first()
    target_user = db.query(User).filter(User.id == prof.user_id).first()

    log_action(
        current_user,
        "delete_proficiency",
        target=f"proficiency {prof_id}",
        extra={
            "skill": skill.name if skill else f"id:{prof.skill_id}",
            "target_user": target_user.username if target_user else f"id:{prof.user_id}",
            "proficiency": prof.proficiency
        }
    )

    db.delete(prof)
    db.commit()
    return prof


ProficiencyRouter = router
