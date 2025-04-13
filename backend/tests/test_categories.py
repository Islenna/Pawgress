import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.config.database import SessionLocal
from backend.models.User import User as UserModel
from backend.utils.auth import hash_password, create_access_token

client = TestClient(app)

@pytest.fixture  # <- This is what you were missing!
def db():
    db = SessionLocal()
    yield db
    db.close()


# Fixture to create a test user and get an auth token
@pytest.fixture
def auth_header(db):
    # Create test user
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

def test_create_category(test_category):
    assert test_category["name"] == "Test Category for Proficiencies"

def test_get_categories(db, auth_header):
    res = client.get("/api/categories/", headers=auth_header)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_update_category(db, auth_header):
    category_data = {
        "name": "Update Category",
        "description": "To be updated"
    }

    res = client.post("/api/categories/", json=category_data, headers=auth_header)

    if res.status_code == 200:
        category_id = res.json()["id"]
    elif res.status_code == 400 and "already exists" in res.text:
        get_res = client.get("/api/categories/", headers=auth_header)
        for cat in get_res.json():
            if cat["name"] == category_data["name"]:
                category_id = cat["id"]
                break
        else:
            pytest.fail("Category exists but could not be retrieved")
    else:
        pytest.fail(f"Unexpected error: {res.json()}")

    updated_data = {
        "name": "Updated Category",
        "description": "Updated description"
    }

    res = client.put(f"/api/categories/{category_id}", json=updated_data, headers=auth_header)
    assert res.status_code == 200
    assert res.json()["name"] == updated_data["name"]
    assert res.json()["description"] == updated_data["description"]



def test_delete_category(db, auth_header):
    category_data = {
        "name": "Delete Category",
        "description": "To be deleted"
    }
    res = client.post("/api/categories/", json=category_data, headers=auth_header)
    category_id = res.json()["id"]

    res = client.delete(f"/api/categories/{category_id}", headers=auth_header)
    assert res.status_code == 200

    res = client.get(f"/api/categories/{category_id}", headers=auth_header)
    assert res.status_code == 404
