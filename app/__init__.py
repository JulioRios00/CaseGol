import os

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "/login"


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


def create_app(config_name="default"):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "super-secreta")

    database_url = os.environ.get('DATABASE_URL', 'postgres://ue2vq6vfrikq1a:p1973b361910c931982a079e3016e495e9c9c03d24d39488ac5850c09e05f06ed@c3nv2ev86aje4j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dfuev85km9t3nd')
    
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

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
        from app.models.models import Flight, User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        from app.dashapp import init_dashboard

        init_dashboard(app)

    return app
