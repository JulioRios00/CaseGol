import os
import tempfile

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import create_app, db
from app.models.models import Flight, User
from app.utils.utils import hash_password


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SERVER_NAME': 'localhost.localdomain',
    })

    with app.app_context():
        db.create_all()
        _populate_test_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()


def _populate_test_db():
    """Populate the database with test data."""
    test_user = User(username="testuser", password=hash_password("password123"))
    db.session.add(test_user)
    
    test_flights = [
        Flight(ano=2022, mes=1, mercado="BSBBEL", rpk=1000.0),
        Flight(ano=2022, mes=2, mercado="BSBBEL", rpk=1200.0),
        Flight(ano=2022, mes=3, mercado="BSBBEL", rpk=1100.0),
        Flight(ano=2022, mes=1, mercado="RIOCGH", rpk=800.0),
        Flight(ano=2022, mes=2, mercado="RIOCGH", rpk=850.0),
    ]
    
    for flight in test_flights:
        db.session.add(flight)
    
    db.session.commit()


@pytest.fixture
def auth(client):
    """Authentication helper for tests."""
    class AuthActions:
        def login(self, username="testuser", password="password123"):
            return client.post(
                "/api/login",
                data={"username": username, "password": password},
                follow_redirects=True
            )

        def logout(self):
            return client.get("/api/logout", follow_redirects=True)

    return AuthActions() 