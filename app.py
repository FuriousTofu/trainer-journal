from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# https://flask.palletsprojects.com/en/stable/patterns/appfactories/
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trainer.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app