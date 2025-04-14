from fastapi.testclient import TestClient
from backend.main import app
from backend.config.database import SessionLocal
from backend.models.User import User as UserModel
from backend.utils.auth import hash_password, create_access_token
from sqlalchemy import text
import pytest

from backend.models.Category import Category as CategoryModel
from backend.models.Skill import Skill as SkillModel
from backend.models.Proficiency import Proficiency as ProficiencyModel
from backend.models.CERecord import CERecord as CERecordModel

client = TestClient(app)

@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture(autouse=True)
def clean_test_data(db):
    # 1. Delete Proficiencies
    db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    db.execute(text("""
        DELETE FROM proficiencies
        WHERE user_id IN (SELECT id FROM users WHERE email LIKE '%@example.com')
        OR signed_off_by IN (SELECT id FROM users WHERE email LIKE '%@example.com')
        OR skill_id IN (SELECT id FROM skills WHERE name LIKE 'Test%')
    """))

    # 2. Delete CE Records
    db.execute(text("""
        DELETE FROM ce_records
        WHERE user_id IN (SELECT id FROM users WHERE email LIKE '%@example.com')
    """))

    # 3. Delete Skills
    db.execute(text("""
        DELETE FROM skills
        WHERE name LIKE 'Test%'
    """))

    # 4. Delete Categories
    db.execute(text("""
        DELETE FROM categories
        WHERE name LIKE 'Test%' OR name LIKE 'Update%' OR name LIKE 'Delete%'
    """))

    #5 Delete Shoutouts
    db.execute(text("""
        DELETE FROM shoutouts
        WHERE user_id IN (SELECT id FROM users WHERE email LIKE '%@example.com')
        OR target_user_id IN (SELECT id FROM users WHERE email LIKE '%@example.com')
    """))

    # 6. Delete Users (last, after dependents)
    db.execute(text("""
        DELETE FROM users
        WHERE email LIKE '%@example.com'
    """))

    db.commit()


@pytest.fixture
def auth_header(db):
    email = "testadmin@example.com"
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        user = UserModel(
            first_name="Test",
            last_name="Admin",
            email=email,
            hashed_password=hash_password("password"),
            role="admin",
            is_active=True,
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
