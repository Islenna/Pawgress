from fastapi.responses import StreamingResponse
import io
import csv
from sqlalchemy.orm import aliased
from fastapi import APIRouter, Depends, HTTPException
from models import User, Skill, Proficiency
from config.database import get_db
from sqlalchemy.orm import Session
from utils.dependencies import get_current_user

router = APIRouter(prefix="/exports", tags=["Exports"])

@router.get("/proficiencies", response_class=StreamingResponse)
def export_proficiencies(
    user_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Regular users can only export their own data
    if current_user.role == "user":
        user_id = current_user.id
    elif current_user.role in ("admin", "superuser"):
        if user_id is None:
            raise HTTPException(status_code=400, detail="user_id required for export")
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")

    SignedOffBy = aliased(User)

    results = (
        db.query(
            Skill.name.label("Skill"),
            Proficiency.proficiency.label("Proficiency"),
            Proficiency.signed_off_at.label("Signed Off At"),
            SignedOffBy.full_name.label("Signed Off By"),
        )
        .join(Skill, Skill.id == Proficiency.skill_id)
        .join(User, User.id == Proficiency.user_id)
        .outerjoin(SignedOffBy, SignedOffBy.id == Proficiency.signed_off_by)
        .filter(Proficiency.user_id == user_id)
        .all()
    )

    def generate():
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Skill", "Proficiency", "Signed Off At", "Signed Off By"])
        for row in results:
            writer.writerow(row)
        yield output.getvalue()
        output.close()

    filename = f"user_{user_id}_proficiencies.csv"
    return StreamingResponse(generate(), media_type="text/csv", headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })

ExportRouter = router
