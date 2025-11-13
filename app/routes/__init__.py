from flask import Blueprint

bp = Blueprint("main", __name__)

from . import user, sessions, exercises, clients  # noqa: F401,E402
