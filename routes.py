from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app import db
from models import Trainer, Client, Session, Exercise, SessionExercise
from forms import (
    RegisterForm, LoginForm, AddExerciseForm, 
    AddClientForm, AddSessionForm, AddSessionExerciseForm
)

bp = Blueprint("main", __name__)

@bp.route("/")
@login_required
def index():
    return render_template("main.html")

@bp.route("/sessions", methods=["GET", "POST"])
@login_required
def sessions():
    return render_template("sessions.html")

@bp.route("/sessions/add", methods=["GET", "POST"])
@login_required
def add_session():
    form = AddSessionForm()

    form.client.render_kw = {
        "hx-get": url_for(".client_price"),
        "hx-target": "#price-wrapper",
        "hx-trigger": "change",
        "hx-swap": "outerHTML"
    } # God bless HTMX

    clients = db.session.execute(
        select(Client.id, Client.name)
        .where(Client.trainer_id == current_user.id)
        .order_by(Client.name)
    ).all()
    form.client.choices = [(0, "Select Client")] + [(c.id, c.name) for c in clients]

    exercises = db.session.execute(
        select(Exercise.id, Exercise.name)
        .where(Exercise.trainer_id == current_user.id)
        .order_by(Exercise.name)
    ).all()
    exercise_choices = [(0, "Select Exercise")] + [(e.id, e.name) for e in exercises]
    for subform in form.exercises:
        subform.exercise.choices = exercise_choices
    
    if form.validate_on_submit():
        client = db.session.get(Client, form.client.data)
        if not client or client.trainer_id != current_user.id:
            abort(404)
        
        try:
            s = Session(
                client_id=form.client.data,
                start_dt=form.start_dt.data,
                duration_min=form.duration_min.data,
                mode=form.mode.data,
                price=form.price.data,
                notes=form.notes.data.strip() if form.notes.data else None,
            )
            db.session.add(s)
            db.session.flush() # to use s.id below

            for exercise_form in form.exercises:  
                sub: AddSessionExerciseForm = exercise_form.form # for code readability
                
                ex = db.session.get(Exercise, sub.exercise.data)
                if not ex or ex.trainer_id != current_user.id:
                    abort(404)

                se = SessionExercise(
                    session_id=s.id,
                    client_id=s.client_id,
                    exercise_id=sub.exercise.data,
                    sets=sub.sets.data,
                    reps=sub.reps.data,
                    weight=sub.weight.data,
                )
                db.session.add(se)
            db.session.commit()
            flash("Session added successfully", "success")
            return redirect(url_for(".sessions"))
        
        except IntegrityError:
            db.session.rollback()
            flash(
                (
                    "Database error occurred."
                    "Please check your inputs and try again."
                ), 
                "danger"
            )
        
        except Exception:
            db.session.rollback()
            flash(
                (
                    "An unexpected error occured."
                    "Please contact support if the issue persists."
                ), 
                "danger"
            )

    return render_template("add_session.html", form=form)

@bp.route("/sessions/client-price")
@login_required
def client_price():
    if not request.headers.get("HX-Request"):
        abort(404)
    client_id = request.args.get("client", type=int)

    form = AddSessionForm()
    if not client_id:
        form.price.data = 0
        return render_template("helpers/_price_field.html", form=form)
    
    client = Client.query.filter_by(
        id=client_id,
        trainer_id=current_user.id
    ).first_or_404()
    form.price.data = client.price or 0
    return render_template("helpers/_price_field.html", form=form)

@bp.route("/clients", methods=["GET", "POST"])
@login_required
def clients():
    stmt = select(Client).where(Client.trainer_id == current_user.id)
    clients = db.session.execute(stmt).scalars().all()
    return render_template("clients.html", clients=clients)

@bp.route("/clients/add", methods=["GET", "POST"])
@login_required
def add_client():
    form = AddClientForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        price = form.price.data
        contact = form.contact.data.strip() if form.contact.data else None
        notes = form.notes.data.strip() if form.notes.data else None
        status = form.status.data
        new_client = Client(
            name=name,
            price=price,
            contact=contact,
            notes=notes,
            status=status,
            trainer_id=current_user.id
        )
        db.session.add(new_client)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            form.name.errors.append("A client with this name already exists.")
        
        flash("Client added successfully", "success")
        return redirect(url_for(".clients"))
    
    return render_template("add_client.html", form=form)

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