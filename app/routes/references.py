from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy import select

from app import db
from app.models import Exercise, Tag

from . import bp


@bp.route("/references")
@bp.route("/references/<tab>")
@login_required
def references(tab="exercises"):
    if tab not in ("exercises", "tags"):
        tab = "exercises"

    stmt_exercises = select(Exercise).where(
        Exercise.trainer_id == current_user.id,
        Exercise.is_active.is_(True)
    ).order_by(Exercise.name)
    exercises = db.session.execute(stmt_exercises).scalars().all()

    stmt_tags = select(Tag).where(
        Tag.trainer_id == current_user.id
    ).order_by(Tag.name)
    tags = db.session.execute(stmt_tags).scalars().all()

    return render_template(
        "references/references.html",
        exercises=exercises,
        tags=tags,
        active_tab=tab,
    )
