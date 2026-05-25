"""Basit JSON API — /api/v1/* (bonus)."""
from flask import jsonify, request, current_app, abort
from sqlalchemy import or_

from app.api import bp
from app.models import Listing, Category
from app.extensions import db


def _listing_dict(l: Listing) -> dict:
    return {
        "id": l.id,
        "title": l.title,
        "description": l.description,
        "price": float(l.price),
        "image_url": l.image_url(),
        "location": l.location,
        "status": l.status,
        "created_at": l.created_at.isoformat(),
        "seller": {"id": l.seller.id, "username": l.seller.username},
        "category": {"id": l.category.id, "name": l.category.name, "slug": l.category.slug},
    }


@bp.get("/listings")
def list_listings():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 12, type=int), 50)
    q = (request.args.get("q") or "").strip()
    category_slug = request.args.get("category")

    stmt = db.select(Listing).where(Listing.status == "active")
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Listing.title.ilike(like), Listing.description.ilike(like)))
    if category_slug:
        cat = db.session.scalar(db.select(Category).where(Category.slug == category_slug))
        if cat is None:
            return jsonify({"error": "category not found"}), 404
        stmt = stmt.where(Listing.category_id == cat.id)

    stmt = stmt.order_by(Listing.created_at.desc())
    pagination = db.paginate(stmt, page=page, per_page=per_page, error_out=False)
    return jsonify(
        {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "items": [_listing_dict(l) for l in pagination.items],
        }
    )


@bp.get("/listings/<int:listing_id>")
def get_listing(listing_id):
    listing = db.get_or_404(Listing, listing_id)
    return jsonify(_listing_dict(listing))


@bp.get("/categories")
def list_categories():
    cats = db.session.scalars(db.select(Category).order_by(Category.name)).all()
    return jsonify([{"id": c.id, "name": c.name, "slug": c.slug} for c in cats])
