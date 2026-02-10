import os
from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .config import DevelopmentConfig, ProductionConfig
from .utils import init_template_filters

login_manager = LoginManager()
login_manager.login_view = "main.login"

db = SQLAlchemy()
csrf = CSRFProtect()


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["20 per minute"],
    storage_uri="memory://",
)


def create_app(config_class=None):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    if config_class is None:
        env = os.environ.get("FLASK_ENV", "development")
        if env == "production":
            config_class = ProductionConfig
        else:
            config_class = DevelopmentConfig

    app.config.from_object(config_class)
    if not app.config["SQLALCHEMY_DATABASE_URI"]:
        raise ValueError("SQLALCHEMY_DATABASE_URI is not set.")
    if not app.config["SECRET_KEY"]:
        raise ValueError("SECRET_KEY is not set.")

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    init_template_filters(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
