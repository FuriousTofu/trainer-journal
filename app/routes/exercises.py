from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Exercise
from app.forms import AddExerciseForm

from . import bp


@bp.route("/exercises", methods=["GET", "POST"])
@login_required
def exercises():
    stmt = select(Exercise).where(Exercise.trainer_id == current_user.id)
    exercises = db.session.execute(stmt).scalars().all()
    return render_template("exercises/exercises.html", exercises=exercises)


@bp.route("/exercises/add", methods=["GET", "POST"])
@login_required
def add_exercise():
    form = AddExerciseForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        description = (
            form.description.data.strip()
            if form.description.data
            else None
        )
        new_exercise = Exercise(
            name=name,
            description=description,
            trainer_id=current_user.id
        )

        try:
            db.session.add(new_exercise)
            db.session.commit()
            flash("Exercise added successfully", "success")
            return redirect(url_for(".add_exercise"))
        except IntegrityError:
            db.session.rollback()
            form.name.errors.append(
                "An exercise with this name already exists."
            )

    return render_template("exercises/add_exercise.html", form=form)
