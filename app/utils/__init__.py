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
    
    # Use the Heroku PostgreSQL URL
    heroku_db_url = 'postgres://ue2vq6vfrikq1a:p1973b361910c931982a079e3016e495e9c9c03d24d39488ac5850c09e05f06ed@c3nv2ev86aje4j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dfuev85km9t3nd'
    database_url = os.environ.get('DATABASE_URL', heroku_db_url)

    # Fix Heroku's postgres:// vs postgresql:// issue
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    # Set the database URI in app config
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
