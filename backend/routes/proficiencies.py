from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from models.Proficiency import Proficiency as ProficiencyModel
from schemas.proficiency_schema import ProficiencyCreate, Proficiency as ProficiencySchema
from utils.dependencies import get_current_user  
from models.User import User as UserModel

router = APIRouter(
    prefix="/proficiencies",
    tags=["Proficiencies"],
)

# Create a proficiency entry
@router.post("/", response_model=ProficiencySchema)
def create_proficiency(prof: ProficiencyCreate, 
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(get_current_user)):
    db_prof = ProficiencyModel(**prof.dict())
    db.add(db_prof)
    db.commit()
    db.refresh(db_prof)
    return db_prof

# Get all proficiencies
@router.get("/", response_model=List[ProficiencySchema])
def get_proficiencies(skip: int = 0, limit: int = 100, 
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(get_current_user)):
    return db.query(ProficiencyModel).offset(skip).limit(limit).all()

# Get a specific proficiency
@router.get("/{prof_id}", response_model=ProficiencySchema)
def get_proficiency(prof_id: int, 
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(get_current_user)):
    prof = db.query(ProficiencyModel).filter(ProficiencyModel.id == prof_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Proficiency not found")
    return prof

# Update a proficiency
@router.put("/{prof_id}", response_model=ProficiencySchema)
def update_proficiency(prof_id: int, 
                    updated: ProficiencyCreate, 
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(get_current_user)):
    prof = db.query(ProficiencyModel).filter(ProficiencyModel.id == prof_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Proficiency not found")
    for key, value in updated.dict().items():
        setattr(prof, key, value)
    db.commit()
    db.refresh(prof)
    return prof

# Delete a proficiency
@router.delete("/{prof_id}", response_model=ProficiencySchema)
def delete_proficiency(prof_id: int, 
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(get_current_user)):
    prof = db.query(ProficiencyModel).filter(ProficiencyModel.id == prof_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Proficiency not found")
    db.delete(prof)
    db.commit()
    return prof

ProficiencyRouter = router
