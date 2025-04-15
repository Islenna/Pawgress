# backend/routes/metrics.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.Skill import Skill
from models.Category import Category
from models.Proficiency import Proficiency
from utils.dependencies import get_current_user
from models.User import User
from typing import Dict, List
from collections import defaultdict
from sqlalchemy import func

router = APIRouter(
    prefix="/metrics",
    tags=["Admin Metrics"]
)

@router.get("/")
def get_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ("admin", "superuser"):
        return {"error": "Unauthorized"}

    total_skills = db.query(Skill).count()
    total_profs = db.query(Proficiency).count()
    signed_off = db.query(Proficiency).filter(Proficiency.signed_off_by.isnot(None)).count()

    # Avg proficiency per skill
    
    avg_per_skill = db.query(
        Skill.name.label("skill_name"),
        func.avg(Proficiency.proficiency).label("avg_prof")
    ).join(Skill, Skill.id == Proficiency.skill_id)\
    .group_by(Skill.id, Skill.name)\
    .all()


    avg_proficiency_map = {
    skill_name: round(avg, 2)
    for skill_name, avg in avg_per_skill
}


    # Breakdown per category
    category_breakdown = []
    categories = db.query(Category).all()
    for cat in categories:
        skill_ids = [skill.id for skill in cat.skills]
        profs = db.query(Proficiency).filter(Proficiency.skill_id.in_(skill_ids)).all()
        if not profs:
            continue

        total = len(profs)
        signed = len([p for p in profs if p.signed_off_by])
        avg = round(sum(p.proficiency for p in profs) / total, 2)

        category_breakdown.append({
            "category": cat.name,
            "total": total,
            "signed_off": signed,
            "avg_proficiency": avg
        })

    return {
        "total_skills": total_skills,
        "total_proficiencies": total_profs,
        "signed_off_proficiencies": signed_off,
        "avg_proficiency_per_skill": avg_proficiency_map,
        "category_breakdown": category_breakdown
    }

MetricRouter = router