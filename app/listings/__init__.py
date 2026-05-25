from flask import Blueprint

bp = Blueprint("listings", __name__, template_folder="../templates/listings")

from app.listings import routes  # noqa: E402,F401
