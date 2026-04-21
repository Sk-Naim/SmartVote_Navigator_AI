from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={"session_id": "test_session", "message": "Where do I vote? 90210"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["triggered_action"] == "trigger_maps"

def test_location_endpoint():
    response = client.get("/locations?zip_code=10001")
    assert response.status_code == 200
    data = response.json()
    assert "10001" in data["address"]
    assert "maps_url" in data
    assert data["distance_miles"] > 0

def test_indian_location_endpoint():
    response = client.get("/locations?zip_code=713101")
    assert response.status_code == 200
    data = response.json()
    assert "Burdwan" in data["address"]
    assert "maps_url" in data
    assert "Burdwan" in data["maps_url"]

def test_reminder_endpoint():
    response = client.post("/reminder", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "calendar.google.com" in data["calendar_link"]
