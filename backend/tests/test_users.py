import pytest
from fastapi.testclient import TestClient
from main import app
from models.User import User as UserModel
from utils.auth import hash_password

client = TestClient(app)

def test_get_me(auth_header):
    res = client.get("/api/users/me", headers=auth_header)
    assert res.status_code == 200
    assert res.json()["email"] == "testadmin@example.com"

def test_get_users(auth_header):
    res = client.get("/api/users/", headers=auth_header)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_update_user_role(auth_header, db):
    user = db.query(UserModel).filter(UserModel.email == "role_test@example.com").first()
    if not user:
        user = UserModel(
            first_name="Role",
            last_name="Test",
            email="role_test@example.com",
            hashed_password=hash_password("password"),
            role="user",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    update_data = {
        "role": "admin"
    }

    res = client.put(f"/api/users/{user.id}", json=update_data, headers=auth_header)
    assert res.status_code == 200, res.json()
    assert res.json()["role"] == "admin"

def test_unauthorized_user_access():
    res = client.get("/api/users/")
    assert res.status_code == 401
