from flask import Blueprint

bp = Blueprint("main", __name__)

from . import user, sessions, exercises, clients, tags, static_routes  # noqa: F401,E402
