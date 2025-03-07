import pytest
from app import create_app

def test_config():
    """Test create_app with testing config."""
    assert not create_app().testing
    assert create_app(config_name="testing").testing

def test_hello(client):
    """Test that the application responds to requests."""
    response = client.get("/api/auth-status")
    assert response.status_code == 200 