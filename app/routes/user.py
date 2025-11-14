from flask import render_template, redirect, url_for, flash
from flask_login import (
    login_user, logout_user,
    login_required, current_user,
)
from werkzeug.security import (
    generate_password_hash, check_password_hash,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Trainer
from app.forms import RegisterForm, LoginForm

from . import bp


@bp.route("/")
@login_required
def index():
    return render_template("user/main.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(".index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        stmt = select(Trainer).where(Trainer.email == email)
        trainer = db.session.execute(stmt).scalar_one_or_none()

        if (
            trainer
            and check_password_hash(trainer.password_hash, form.password.data)
        ):
            login_user(trainer, remember=form.remember_me.data)
            flash("Login successful", "success")
            return redirect(url_for(".index"))
        form.password.errors.append("Invalid email or password.")

    return render_template("user/login.html", form=form)


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

        new_trainer = Trainer(
            name=username,
            email=email,
            password_hash=password_hash
        )
        db.session.add(new_trainer)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            form.email.errors.append(
                "Email already registered. Please use a different email."
            )
            return render_template("user/register.html", form=form)

        login_user(new_trainer)
        flash("Registration successful", "success")
        return redirect(url_for(".index"))

    return render_template("user/register.html", form=form)
