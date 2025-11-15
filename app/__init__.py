from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .template_filters import init_template_filters

login_manager = LoginManager()
login_manager.login_view = "main.login"
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = "so_secret_wery_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.instance_path}/trainer.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    login_manager.init_app(app)

    init_template_filters(app)
    
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
