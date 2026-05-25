from flask import Blueprint

bp = Blueprint("messages", __name__, template_folder="../templates/messages")

from app.messages import routes  # noqa: E402,F401
