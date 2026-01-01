from flask import abort, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import exists, func, select
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Exercise
from app.forms import AddExerciseForm, EditExerciseForm

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

        # Normalize spaces
        name = " ".join(form.name.data.split())
        description = (
            form.description.data.strip()
            if form.description.data
            else None
        )

        dup_stmt = select(
            exists().where(
                Exercise.trainer_id == current_user.id,
                func.lower(Exercise.name) == name.lower()
            )
        )
        exercise_exists = db.session.execute(dup_stmt).scalar()

        if exercise_exists:
            form.name.errors.append(
                "An exercise with this name already exists."
            )

        else:
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


@bp.route("/exercises/<int:exercise_id>", methods=["GET", "POST"])
@login_required
def exercise(exercise_id):
    stmt = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.trainer_id == current_user.id,
        Exercise.is_active.is_(True)
    )
    exercise = db.session.execute(stmt).scalars().first()

    if not exercise:
        abort(404)
    
    form = EditExerciseForm(obj=exercise)
    if form.validate_on_submit():
        name = " ".join(form.name.data.split())
        description = (
            form.description.data.strip()
            if form.description.data
            else None
        )

        dup_stmt = select(
            exists().where(
                Exercise.trainer_id == current_user.id,
                func.lower(Exercise.name) == name.lower(),
                Exercise.id != exercise.id
            )
        )
        exercise_exists = db.session.execute(dup_stmt).scalar()

        if exercise_exists:
            form.name.errors.append(
                "An exercise with this name already exists."
            )

        else:
            exercise.name = name
            exercise.description = description
            try:
                db.session.commit()
                flash("Exercise updated successfully", "success")
                return redirect(
                    url_for(".exercise", exercise_id=exercise.id)
                )
            except IntegrityError:
                db.session.rollback()
                form.name.errors.append(
                    "An exercise with this name already exists."
                )
    return render_template("exercises/exercise.html", exercise=exercise, form=form)