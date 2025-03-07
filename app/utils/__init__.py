import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "main.login"


def create_app(config_name="default"):
    app = Flask(__name__)
    
    # Use environment variable for database URL with SQLite fallback
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    
    # Fix Heroku's postgres:// vs postgresql:// issue
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    @app.shell_context_processor
    def make_shell_context():
        from app.models.models import Flight, User

        return {"db": db, "User": User, "Flight": Flight}

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from app.models.models import Flight, User

    return app
