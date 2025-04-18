from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from utils.dependencies import get_current_user  
from utils.logger import log_action
from schemas.CE_schema import CERecordCreate, CERecord
from models.CERecord import CERecord as CERecordModel
from models.User import User as UserModel
from utils.permissions import prevent_demo_changes
import os
from zipfile import ZipFile
from uuid import uuid4
from pathlib import Path
import tempfile
import re

router= APIRouter(
    prefix="/ce_records",
    tags=["CE Records"],
)

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "static" / "ce_docs"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "ce_docs")

# Create a new CE record entry
@router.post("/", response_model=CERecord)
async def create_ce_record(
    ce_record: CERecordCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    new_ce_record = CERecordModel(**ce_record.model_dump(), user_id=current_user.id)

    db.add(new_ce_record)
    db.commit()
    db.refresh(new_ce_record)

    log_action(current_user, "create_ce_record", target=f"CE record {ce_record.ce_description}", extra={"ce_record": ce_record.model_dump()})
    prevent_demo_changes(current_user)
    return new_ce_record
    
# Upload a CE record file
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

    # 🔒 Validate extension BEFORE saving
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    def sanitize_filename(filename: str) -> str:
        name, ext = os.path.splitext(filename)
        safe_name = re.sub(r"[^\w\-_.]", "_", name)  # Replace sketchy chars
        return f"{uuid4()}_{safe_name}{ext}"

    filename = sanitize_filename(file.filename)  # ✅ Use the sanitizer here
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    ce_record.ce_file_path = f"/static/ce_docs/{filename}"
    db.commit()

    log_action(
        current_user,
        "upload_ce_file",
        target=f"CE record {ce_record.ce_description}",
        extra={"file": filename}
    )
    prevent_demo_changes(current_user)
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
    for key, value in ce_record.model_dump().items():
        setattr(ce_record_to_update, key, value)
    log_action(
        current_user,
        "update_ce_record",
        target=f"CE record {ce_record.ce_description}",
        extra={"ce_record": ce_record.model_dump()},
    )
    prevent_demo_changes(current_user)
    db.commit()
    db.refresh(ce_record_to_update)
    return ce_record_to_update

# Download all CE documents for a user
@router.get("/user/{user_id}/download-all")
def download_all_ce_files(
    user_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role != "superuser":
        raise HTTPException(status_code=403, detail="Unauthorized")

    records = db.query(CERecordModel).filter(CERecordModel.user_id == user_id).all()
    files = [
        os.path.join(STATIC_DIR, os.path.basename(r.ce_file_path))
        for r in records
        if r.ce_file_path and os.path.exists(os.path.join(STATIC_DIR, os.path.basename(r.ce_file_path)))
    ]

    if not files:
        raise HTTPException(status_code=404, detail="No CE files found")
    #Temporary directory for the zip file
    temp_dir = tempfile.gettempdir()
    zip_name = os.path.join(temp_dir, f"ce_user_{user_id}.zip")
    # Create a zip file
    with ZipFile(zip_name, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=os.path.basename(file))
    prevent_demo_changes(current_user)
    # Schedule file deletion after response
    background_tasks.add_task(os.remove, zip_name)

    return FileResponse(zip_name, filename=f"ce_records_user_{user_id}.zip", media_type="application/zip")

# Delete a CE record entry
@router.delete("/{ce_record_id}", response_model=CERecord)
async def delete_ce_record(
    ce_record_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    ce_record_to_delete = db.query(CERecordModel).filter(CERecordModel.id == ce_record_id).first()
    if not ce_record_to_delete:
        raise HTTPException(status_code=404, detail="CE record not found")

    # 🧼 Delete associated file if it exists
    if ce_record_to_delete.ce_file_path:
        file_path = Path(__file__).resolve().parent.parent / ce_record_to_delete.ce_file_path.lstrip("/")
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            print(f"⚠️ Error deleting file: {e}")

    db.delete(ce_record_to_delete)
    db.commit()

    log_action(
        current_user,
        "delete_ce_record",
        target=f"CE record {ce_record_to_delete.ce_description}",
        extra={"ce_record": ce_record_to_delete.__dict__},
    )
    prevent_demo_changes(current_user)
    return ce_record_to_delete


CERouter = router