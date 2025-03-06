from flask import Flask, jsonify
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "/login"

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Authentication required"}), 401

def create_app(config_name="default"):
    app = Flask(__name__)

    # Set a secure secret key
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    @app.shell_context_processor
    def make_shell_context():
        from app.models.models import Flight, User

        return {"db": db, "User": User, "Flight": Flight}

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    with app.app_context():
        from app.dashapp import init_dashboard
        init_dashboard(app)

    from app.models.models import Flight, User

    return app
