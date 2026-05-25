"""Basit admin paneli — sadece is_admin=True kullanıcılar için."""
from functools import wraps
from flask import render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

from app.admin import bp
from app.models import User, Listing, Category, Message
from app.extensions import db


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapper


class CategoryForm(FlaskForm):
    name = StringField("Ad", validators=[DataRequired(), Length(min=2, max=64)])
    slug = StringField(
        "Slug",
        validators=[DataRequired(), Length(min=2, max=64), Regexp(r"^[a-z0-9-]+$", message="Sadece küçük harf, rakam ve - kullan.")],
    )
    submit = SubmitField("Kaydet")


class EmptyForm(FlaskForm):
    submit = SubmitField("Onayla")


@bp.route("/")
@admin_required
def dashboard():
    stats = {
        "users": db.session.scalar(db.select(db.func.count(User.id))),
        "listings": db.session.scalar(db.select(db.func.count(Listing.id))),
        "categories": db.session.scalar(db.select(db.func.count(Category.id))),
        "messages": db.session.scalar(db.select(db.func.count(Message.id))),
    }
    return render_template("admin/dashboard.html", stats=stats, title="Yönetim")


@bp.route("/kullanicilar")
@admin_required
def users():
    page = request.args.get("page", 1, type=int)
    pagination = db.paginate(
        db.select(User).order_by(User.created_at.desc()),
        page=page,
        per_page=20,
        error_out=False,
    )
    return render_template("admin/users.html", users=pagination, title="Kullanıcılar", form=EmptyForm())


@bp.route("/kullanicilar/<int:user_id>/admin-toggle", methods=["POST"])
@admin_required
def toggle_admin(user_id):
    user = db.get_or_404(User, user_id)
    if user.id == current_user.id:
        flash("Kendi admin yetkini kaldıramazsın.", "warning")
        return redirect(url_for("admin.users"))
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f"{user.username} → admin={'evet' if user.is_admin else 'hayır'}", "success")
    return redirect(url_for("admin.users"))


@bp.route("/ilanlar")
@admin_required
def listings():
    page = request.args.get("page", 1, type=int)
    pagination = db.paginate(
        db.select(Listing).order_by(Listing.created_at.desc()),
        page=page,
        per_page=20,
        error_out=False,
    )
    return render_template("admin/listings.html", listings=pagination, title="Tüm ilanlar", form=EmptyForm())


@bp.route("/ilanlar/<int:listing_id>/sil", methods=["POST"])
@admin_required
def delete_listing(listing_id):
    listing = db.get_or_404(Listing, listing_id)
    db.session.delete(listing)
    db.session.commit()
    flash("İlan silindi.", "info")
    return redirect(url_for("admin.listings"))


@bp.route("/kategoriler", methods=["GET", "POST"])
@admin_required
def categories():
    form = CategoryForm()
    if form.validate_on_submit():
        if db.session.scalar(db.select(Category).where(Category.slug == form.slug.data)):
            flash("Bu slug zaten kullanılıyor.", "danger")
        else:
            db.session.add(Category(name=form.name.data, slug=form.slug.data))
            db.session.commit()
            flash("Kategori eklendi.", "success")
        return redirect(url_for("admin.categories"))
    cats = db.session.scalars(db.select(Category).order_by(Category.name)).all()
    return render_template("admin/categories.html", form=form, categories=cats, title="Kategoriler", delete_form=EmptyForm())


@bp.route("/kategoriler/<int:category_id>/sil", methods=["POST"])
@admin_required
def delete_category(category_id):
    cat = db.get_or_404(Category, category_id)
    # İlan varsa engelle
    has_listings = db.session.scalar(db.select(db.func.count(Listing.id)).where(Listing.category_id == cat.id))
    if has_listings:
        flash("Bu kategoride ilan var, silinemez.", "warning")
        return redirect(url_for("admin.categories"))
    db.session.delete(cat)
    db.session.commit()
    flash("Kategori silindi.", "info")
    return redirect(url_for("admin.categories"))
