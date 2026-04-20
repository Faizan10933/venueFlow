import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_stadium_info():
    response = client.get("/api/stadium")
    assert response.status_code == 200
    data = response.json()
    assert "info" in data
    assert "zones" in data
    assert data["info"]["name"] == "Wankhede Stadium"
    assert len(data["zones"]) > 0

def test_cors_headers():
    response = client.options("/api/stadium", headers={
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "GET"
    })
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

def test_security_headers():
    response = client.get("/api/stadium")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-XSS-Protection"] == "1; mode=block"

def test_chat_endpoint_empty():
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 400

def test_websocket_connection():
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert "zones" in data
        assert "sim_time" in data
        
        # Test ping-pong
        websocket.send_text("ping")
        response = websocket.receive_text()
        assert response == "pong"
