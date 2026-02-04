
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307 or response.status_code == 302
    assert "/static/index.html" in response.headers["location"]

def test_static_index():
    # Follow redirect to static HTML
    response = client.get("/")
    assert response.status_code == 200
    assert "Mergington High School" in response.text

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400

def test_unregister_from_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    # Try unregistering again (should fail)
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 400
