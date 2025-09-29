from flask import Blueprint, render_template

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("main.html")

@bp.route("/clients")
def clients():
    return "Тут буде список клієнтів"

@bp.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")