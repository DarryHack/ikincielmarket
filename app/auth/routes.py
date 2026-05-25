from __future__ import annotations
import os
import secrets
from pathlib import Path
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image

from app.auth import bp
from app.auth.forms import (
    LoginForm, RegisterForm, RequestResetForm, ResetPasswordForm, EditProfileForm
)
from app.models import User, Listing
from app.extensions import db
from app.email import send_password_reset_email


def _allowed_image(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def _save_avatar(file_storage) -> str | None:
    if not file_storage or not file_storage.filename:
        return None
    if not _allowed_image(file_storage.filename):
        raise ValueError("Geçersiz görsel formatı.")
    ext = file_storage.filename.rsplit(".", 1)[-1].lower()
    name = f"{secrets.token_hex(8)}.{ext}"
    folder = Path(current_app.config["UPLOAD_FOLDER"]) / "avatars"
    folder.mkdir(parents=True, exist_ok=True)
    full = folder / name
    # Pillow ile küçült (256x256 max)
    img = Image.open(file_storage.stream)
    img.thumbnail((256, 256))
    img.save(full)
    return name


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Hesabın oluşturuldu, şimdi giriş yapabilirsin.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form, title="Kayıt ol")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.email == form.email.data.lower()))
        if user is None or not user.check_password(form.password.data):
            flash("E-posta veya şifre hatalı.", "danger")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember.data)
        flash(f"Hoş geldin, {user.username}!", "success")
        next_page = request.args.get("next")
        if not next_page or not next_page.startswith("/"):
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html", form=form, title="Giriş")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Çıkış yaptın.", "info")
    return redirect(url_for("main.index"))


@bp.route("/reset-password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.email == form.email.data.lower()))
        if user:
            send_password_reset_email(user)
        flash("E-posta varsa sıfırlama linki gönderildi. Gelen kutunu kontrol et.", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_request.html", form=form, title="Şifre sıfırla")


@bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_reset_token(token)
    if not user:
        flash("Token geçersiz veya süresi dolmuş.", "danger")
        return redirect(url_for("auth.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Şifren güncellendi, giriş yapabilirsin.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form, title="Yeni şifre")


@bp.route("/profil/<username>")
def profile(username):
    user = db.first_or_404(db.select(User).where(User.username == username))
    page = request.args.get("page", 1, type=int)
    listings = db.paginate(
        db.select(Listing).where(Listing.user_id == user.id).order_by(Listing.created_at.desc()),
        page=page,
        per_page=current_app.config["LISTINGS_PER_PAGE"],
        error_out=False,
    )
    return render_template("auth/profile.html", user=user, listings=listings, title=user.username)


@bp.route("/profil/duzenle", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(original_username=current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        avatar_file = request.files.get("avatar")
        if avatar_file and avatar_file.filename:
            try:
                old = current_user.avatar
                current_user.avatar = _save_avatar(avatar_file)
                if old:
                    old_path = Path(current_app.config["UPLOAD_FOLDER"]) / "avatars" / old
                    if old_path.exists():
                        old_path.unlink()
            except ValueError as e:
                flash(str(e), "danger")
                return redirect(url_for("auth.edit_profile"))
        db.session.commit()
        flash("Profil güncellendi.", "success")
        return redirect(url_for("auth.profile", username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.bio.data = current_user.bio
    return render_template("auth/edit_profile.html", form=form, title="Profili düzenle")
