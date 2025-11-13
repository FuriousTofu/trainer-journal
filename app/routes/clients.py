from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Client
from app.forms import AddClientForm

from . import bp


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
            form.name.errors.append(
                "A client with this name already exists."
            )
            return render_template("add_client.html", form=form)

        flash("Client added successfully", "success")
        return redirect(url_for(".clients"))

    return render_template("add_client.html", form=form)
