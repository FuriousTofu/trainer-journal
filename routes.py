from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from app import db
from models import Trainer, Client, Session, Exercise, SessionExercise

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
    if request.method == "POST":
        name = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password")
        password2 = request.form.get("password2")
        if not name or not email or not password or not password2:
            flash("Please fill in all required fields.", "warning")
            return render_template("register.html"), 400
        
        elif password != password2:
            flash("Passwords do not match.", "warning")
            return render_template("register.html"), 400
        elif len(password) < 8:
            flash("Password must be at least 8 characters long.", "warning")
            return render_template("register.html"), 400
        else:
            password_hash = generate_password_hash(password)
            new_trainer = Trainer(name=name, email=email, password_hash=password_hash)
            db.session.add(new_trainer)
            try:
                db.session.commit()
                flash("Registration successful. Please log in.", "success")
                login_user(new_trainer)
                return redirect(url_for(".index"))
            except IntegrityError:
                db.session.rollback()
                flash("Email already registered. Please use a different email.", "error")
                return render_template("register.html"), 409
    else:
        return render_template("register.html")