"""E-posta gönderim yardımcısı (Flask-Mail)."""
from __future__ import annotations
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app.extensions import mail


def _send_async(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as exc:  # pragma: no cover
            app.logger.warning("Mail gönderilemedi: %s", exc)


def send_email(subject: str, recipients: list[str], text_body: str, html_body: str | None = None) -> None:
    """E-postayı arka planda gönderir; SMTP yapılandırılmamışsa sessizce loglar."""
    app = current_app._get_current_object()
    msg = Message(subject, recipients=recipients, sender=app.config.get("MAIL_DEFAULT_SENDER"))
    msg.body = text_body
    if html_body:
        msg.html = html_body
    Thread(target=_send_async, args=(app, msg)).start()


def send_password_reset_email(user) -> None:
    token = user.generate_reset_token()
    send_email(
        subject="[İkinciElMarket] Şifre sıfırlama",
        recipients=[user.email],
        text_body=render_template("auth/email/reset_password.txt", user=user, token=token),
        html_body=render_template("auth/email/reset_password.html", user=user, token=token),
    )
