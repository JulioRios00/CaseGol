import pytest
from app.models.models import Flight, User
from app.utils.utils import hash_password

def test_user_model(app):
    """Test the User model."""
    with app.app_context():
        # Test creating a new user
        user = User(username="modeluser", password=hash_password("modelpassword"))
        assert user.username == "modeluser"
        assert user.password == hash_password("modelpassword")
        
        # Test user authentication methods
        assert user.is_authenticated
        assert user.is_active
        assert not user.is_anonymous
        
        # Test get_id method
        assert user.get_id() == str(user.id)

def test_flight_model(app):
    """Test the Flight model."""
    with app.app_context():
        # Test creating a new flight
        flight = Flight(ano=2023, mes=4, mercado="SAOFOR", rpk=1500.0)
        assert flight.ano == 2023
        assert flight.mes == 4
        assert flight.mercado == "SAOFOR"
        assert flight.rpk == 1500.0 