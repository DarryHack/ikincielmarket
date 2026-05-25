from flask import render_template
from app.errors import bp
from app.extensions import db


@bp.app_errorhandler(404)
def not_found(error):
    return render_template("errors/404.html", title="Sayfa bulunamadı"), 404


@bp.app_errorhandler(403)
def forbidden(error):
    return render_template("errors/403.html", title="Yetki yok"), 403


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("errors/500.html", title="Sunucu hatası"), 500


@bp.app_errorhandler(413)
def request_too_large(error):
    return render_template("errors/413.html", title="Dosya çok büyük"), 413
