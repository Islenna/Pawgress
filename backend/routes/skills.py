from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from models.Skill import Skill as SkillModel
from schemas.skill_schema import Skill as SkillSchema, SkillCreate

router = APIRouter(
    prefix="/skills",
    tags=["Skills"],
)

# Create a skill
@router.post("/", response_model=SkillSchema)
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    db_skill = SkillModel(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

# Get all skills
@router.get("/", response_model=List[SkillSchema])
def get_skills(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(SkillModel).offset(skip).limit(limit).all()

# Get skill by ID
@router.get("/{skill_id}", response_model=SkillSchema)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(SkillModel).filter(SkillModel.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

# Get skill by name
@router.get("/name/{name}", response_model=SkillSchema)
def get_skill_by_name(name: str, db: Session = Depends(get_db)):
    skill = db.query(SkillModel).filter(SkillModel.name == name).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

# Update skill
@router.put("/{skill_id}", response_model=SkillSchema)
def update_skill(skill_id: int, skill: SkillCreate, db: Session = Depends(get_db)):
    db_skill = db.query(SkillModel).filter(SkillModel.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    for key, value in skill.dict().items():
        setattr(db_skill, key, value)
    
    db.commit()
    db.refresh(db_skill)
    return db_skill

# Delete skill
@router.delete("/{skill_id}", response_model=SkillSchema)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    db_skill = db.query(SkillModel).filter(SkillModel.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(db_skill)
    db.commit()
    return db_skill

SkillRouter = router
