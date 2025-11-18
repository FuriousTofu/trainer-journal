from nanoid import generate
from sqlalchemy import select

from app.constants import (
    PUBLIC_ID_SIZE_CLIENT,
    PUBLIC_ID_SIZE_SESSION,
    MAX_PUBLIC_ID_RETRIES
)


def _generate_unique(model, size):
    from app import db
    for _ in range(MAX_PUBLIC_ID_RETRIES):
        candidate = generate(size=size)
        exists = db.session.execute(
            select(model).where(model.public_id == candidate)
        ).scalar_one_or_none()
        if not exists:
            return candidate
    raise ValueError("Failed to generate a public ID.")


def generate_client_public_id():
    from app.models import Client
    return _generate_unique(Client, PUBLIC_ID_SIZE_CLIENT)


def generate_session_public_id():
    from app.models import Session
    return _generate_unique(Session, PUBLIC_ID_SIZE_SESSION)