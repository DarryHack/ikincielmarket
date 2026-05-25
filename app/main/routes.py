from flask import render_template, request, current_app, redirect, url_for, session, abort
from sqlalchemy import or_

from app.main import bp
from app.models import Listing, Category
from app.extensions import db


@bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    q = (request.args.get("q") or "").strip()
    category_slug = request.args.get("kategori")

    stmt = db.select(Listing).where(Listing.status == "active")

    if category_slug:
        cat = db.session.scalar(db.select(Category).where(Category.slug == category_slug))
        if cat is None:
            abort(404)
        stmt = stmt.where(Listing.category_id == cat.id)

    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Listing.title.ilike(like), Listing.description.ilike(like)))

    stmt = stmt.order_by(Listing.created_at.desc())

    pagination = db.paginate(
        stmt,
        page=page,
        per_page=current_app.config["LISTINGS_PER_PAGE"],
        error_out=False,
    )
    return render_template(
        "main/index.html",
        listings=pagination,
        q=q,
        category_slug=category_slug,
        title="Anasayfa",
    )


@bp.route("/hakkimizda")
def about():
    return render_template("main/about.html", title="Hakkımızda")


@bp.route("/dil/<lang>")
def set_language(lang):
    if lang in current_app.config["LANGUAGES"]:
        session["lang"] = lang
    return redirect(request.referrer or url_for("main.index"))
