from datetime import datetime, timezone
from flask import abort, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import exists, func, select
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Client, Session
from app.forms import AddClientForm

from . import bp


@bp.route("/clients", methods=["GET"])
@login_required
def clients():
    stmt = select(Client).where(
        Client.trainer_id == current_user.id,
        Client.archived_at == None)
    clients = db.session.execute(stmt).scalars().all()
    return render_template("clients/clients.html", clients=clients)


@bp.route("/clients/archive", methods=["GET"])
@login_required
def archived_clients():
    last_dt = func.max(Session.start_dt).label("last_session_dt")

    stmt = (
        select(Client, last_dt)
        .outerjoin(Session, Session.client_id == Client.id)
        .where(
            Client.trainer_id == current_user.id,
            Client.archived_at != None
        )
        .group_by(Client.id)
        .order_by(Client.name)
    )

    rows = db.session.execute(stmt).all()
    clients = []
    for client, last_session_dt in rows:
        client.last_session_dt = last_session_dt
        clients.append(client)
    return render_template("clients/archived_clients.html", clients=clients)


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
            form.name.errors.append(
                "A client with this name already exists."
            )
            return render_template("clients/add_client.html", form=form)

        flash("Client added successfully", "success")
        return redirect(url_for(".clients"))

    return render_template("clients/add_client.html", form=form)


@bp.route("/clients/<string:client_public_id>", methods=["GET", "POST"])
@login_required
def client(client_public_id):
    stmt = select(Client).where(
        Client.public_id == client_public_id,
        Client.trainer_id == current_user.id
    )
    client = db.session.execute(stmt).scalars().first()

    if not client:
        abort(404)
        
    if request.method == "POST" and client.archived_at:
        abort(403)

    stmt = (
        select(Session)
        .where(
            Session.client.has(trainer_id=current_user.id),
            Session.client.has(id=client.id)
        )
        .order_by(Session.start_dt)
    )
    sessions = db.session.execute(stmt).scalars().all()

    form = AddClientForm(obj=client)
    if form.validate_on_submit():
        form.populate_obj(client)
        try:
            db.session.commit()
            flash("Client updated successfully", "success")
        except Exception:
            db.session.rollback()
            flash("Error updating client. Please try again.", "danger")
            return render_template("clients/client.html")

        return redirect(url_for(".client", client_public_id=client.public_id))

    return render_template(
        "clients/client.html",
        client=client,
        form=form,
        sessions=sessions
    )

@bp.route("/clients/<string:client_public_id>/archive", methods=["POST"])
@login_required
def archive_client(client_public_id):
    stmt = select(Client).where(
        Client.public_id == client_public_id,
        Client.trainer_id == current_user.id,
        Client.archived_at.is_(None)
    )
    client = db.session.execute(stmt).scalars().first()

    if not client:
        abort(404)

    planned_session = db.session.scalar(
        select(
            exists().where(
                Session.client_id == client.id,
                Session.status == "planned"
            )
        )
    )

    if planned_session:
        flash("Сlient with planned sessions cannot be archived.", "danger")
        return redirect(url_for(".client", client_public_id=client.public_id))

    client.archived_at = datetime.now(timezone.utc)
    try:
        db.session.commit()
        flash("Client archived successfully", "success")
    except Exception:
        db.session.rollback()
        flash("Error archiving client. Please try again.", "danger")

    return redirect(url_for(".client", client_public_id=client.public_id))


@bp.route("/clients/<string:client_public_id>/unarchive", methods=["POST"])
@login_required
def unarchive_client(client_public_id):
    stmt = select(Client).where(
        Client.public_id == client_public_id,
        Client.trainer_id == current_user.id,
        Client.archived_at.isnot(None)
    )
    client = db.session.execute(stmt).scalars().first()

    if not client:
        abort(404)

    client.archived_at = None
    try:
        db.session.commit()
        flash("Client unarchived successfully", "success")
    except Exception:
        db.session.rollback()
        flash("Error unarchiving client. Please try again.", "danger")

    return redirect(url_for(".client", client_public_id=client.public_id))


@bp.route("/clients/<string:client_public_id>/delete", methods=["POST"])
@login_required
def delete_client(client_public_id):
    stmt = select(Client).where(
        Client.public_id == client_public_id,
        Client.trainer_id == current_user.id
    )
    client = db.session.execute(stmt).scalars().first()

    if not client:
        abort(404)

    planned_session = db.session.scalar(
        select(
            exists().where(
                Session.client_id == client.id,
                Session.status == "planned"
            )
        )
    )

    if planned_session:
        flash("Сlient with planned sessions cannot be deleted.", "danger")
        return redirect(url_for(".client", client_public_id=client.public_id))

    db.session.delete(client)
    try:
        db.session.commit()
        flash("Client deleted successfully", "success")
    except Exception:
        db.session.rollback()
        flash("Error deleting client. Please try again.", "danger")

    return redirect(url_for(".clients"))