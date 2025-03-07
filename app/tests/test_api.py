import json
import pytest
from flask import session

def test_dashboard_data_unauthenticated(client):
    """Test dashboard data endpoint without authentication."""
    response = client.get("/api/dashboard-data")
    assert response.status_code == 401

def test_dashboard_data_authenticated(client, auth):
    """Test dashboard data endpoint with authentication."""
    auth.login()
    
    response = client.get("/api/dashboard-data")
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert "year_min" in data
    assert "year_max" in data
    assert "markets" in data
    
    assert "BSBBEL" in data["markets"]
    assert "RIOCGH" in data["markets"]

def test_filter_endpoint(client, auth):
    """Test the filter endpoint."""
    auth.login()
    
    response = client.post(
        "/api/filter",
        data={
            "market": "BSBBEL",
            "start_year": 2022,
            "start_month": 1,
            "end_year": 2022,
            "end_month": 3
        }
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert "flights" in data
    assert "labels" in data
    assert "rpk_values" in data
    assert "market" in data
    
    assert len(data["flights"]) == 3
    assert len(data["labels"]) == 3
    assert len(data["rpk_values"]) == 3
    
    assert data["market"] == "BSBBEL"

def test_markets_endpoint(client, auth):
    """Test the markets endpoint."""
    auth.login()
    
    response = client.get("/api/dashboard-data/markets")
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert "status" in data
    assert "count" in data
    assert "markets" in data
    
    assert data["status"] == "success"
    
    assert data["count"] == 2
    
    assert "BSBBEL" in data["markets"]
    assert "RIOCGH" in data["markets"]

def test_auth_status_endpoint(client, auth):
    """Test the auth status endpoint."""
    response = client.get("/api/auth-status")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "authenticated" in data
    assert data["authenticated"] is False
    
    auth.login()
    response = client.get("/api/auth-status")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "authenticated" in data
    assert data["authenticated"] is True
    assert "user_id" in data
    assert "username" in data
    assert data["username"] == "testuser" 