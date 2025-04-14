import pytest
from fastapi.testclient import TestClient
from main import app
from config.database import SessionLocal
from models.User import User as UserModel
from utils.auth import hash_password, create_access_token

client = TestClient(app)

# Fixtures
@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def test_user(db):
    user = UserModel(
        first_name="Test",
        last_name="User",
        email="testuser@example.com",
        hashed_password=hash_password("password"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"email": user.email, "password": "password", "id": user.id}

@pytest.fixture
def auth_header(test_user):
    token = create_access_token({"sub": test_user["email"]})
    return {"Authorization": f"Bearer {token}"}

# Tests
def test_login_success(test_user):
    res = client.post("/api/auth/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_failure():
    res = client.post("/api/auth/login", data={
        "username": "notreal@example.com",
        "password": "wrong"
    })
    assert res.status_code == 401


def test_protected_route_unauthenticated():
    res = client.get("/api/users/me")
    assert res.status_code == 401


def test_protected_route_authenticated(auth_header):
    res = client.get("/api/users/me", headers=auth_header)
    assert res.status_code == 200
    assert res.json()["email"] == "testuser@example.com"
