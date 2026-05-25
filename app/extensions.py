"""Eklentiler tek yerde — döngüsel import'tan kaçınmak için."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
babel = Babel()

login_manager.login_view = "auth.login"
login_manager.login_message = "Bu sayfayı görmek için giriş yapmalısın."
login_manager.login_message_category = "warning"
