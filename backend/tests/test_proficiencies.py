import pytest
from fastapi.testclient import TestClient
from main import app
from config.database import SessionLocal
from models.User import User as UserModel
from utils.auth import hash_password, create_access_token

client = TestClient(app)

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def auth_header(db):
    test_email = "testadmin@example.com"
    user = db.query(UserModel).filter(UserModel.email == test_email).first()
    if not user:
        user = UserModel(
            first_name="Test",
            last_name="Admin",
            email=test_email,
            hashed_password=hash_password("testpassword"),
            role="admin",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(data={
        "sub": user.email,
        "name": f"{user.first_name} {user.last_name}",
        "role": user.role
    })

    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_category(auth_header):
    category_data = {
        "name": "Test Category for Proficiencies",
        "description": "Temporary category for testing"
    }
    res = client.post("/api/categories/", json=category_data, headers=auth_header)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 400 and "already exists" in res.text:
        # Fallback: fetch existing category
        get_res = client.get("/api/categories/", headers=auth_header)
        for cat in get_res.json():
            if cat["name"] == category_data["name"]:
                return cat
    pytest.fail("Could not create or fetch test category")

@pytest.fixture
def test_skill(auth_header, test_category):
    skill_data = {
        "name": "Test Skill for Proficiency",
        "description": "Temporary skill for testing",
        "category_id": test_category["id"]
    }
    res = client.post("/api/skills/", json=skill_data, headers=auth_header)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 400 and "already exists" in res.text:
        get_res = client.get("/api/skills/", headers=auth_header)
        for skill in get_res.json():
            if skill["name"] == skill_data["name"]:
                return skill
    pytest.fail("Could not create or fetch test skill")


def test_create_proficiency(db, auth_header, test_skill):
    user = db.query(UserModel).filter(UserModel.email == "testadmin@example.com").first()

    proficiency_data = {
        "user_id": user.id,
        "skill_id": test_skill["id"],
        "proficiency": 3
    }
    res = client.post("/api/proficiencies/", json=proficiency_data, headers=auth_header)
    assert res.status_code == 200
    assert res.json()["skill_id"] == test_skill["id"]


def test_get_proficiencies(auth_header):
    res = client.get("/api/proficiencies/", headers=auth_header)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_update_proficiency(db, auth_header, test_skill):
    user = db.query(UserModel).filter(UserModel.email == "testadmin@example.com").first()
    # Create a proficiency
    create_res = client.post("/api/proficiencies/", json={
        "user_id": user.id,
        "skill_id": test_skill["id"],
        "proficiency": 2
    }, headers=auth_header)
    prof_id = create_res.json()["id"]

    # Update it
    res = client.put(f"/api/proficiencies/{prof_id}", json={
        "user_id": user.id,
        "skill_id": test_skill["id"],
        "proficiency": 5
    }, headers=auth_header)
    assert res.status_code == 200
    assert res.json()["proficiency"] == 5

def test_delete_proficiency(db, auth_header, test_skill):
    user = db.query(UserModel).filter(UserModel.email == "testadmin@example.com").first()
    res = client.post("/api/proficiencies/", json={
        "user_id": user.id,
        "skill_id": test_skill["id"],
        "proficiency": 1
    }, headers=auth_header)
    prof_id = res.json()["id"]

    res = client.delete(f"/api/proficiencies/{prof_id}", headers=auth_header)
    assert res.status_code == 200
    assert res.json()["detail"] == "Proficiency deleted successfully"

def test_proficiencies_unauthorized():
    res = client.get("/api/proficiencies/")
    assert res.status_code == 401
