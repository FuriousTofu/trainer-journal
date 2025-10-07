from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from app import db
from models import Trainer, Client, Session, Exercise, SessionExercise
from forms import RegisterForm

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
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        password_hash = generate_password_hash(form.password.data)
        new_trainer = Trainer(name=username, email=email, password_hash=password_hash)
        db.session.add(new_trainer)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            form.email.errors.append("Email already registered. Please use a different email.")
            return render_template("register.html", form=form)
        
        login_user(new_trainer)
        flash("Registration successful", "success")
        return redirect(url_for(".index"))
    
    return render_template("register.html" , form=form)