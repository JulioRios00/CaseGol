import json
import pytest
from flask import session

def test_login(client, auth):
    """Test login functionality."""
    response = auth.login()
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "user_id" in data
    assert data["message"] == "Login successful"
    
    response = auth.login(username="wronguser", password="password123")
    assert response.status_code == 401
    data = json.loads(response.data)
    assert "error" in data
    
    response = auth.login(username="testuser", password="wrongpassword")
    assert response.status_code == 401
    data = json.loads(response.data)
    assert "error" in data

def test_logout(client, auth):
    """Test logout functionality."""
    auth.login()
    
    response = auth.logout()
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Logged out successfully"

def test_register(client):
    """Test user registration."""
    response = client.post(
        "/api/register",
        data={"username": "newuser", "password": "newpassword"},
        follow_redirects=True
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "user_id" in data
    assert data["message"] == "User registered successfully"
    
    response = client.post(
        "/api/register",
        data={"username": "testuser", "password": "newpassword"},
        follow_redirects=True
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data 