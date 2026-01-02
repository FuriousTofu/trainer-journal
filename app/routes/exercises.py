from flask import abort, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import exists, func, select
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Exercise, SessionExercise
from app.forms import AddExerciseForm, EditExerciseForm

from . import bp


@bp.route("/exercises", methods=["GET", "POST"])
@login_required
def exercises():
    stmt = select(Exercise).where(
        Exercise.trainer_id == current_user.id,
        Exercise.is_active.is_(True)
    ).order_by(Exercise.name)
    exercises = db.session.execute(stmt).scalars().all()

    return render_template("exercises/exercises.html", exercises=exercises)


@bp.route("/exercises/archived", methods=["GET"])
@login_required
def archived_exercises():
    stmt = select(Exercise).where(
        Exercise.trainer_id == current_user.id,
        Exercise.is_active.is_(False)
    ).order_by(Exercise.name)
    exercises = db.session.execute(stmt).scalars().all()

    return render_template("exercises/archived_exercises.html", exercises=exercises)


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
    )
    exercise = db.session.execute(stmt).scalars().first()

    if not exercise:
        abort(404)

    exercise_used = _exercise_used_in_sessions(exercise.id)
    
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
    return render_template(
        "exercises/exercise.html", exercise=exercise,
        form=form, exercise_used=exercise_used
    )


@bp.route("/exercises/<int:exercise_id>/archive", methods=["POST"])
@login_required
def archive_exercise(exercise_id):
    stmt = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.trainer_id == current_user.id,
        Exercise.is_active.is_(True)
    )
    exercise = db.session.execute(stmt).scalars().first()

    if not exercise:
        abort(404)

    exercise.is_active = False

    try:
        db.session.commit()
        flash("Exercise archived successfully", "success")
    except Exception:
        db.session.rollback()
        flash("Error archiving exercise. Please try again.", "danger")

    return redirect(url_for(".exercise", exercise_id=exercise.id))


@bp.route("/exercises/<int:exercise_id>/unarchive", methods=["POST"])
@login_required
def unarchive_exercise(exercise_id):
    stmt = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.trainer_id == current_user.id,
        Exercise.is_active.is_(False)
    )
    exercise = db.session.execute(stmt).scalars().first()

    if not exercise:
        abort(404)

    exercise.is_active = True

    try:
        db.session.commit()
        flash("Exercise unarchived successfully", "success")
    except Exception:
        db.session.rollback()
        flash("Error unarchiving exercise. Please try again.", "danger")

    return redirect(url_for(".exercise", exercise_id=exercise.id))


@bp.route("/exercises/<int:exercise_id>/delete", methods=["POST"])
@login_required
def delete_exercise(exercise_id):
    stmt = select(Exercise).where(
        Exercise.id == exercise_id,
        Exercise.trainer_id == current_user.id
    )
    exercise = db.session.execute(stmt).scalars().first()

    if not exercise:
        abort(404)

    if _exercise_used_in_sessions(exercise.id):
        flash("Exercise used in sessions cannot be deleted. Archive it instead.", "danger")
        return redirect(url_for(".exercise", exercise_id=exercise.id))

    db.session.delete(exercise)

    try:
        db.session.commit()
        flash("Exercise deleted successfully", "success")
    except Exception:
        db.session.rollback()
        flash("Error deleting exercise. Please try again.", "danger")

    return redirect(url_for(".exercises"))


def _exercise_used_in_sessions(exercise_id: int) -> bool:
    stmt = select(
        exists().where(SessionExercise.exercise_id == exercise_id)
    )
    return bool(db.session.scalar(stmt))
