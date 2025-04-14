import os
import pytest
from fastapi.testclient import TestClient
from main import app
from config.database import SessionLocal
from models.User import User as UserModel
from utils.auth import hash_password, create_access_token

client = TestClient(app)

# ✅ FIXED: Add missing decorator
@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

# ✅ FIXED: Auth fixture
@pytest.fixture
def auth_header(db):
    test_email = "testadmin@example.com"
    test_user = db.query(UserModel).filter(UserModel.email == test_email).first()
    if not test_user:
        test_user = UserModel(
            first_name="Test",
            last_name="Admin",
            email=test_email,
            hashed_password=hash_password("testpassword"),
            role="admin",
            is_active=True
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

    token = create_access_token(data={
        "sub": test_user.email,
        "name": f"{test_user.first_name} {test_user.last_name}",
        "role": test_user.role
    })

    return {"Authorization": f"Bearer {token}"}

# ✅ Create CE record
def test_create_ce(db, auth_header):
    ce_data = {
        "ce_description": "Test CE",
        "ce_date": "2023-10-01",
        "ce_hours": 1.5,
        "ce_type": "conference",
        "ce_status": "completed"
    }
    res = client.post("/api/ce_records/", json=ce_data, headers=auth_header)
    assert res.status_code == 200
    assert res.json()["ce_description"] == ce_data["ce_description"]

# ✅ Get CE records
def test_get_ce(db, auth_header):
    res = client.get("/api/ce_records/user/1", headers=auth_header)  # Replace 1 if needed
    assert res.status_code == 200
    assert isinstance(res.json(), list)

# ✅ Update CE record
def test_update_ce(db, auth_header):
    ce_data = {
        "ce_description": "To update",
        "ce_date": "2023-10-01",
        "ce_hours": 2.0,
        "ce_type": "online",
        "ce_status": "completed"
    }
    res = client.post("/api/ce_records/", json=ce_data, headers=auth_header)
    ce_id = res.json()["id"]

    update_data = {
        "ce_description": "Updated",
        "ce_date": "2023-11-01",
        "ce_hours": 3.0,
        "ce_type": "lecture",
        "ce_status": "in-progress"
    }
    res = client.put(f"/api/ce_records/{ce_id}", json=update_data, headers=auth_header)
    assert res.status_code == 200
    assert res.json()["ce_description"] == "Updated"

# ✅ Delete CE record
def test_delete_ce(db, auth_header):
    ce_data = {
        "ce_description": "To delete",
        "ce_date": "2023-10-01",
        "ce_hours": 2.0,
        "ce_type": "online",
        "ce_status": "completed"
    }
    res = client.post("/api/ce_records/", json=ce_data, headers=auth_header)
    ce_id = res.json()["id"]

    res = client.delete(f"/api/ce_records/{ce_id}", headers=auth_header)
    assert res.status_code == 200

    # Confirm deletion
    res = client.get(f"/api/ce_records/user/1", headers=auth_header)
    assert all(r["id"] != ce_id for r in res.json())

# ✅ Upload file (create it temporarily)
def test_upload_ce_file(db, auth_header):
    ce_data = {
        "ce_description": "Upload Test",
        "ce_date": "2023-10-01",
        "ce_hours": 2.0,
        "ce_type": "webinar",
        "ce_status": "completed"
    }

    # 1. Create a CE record first
    res = client.post("/api/ce_records/", json=ce_data, headers=auth_header)
    assert res.status_code == 200, res.json()
    ce_id = res.json()["id"]

    # 2. Prepare a fake file for upload
    test_file_content = b"%PDF-1.4 fake pdf content"
    files = {
        "file": ("test_ce_doc.pdf", test_file_content, "application/pdf")
    }

    # 3. Upload the file to the route
    res = client.post(f"/api/ce_records/{ce_id}/upload", headers=auth_header, files=files)
    assert res.status_code == 200, res.json()
    assert "filename" in res.json()
    assert res.json()["message"] == "File uploaded successfully"



def test_ce_unauthorized():
    res = client.get("/api/ce_records/user/1")
    assert res.status_code == 401