import pytest
from app.utils.utils import hash_password, direct_login, direct_register
from app.models.models import User
from app import db

def test_hash_password():
    """Test the hash_password function."""
    password = "testpassword"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    assert hash1 == hash2
    
    password2 = "differentpassword"
    hash3 = hash_password(password2)
    assert hash1 != hash3

def test_direct_login(app):
    """Test the direct_login function."""
    with app.app_context():
        success, error = direct_login("testuser", "password123")
        assert success is True
        assert error is None
        
        success, error = direct_login("wronguser", "password123")
        assert success is False
        assert error is not None
        
        success, error = direct_login("testuser", "wrongpassword")
        assert success is False
        assert error is not None

def test_direct_register(app):
    """Test the direct_register function."""
    with app.app_context():
        success, error = direct_register("newregisteruser", "newpassword")
        assert success is True
        assert error is None
        
        user = User.query.filter_by(username="newregisteruser").first()
        assert user is not None
        assert user.username == "newregisteruser"
        
        success, error = direct_register("testuser", "anotherpassword")
        assert success is False
        assert error is not None 