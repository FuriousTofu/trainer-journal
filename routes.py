from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app import db
from models import Trainer, Client, Session, Exercise, SessionExercise
from forms import RegisterForm, LoginForm, AddExerciseForm

bp = Blueprint("main", __name__)

@bp.route("/")
@login_required
def index():
    return render_template("main.html")

@bp.route("/sessions")
@login_required
def sessions():
    return "Тут буде список сесій"

@bp.route("/clients")
@login_required
def clients():
    return "Тут буде список клієнтів"

@bp.route("/exercises", methods=["GET", "POST"])
@login_required
def exercises():
    stmt = select(Exercise).where(Exercise.trainer_id == current_user.id)
    exercises = db.session.execute(stmt).scalars().all()
    return render_template("exercises.html", exercises=exercises)

@bp.route("/exercises/add", methods=["GET", "POST"])
@login_required
def add_exercise():
    form = AddExerciseForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        description = form.description.data.strip() if form.description.data else None
        new_exercise = Exercise(name=name, description=description, trainer_id=current_user.id)
        try:
            db.session.add(new_exercise)
            db.session.commit()
            flash("Exercise added successfully", "success")
            return redirect(url_for(".add_exercise"))
        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("An exercise with this name already exists.")
    return render_template("add_exercise.html", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(".index"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        stmt = select(Trainer).where(Trainer.email == email)
        trainer = db.session.execute(stmt).scalar_one_or_none()
        if trainer and check_password_hash(trainer.password_hash, form.password.data):
            login_user(trainer, remember=form.remember_me.data)
            flash("Login successful", "success")
            return redirect(url_for(".index"))
        form.password.errors.append("Invalid email or password.")

    return render_template("login.html" , form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for(".login"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(".index"))
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