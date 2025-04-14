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


def test_get_skills(db, auth_header):
    res = client.get("/api/skills/", headers=auth_header)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) > 0
    assert all("name" in skill for skill in res.json())
    assert all("description" in skill for skill in res.json())
    assert all("category_id" in skill for skill in res.json())
    assert all("id" in skill for skill in res.json())


def test_update_skill(db, auth_header, test_skill):
    skill_id = test_skill["id"]
    updated_data = {
    "name": "Updated Skill",
    "description": "Updated description",
    "category_id": test_skill["category_id"]
}
    
    res = client.put(f"/api/skills/{skill_id}", json=updated_data, headers=auth_header)
    assert res.status_code == 200, res.json()
    assert res.json()["name"] == updated_data["name"]
    assert res.json()["description"] == updated_data["description"]
    assert res.json()["category_id"] == test_skill["category_id"]


def test_delete_skill(db, auth_header, test_skill):
    skill_id = test_skill["id"]

    res = client.delete(f"/api/skills/{skill_id}", headers=auth_header)
    assert res.status_code == 200
    assert res.json()["detail"] == "Skill deleted successfully"

    # Confirm deletion
    res = client.get(f"/api/skills/{skill_id}", headers=auth_header)
    assert res.status_code == 404


def test_skills_unauthorized():
    res = client.get("/api/skills/")
    assert res.status_code == 401
