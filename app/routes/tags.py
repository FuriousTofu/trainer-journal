from flask import abort, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import exists, func, select
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Tag
from app.forms import AddTagForm, EditTagForm

from . import bp


@bp.route("/tags", methods=["GET"])
@login_required
def tags():
    return redirect(url_for(".references", tab="tags"))


@bp.route("/tags/add", methods=["GET", "POST"])
@login_required
def add_tag():
    form = AddTagForm()
    if form.validate_on_submit():

        name = " ".join(form.name.data.split())

        dup_stmt = select(
            exists().where(
                Tag.trainer_id == current_user.id,
                func.lower(Tag.name) == name.lower()
            )
        )
        tag_exists = db.session.execute(dup_stmt).scalar()

        if tag_exists:
            form.name.errors.append(
                "A tag with this name already exists."
            )

        else:
            new_tag = Tag(
                name=name,
                color=form.color.data,
                trainer_id=current_user.id
            )
            try:
                db.session.add(new_tag)
                db.session.commit()
                flash("Tag added successfully", "success")
                return redirect(url_for(".add_tag"))
            except IntegrityError:
                db.session.rollback()
                form.name.errors.append(
                    "A tag with this name already exists."
                )

    return render_template("tags/add_tag.html", form=form)


@bp.route("/tags/<int:tag_id>", methods=["GET", "POST"])
@login_required
def tag(tag_id):
    stmt = select(Tag).where(
        Tag.id == tag_id,
        Tag.trainer_id == current_user.id,
    )
    tag = db.session.execute(stmt).scalars().first()

    if not tag:
        abort(404)

    form = EditTagForm(obj=tag)
    if form.validate_on_submit():
        name = " ".join(form.name.data.split())

        dup_stmt = select(
            exists().where(
                Tag.trainer_id == current_user.id,
                func.lower(Tag.name) == name.lower(),
                Tag.id != tag.id
            )
        )
        tag_exists = db.session.execute(dup_stmt).scalar()

        if tag_exists:
            form.name.errors.append(
                "A tag with this name already exists."
            )

        else:
            tag.name = name
            tag.color = form.color.data

            try:
                db.session.commit()
                flash("Tag updated successfully", "success")
                return redirect(url_for(".tag", tag_id=tag.id))
            except IntegrityError:
                db.session.rollback()
                form.name.errors.append(
                    "A tag with this name already exists."
                )

    return render_template("tags/tag.html", tag=tag, form=form)


@bp.route("/tags/<int:tag_id>/delete", methods=["POST"])
@login_required
def delete_tag(tag_id):
    stmt = select(Tag).where(
        Tag.id == tag_id,
        Tag.trainer_id == current_user.id
    )
    tag = db.session.execute(stmt).scalars().first()

    if not tag:
        abort(404)

    db.session.delete(tag)

    try:
        db.session.commit()
        flash("Tag deleted successfully", "success")
    except Exception:
        db.session.rollback()
        flash("Error deleting tag. Please try again.", "danger")

    return redirect(url_for(".tags"))
