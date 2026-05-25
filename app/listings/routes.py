from __future__ import annotations
import secrets
from pathlib import Path
from flask import render_template, redirect, url_for, flash, abort, request, current_app
from flask_login import login_required, current_user
from PIL import Image

from app.listings import bp
from app.listings.forms import ListingForm, DeleteListingForm
from app.models import Listing, Category, Favorite
from app.extensions import db


def _save_listing_image(file_storage) -> str | None:
    if not file_storage or not file_storage.filename:
        return None
    ext = file_storage.filename.rsplit(".", 1)[-1].lower()
    if ext not in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        raise ValueError("Geçersiz görsel formatı.")
    name = f"{secrets.token_hex(8)}.{ext}"
    folder = Path(current_app.config["UPLOAD_FOLDER"]) / "listings"
    folder.mkdir(parents=True, exist_ok=True)
    img = Image.open(file_storage.stream)
    img.thumbnail((1280, 1280))
    img.save(folder / name)
    return name


def _populate_categories(form: ListingForm) -> None:
    form.category_id.choices = [
        (c.id, c.name) for c in db.session.scalars(db.select(Category).order_by(Category.name))
    ]


@bp.route("/yeni", methods=["GET", "POST"])
@login_required
def create():
    form = ListingForm()
    _populate_categories(form)
    if form.validate_on_submit():
        try:
            image_name = _save_listing_image(form.image.data)
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("listings.create"))
        listing = Listing(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            location=form.location.data or None,
            category_id=form.category_id.data,
            user_id=current_user.id,
            image=image_name,
        )
        db.session.add(listing)
        db.session.commit()
        flash("İlanın yayınlandı.", "success")
        return redirect(url_for("listings.detail", listing_id=listing.id))
    return render_template("listings/form.html", form=form, title="Yeni İlan", mode="create")


@bp.route("/<int:listing_id>")
def detail(listing_id):
    listing = db.get_or_404(Listing, listing_id)
    is_owner = current_user.is_authenticated and current_user.id == listing.user_id
    favorited = current_user.is_authenticated and current_user.has_favorited(listing.id)
    return render_template(
        "listings/detail.html",
        listing=listing,
        is_owner=is_owner,
        favorited=favorited,
        title=listing.title,
    )


@bp.route("/<int:listing_id>/duzenle", methods=["GET", "POST"])
@login_required
def edit(listing_id):
    listing = db.get_or_404(Listing, listing_id)
    if listing.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    form = ListingForm(obj=listing)
    _populate_categories(form)
    if form.validate_on_submit():
        if form.image.data and form.image.data.filename:
            try:
                old = listing.image
                listing.image = _save_listing_image(form.image.data)
                if old:
                    old_path = Path(current_app.config["UPLOAD_FOLDER"]) / "listings" / old
                    if old_path.exists():
                        old_path.unlink()
            except ValueError as e:
                flash(str(e), "danger")
                return redirect(url_for("listings.edit", listing_id=listing.id))
        listing.title = form.title.data
        listing.description = form.description.data
        listing.price = form.price.data
        listing.location = form.location.data or None
        listing.category_id = form.category_id.data
        db.session.commit()
        flash("İlan güncellendi.", "success")
        return redirect(url_for("listings.detail", listing_id=listing.id))
    return render_template("listings/form.html", form=form, title="İlanı düzenle", mode="edit", listing=listing)


@bp.route("/<int:listing_id>/sil", methods=["GET", "POST"])
@login_required
def delete(listing_id):
    listing = db.get_or_404(Listing, listing_id)
    if listing.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    form = DeleteListingForm()
    if form.validate_on_submit():
        if listing.image:
            p = Path(current_app.config["UPLOAD_FOLDER"]) / "listings" / listing.image
            if p.exists():
                p.unlink()
        db.session.delete(listing)
        db.session.commit()
        flash("İlan silindi.", "info")
        return redirect(url_for("main.index"))
    return render_template("listings/delete_confirm.html", listing=listing, form=form, title="Silme onayı")


@bp.route("/<int:listing_id>/favori", methods=["POST"])
@login_required
def toggle_favorite(listing_id):
    listing = db.get_or_404(Listing, listing_id)
    fav = db.session.scalar(
        db.select(Favorite).where(
            (Favorite.user_id == current_user.id) & (Favorite.listing_id == listing.id)
        )
    )
    if fav:
        db.session.delete(fav)
        msg = "Favorilerden çıkarıldı."
    else:
        db.session.add(Favorite(user_id=current_user.id, listing_id=listing.id))
        msg = "Favorilere eklendi."
    db.session.commit()
    flash(msg, "info")
    return redirect(request.referrer or url_for("listings.detail", listing_id=listing.id))


@bp.route("/favorilerim")
@login_required
def my_favorites():
    page = request.args.get("page", 1, type=int)
    stmt = (
        db.select(Listing)
        .join(Favorite, Favorite.listing_id == Listing.id)
        .where(Favorite.user_id == current_user.id)
        .order_by(Favorite.created_at.desc())
    )
    pagination = db.paginate(
        stmt, page=page, per_page=current_app.config["LISTINGS_PER_PAGE"], error_out=False
    )
    return render_template("listings/favorites.html", listings=pagination, title="Favorilerim")
