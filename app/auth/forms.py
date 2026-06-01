from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp

from app.models import User
from app.extensions import db


class LoginForm(FlaskForm):
    # Email validator login formunda yok — DB lookup zaten geçersiz e-postayı
    # "E-posta veya şifre hatalı" mesajıyla yakalar; ayrıca .local gibi TLD'leri
    # email-validator paketi reddediyor, demo hesapları için sorun çıkıyordu.
    email = StringField("E-posta", validators=[DataRequired()])
    password = PasswordField("Şifre", validators=[DataRequired()])
    remember = BooleanField("Beni hatırla")
    submit = SubmitField("Giriş yap")


class RegisterForm(FlaskForm):
    username = StringField(
        "Kullanıcı adı",
        validators=[
            DataRequired(),
            Length(min=3, max=64),
            Regexp(r"^[A-Za-z0-9_.-]+$", message="Sadece harf, rakam, . _ - kullanılabilir."),
        ],
    )
    email = StringField("E-posta", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Şifre", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField(
        "Şifre (tekrar)",
        validators=[DataRequired(), EqualTo("password", message="Şifreler eşleşmiyor.")],
    )
    submit = SubmitField("Kayıt ol")

    def validate_username(self, field):
        if db.session.scalar(db.select(User).where(User.username == field.data)):
            raise ValidationError("Bu kullanıcı adı kullanımda.")

    def validate_email(self, field):
        if db.session.scalar(db.select(User).where(User.email == field.data.lower())):
            raise ValidationError("Bu e-posta zaten kayıtlı.")


class RequestResetForm(FlaskForm):
    email = StringField("E-posta", validators=[DataRequired(), Email()])
    submit = SubmitField("Sıfırlama linki gönder")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Yeni şifre", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField(
        "Yeni şifre (tekrar)",
        validators=[DataRequired(), EqualTo("password", message="Şifreler eşleşmiyor.")],
    )
    submit = SubmitField("Şifremi güncelle")


class EditProfileForm(FlaskForm):
    username = StringField(
        "Kullanıcı adı",
        validators=[DataRequired(), Length(min=3, max=64), Regexp(r"^[A-Za-z0-9_.-]+$")],
    )
    bio = TextAreaField("Hakkımda", validators=[Length(max=500)])
    submit = SubmitField("Güncelle")

    def __init__(self, original_username: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, field):
        if field.data != self.original_username:
            if db.session.scalar(db.select(User).where(User.username == field.data)):
                raise ValidationError("Bu kullanıcı adı kullanımda.")
