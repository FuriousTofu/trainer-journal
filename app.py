from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "main.login"
db = SQLAlchemy()


# https://flask.palletsprojects.com/en/stable/patterns/appfactories/
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = "so_secret_wery_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trainer.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    login_manager.init_app(app)

    from routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
