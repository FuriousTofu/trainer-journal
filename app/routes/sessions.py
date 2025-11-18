from flask import (
    render_template, request, redirect,
    url_for, flash, abort,
)
from flask_login import login_required, current_user
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import (
    Client, Session,
    Exercise, SessionExercise,
)
from app.forms import (
    AddSessionForm, AddSessionHelperForm,
)

from . import bp


@bp.route("/sessions", methods=["GET", "POST"])
@login_required
def sessions():
    stmt = (
        select(Session)
        .where(Session.client.has(trainer_id=current_user.id))
        .order_by(Session.start_dt)
    )
    sessions = db.session.execute(stmt).scalars().all()
    return render_template("sessions/sessions.html", sessions=sessions)


@bp.route("/sessions/add", methods=["GET", "POST"])
@login_required
def add_session():
    form = AddSessionForm()

    form.client.render_kw = {
        "hx-get": url_for(".client_price"),
        "hx-target": "#price-wrapper",
        "hx-trigger": "change",
        "hx-swap": "outerHTML"
    }  # God bless HTMX

    clients = db.session.execute(
        select(Client.id, Client.name)
        .where(
            Client.trainer_id == current_user.id,
            Client.status == "active"
        )
        .order_by(Client.name)
    ).all()
    form.client.choices = [(0, "Select Client")] + [
        (c.id, c.name) for c in clients
    ]
    has_clients = len(form.client.choices) > 1

    exercises = db.session.execute(
        select(Exercise.id, Exercise.name)
        .where(
            Exercise.trainer_id == current_user.id,
            Exercise.is_active == True
        )
        .order_by(Exercise.name)
    ).all()
    exercise_choices = [(0, "Select Exercise")] + [
        (e.id, e.name) for e in exercises
    ]
    has_exercises = len(exercise_choices) > 1

    if request.method == "GET" and not form.exercises:
        form.exercises.append_entry()

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
                notes=form.notes.data.strip()
                if form.notes.data
                else None,
            )
            db.session.add(s)
            db.session.flush()  # to use s.id below

            for exercise_form in form.exercises:
                sub = exercise_form.form

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

    return render_template(
        "sessions/add_session.html",
        form=form,
        has_clients=has_clients,
        has_exercises=has_exercises
    )


@bp.route("/sessions/add_exercise_row")
@login_required
def exercise_row():
    if not request.headers.get("HX-Request"):
        abort(404)

    form = AddSessionForm(formdata=request.args)
    subform = form.exercises.append_entry()

    exercises = db.session.execute(
        select(Exercise.id, Exercise.name)
        .where(Exercise.trainer_id == current_user.id)
        .order_by(Exercise.name)
    ).all()
    exercise_choices = [(0, "Select Exercise")] + [
        (e.id, e.name) for e in exercises
    ]
    subform.exercise.choices = exercise_choices

    return render_template("helpers/_exercise_row.html", subform=subform)


@bp.route("/sessions/remove_exercise_row", methods=["POST"])
@login_required
def remove_exercise_row():
    if not request.headers.get("HX-Request"):
        abort(404)

    remove_index_raw = request.form.get("remove_index")
    if remove_index_raw is None:
        abort(400)
    try:
        remove_index = int(remove_index_raw)
    except ValueError:
        abort(400)

    orig_form = AddSessionForm(formdata=request.form)
    new_form = AddSessionHelperForm()

    if not (0 <= remove_index < len(orig_form.exercises)):
        abort(400)

    for i, sub in enumerate(orig_form.exercises):
        if i == remove_index:
            continue
        new_sub = new_form.exercises.append_entry()
        new_sub.form.exercise.data = sub.form.exercise.data
        new_sub.form.sets.data = sub.form.sets.data
        new_sub.form.reps.data = sub.form.reps.data
        new_sub.form.weight.data = sub.form.weight.data

    exercises = db.session.execute(
        select(Exercise.id, Exercise.name)
        .where(Exercise.trainer_id == current_user.id)
        .order_by(Exercise.name)
    ).all()
    exercise_choices = [(0, "Select Exercise")] + [
        (e.id, e.name) for e in exercises
    ]
    for sub in new_form.exercises:
        sub.form.exercise.choices = exercise_choices

    return render_template("helpers/_exercise_rows.html", form=new_form)


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
