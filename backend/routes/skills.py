from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from models.Skill import Skill as SkillModel
from schemas.skill_schema import Skill as SkillSchema, SkillCreate
from schemas.category_schema import CategoryWithSkills
from utils.dependencies import get_current_user  # Assuming you have a function to get the current user
from models.User import User as UserModel
from utils.logger import log_action

router = APIRouter(
    prefix="/skills",
    tags=["Skills"],
)

# Create a skill
@router.post("/", response_model=SkillSchema)
def create_skill(skill: SkillCreate, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    db_skill = SkillModel(**skill.model_dump())

    # Check if the skill already exists
    existing_skill = db.query(SkillModel).filter(SkillModel.name == skill.name).first()
    if existing_skill:
        raise HTTPException(status_code=400, detail="Skill already exists")
    log_action(current_user, "create_skill", target=f"skill {skill.name}", extra={"skill": skill.model_dump()})
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

# Get all skills
@router.get("/", response_model=List[SkillSchema])
def get_skills(skip: int = 0, limit: int = 500, 
            db: Session = Depends(get_db),
            current_user: UserModel = Depends(get_current_user)):
    return db.query(SkillModel).offset(skip).limit(limit).all()

# Get skill by ID
@router.get("/{skill_id}", response_model=SkillSchema)
def get_skill(skill_id: int, 
            db: Session = Depends(get_db),
            current_user: UserModel = Depends(get_current_user)):
    skill = db.query(SkillModel).filter(SkillModel.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

# Get skill by name
@router.get("/name/{name}", response_model=SkillSchema)
def get_skill_by_name(name: str, 
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(get_current_user)):
    skill = db.query(SkillModel).filter(SkillModel.name == name).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

# Update skill
@router.put("/{skill_id}", response_model=SkillSchema)
def update_skill(skill_id: int, skill: SkillCreate, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    db_skill = db.query(SkillModel).filter(SkillModel.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    for key, value in skill.model_dump().items():
        setattr(db_skill, key, value)
    log_action(current_user, "update_skill", target=f"skill {skill.name}", extra={"skill": skill.model_dump()})
    db.commit()
    db.refresh(db_skill)
    return db_skill

# Delete skill
@router.delete("/{skill_id}")
def delete_skill(skill_id: int, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)):
    db_skill = db.query(SkillModel).filter(SkillModel.id == skill_id).first()
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    log_action(current_user, "delete_skill", target=f"skill {db_skill.name}", extra={"skill": db_skill.__dict__})

    db.delete(db_skill)
    db.commit()
    return {"detail": "Skill deleted successfully"}

SkillRouter = router
