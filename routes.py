from flask import Blueprint

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return "Привіт з routes.py!"

@bp.route("/clients")
def clients():
    return "Тут буде список клієнтів"
