from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import DevelopmentConfig
from .utils import init_template_filters

login_manager = LoginManager()
login_manager.login_view = "main.login"

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)
    if not app.config["SQLALCHEMY_DATABASE_URI"]:
        raise ValueError("SQLALCHEMY_DATABASE_URI is not set.")
    if not app.config["SECRET_KEY"]:
        raise ValueError("SECRET_KEY is not set.")

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    init_template_filters(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
