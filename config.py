"""Uygulama yapılandırması — tüm hassas değerler ortam değişkenlerinden."""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _normalize_db_url(url: str) -> str:
    # Render/Heroku eski "postgres://" ön ekini SQLAlchemy 2.x için düzelt
    if url and url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")

    SQLALCHEMY_DATABASE_URI = _normalize_db_url(
        os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'ikincielmarket.db'}")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Yükleme
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))
    UPLOAD_FOLDER = str(BASE_DIR / "app" / "static" / "uploads")
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    # Mail
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 25))
    MAIL_USE_TLS = bool(int(os.environ.get("MAIL_USE_TLS", "0")))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@ikincielmarket.local")

    # Babel — çok dil
    LANGUAGES = ["tr", "en"]
    BABEL_DEFAULT_LOCALE = "tr"
    BABEL_DEFAULT_TIMEZONE = "Europe/Istanbul"

    # Sayfalama
    LISTINGS_PER_PAGE = 12
    MESSAGES_PER_PAGE = 20

    # Admin seed
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@ikincielmarket.local")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin1234")


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
