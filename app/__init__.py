"""Application factory."""
from __future__ import annotations
import os
from flask import Flask, request, session
from config import config_by_name
from app.extensions import db, migrate, login_manager, mail, babel


def _select_locale():
    # 1) Kullanıcı oturumda dil seçtiyse onu kullan
    if "lang" in session and session["lang"] in ("tr", "en"):
        return session["lang"]
    # 2) Tarayıcı tercihinden
    return request.accept_languages.best_match(["tr", "en"]) or "tr"


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    # Yükleme klasörlerini garanti et
    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "avatars"), exist_ok=True)
    os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], "listings"), exist_ok=True)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    babel.init_app(app, locale_selector=_select_locale)

    # Flask-Login user loader
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    # Blueprints
    from app.main import bp as main_bp
    from app.auth import bp as auth_bp
    from app.listings import bp as listings_bp
    from app.messages import bp as messages_bp
    from app.api import bp as api_bp
    from app.admin import bp as admin_bp
    from app.errors import bp as errors_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(listings_bp, url_prefix="/ilan")
    app.register_blueprint(messages_bp, url_prefix="/mesaj")
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(errors_bp)

    # CLI komutları (flask seed)
    from app.cli import register_cli
    register_cli(app)

    # Şablonlara global yardımcılar
    from app.models import Category

    @app.context_processor
    def inject_globals():
        return {
            "all_categories": Category.query.order_by(Category.name).all() if _has_table("category") else [],
            "current_lang": session.get("lang", "tr"),
        }

    def _has_table(name: str) -> bool:
        # Migrasyon öncesi context_processor patlamasın
        try:
            return db.session.execute(
                db.text("SELECT 1 FROM information_schema.tables WHERE table_name = :n")
                if not app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite")
                else db.text("SELECT name FROM sqlite_master WHERE type='table' AND name=:n"),
                {"n": name},
            ).first() is not None
        except Exception:
            return False

    return app
