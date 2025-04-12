from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from backend.config.database import get_db
from backend.utils.dependencies import get_current_user  
from backend.utils.logger import log_action
from backend.schemas.CE_schema import CERecordCreate, CERecord
from backend.models.CERecord import CERecord as CERecordModel
from backend.models.User import User as UserModel
import os
from uuid import uuid4

router= APIRouter(
    prefix="/ce_records",
    tags=["CE Records"],
)

UPLOAD_DIR = "uploads/ce_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
# Create a new CE record entry
@router.post("/", response_model=CERecord)
async def create_ce_record(
    ce_record: CERecordCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    new_ce_record = CERecordModel(**ce_record.dict(), user_id=current_user.id)

    db.add(new_ce_record)
    db.commit()
    db.refresh(new_ce_record)

    log_action(current_user, "create_ce_record", target=f"CE record {ce_record.ce_description}", extra={"ce_record": ce_record.dict()})

    return new_ce_record

#Upload a CE record file
@router.post("/{ce_record_id}/upload")
async def upload_ce_file(
    ce_record_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    ce_record = db.query(CERecordModel).filter(CERecordModel.id == ce_record_id).first()
    if not ce_record:
        raise HTTPException(status_code=404, detail="CE record not found")

    filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    ce_record.ce_file_path = f"/static/ce_docs/{filename}"
    db.commit()
    log_action(current_user, "upload_ce_file", target=f"CE record {ce_record.ce_description}", extra={"file": filename})
    return {"message": "File uploaded successfully", "filename": filename}

# Get all CE records for a user
@router.get("/user/{user_id}", response_model=List[CERecord])
async def get_ce_records_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Check if the user exists
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all CE records for the user
    ce_records = db.query(CERecordModel).filter(CERecordModel.user_id == user_id).all()

    return ce_records

# Edit a CE record entry
@router.put("/{ce_record_id}", response_model=CERecord)
async def update_ce_record(
    ce_record_id: int,
    ce_record: CERecordCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Check if the CE record exists
    ce_record_to_update = db.query(CERecordModel).filter(CERecordModel.id == ce_record_id).first()
    if not ce_record_to_update:
        raise HTTPException(status_code=404, detail="CE record not found")

    # Update the CE record
    for key, value in ce_record.dict().items():
        setattr(ce_record_to_update, key, value)
    log_action(
        current_user,
        "update_ce_record",
        target=f"CE record {ce_record.ce_description}",
        extra={"ce_record": ce_record.dict()},
    )
    db.commit()
    db.refresh(ce_record_to_update)
    return ce_record_to_update


# Delete a CE record entry
@router.delete("/{ce_record_id}", response_model=CERecord)
async def delete_ce_record(
    ce_record_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Check if the CE record exists
    ce_record_to_delete = db.query(CERecordModel).filter(CERecordModel.id == ce_record_id).first()
    if not ce_record_to_delete:
        raise HTTPException(status_code=404, detail="CE record not found")

    # Delete the CE record
    db.delete(ce_record_to_delete)
    db.commit()

    # Log the action
    log_action(
        current_user,
        "delete_ce_record",
        target=f"CE record {ce_record_to_delete.ce_description}",
        extra={"ce_record": ce_record_to_delete.__dict__},
    )

    return ce_record_to_delete

CERouter = router