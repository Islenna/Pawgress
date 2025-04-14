import pytest
from fastapi.testclient import TestClient
from main import app
from utils.auth import hash_password, create_access_token
from models.Shoutout import Shoutout

client = TestClient(app)

def test_create_shoutout(auth_header):
    data = {
        "message": "Big props to the team!",
        "target_user_id": None
    }
    res = client.post("/api/shoutouts/", json=data, headers=auth_header)
    assert res.status_code == 200
    assert res.json()["message"] == "Big props to the team!"

def test_create_shoutout_with_target(auth_header, db):
    # Add a second test user to shout out
    from models.User import User
    user = User(
        first_name="Jane",
        last_name="Doe",
        email="janedoe@example.com",
        hashed_password=hash_password("password"),
        role="user",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    data = {
        "message": "Jane crushed it today!",
        "target_user_id": user.id
    }
    res = client.post("/api/shoutouts/", json=data, headers=auth_header)
    assert res.status_code == 200
    assert res.json()["recipient_first_name"] == "Jane"

def test_get_shoutouts(auth_header):
    res = client.get("/api/shoutouts/", headers=auth_header)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

