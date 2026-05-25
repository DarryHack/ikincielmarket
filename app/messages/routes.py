from flask import render_template, redirect, url_for, flash, abort, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_, and_, func

from app.messages import bp
from app.messages.forms import MessageForm
from app.models import Message, User, Listing
from app.extensions import db


@bp.route("/")
@login_required
def inbox():
    # Karşı tarafa göre son mesajları grupla — basit sürüm
    # SQLite/PG uyumlu: kullanıcının dahil olduğu tüm mesajları çek, Python'da grupla
    msgs = db.session.scalars(
        db.select(Message)
        .where(or_(Message.sender_id == current_user.id, Message.receiver_id == current_user.id))
        .order_by(Message.created_at.desc())
    ).all()
    threads = {}
    for m in msgs:
        other_id = m.receiver_id if m.sender_id == current_user.id else m.sender_id
        key = (other_id, m.listing_id)
        if key not in threads:
            threads[key] = {
                "other": db.session.get(User, other_id),
                "listing": db.session.get(Listing, m.listing_id) if m.listing_id else None,
                "last": m,
                "unread": 0,
            }
        if m.receiver_id == current_user.id and not m.is_read:
            threads[key]["unread"] += 1
    return render_template("messages/inbox.html", threads=list(threads.values()), title="Gelen kutusu")


@bp.route("/sohbet/<int:other_id>", defaults={"listing_id": None}, methods=["GET", "POST"])
@bp.route("/sohbet/<int:other_id>/<int:listing_id>", methods=["GET", "POST"])
@login_required
def thread(other_id, listing_id):
    other = db.get_or_404(User, other_id)
    if other.id == current_user.id:
        abort(400)
    listing = db.session.get(Listing, listing_id) if listing_id else None

    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(
            sender_id=current_user.id,
            receiver_id=other.id,
            listing_id=listing.id if listing else None,
            body=form.body.data,
        )
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for("messages.thread", other_id=other.id, listing_id=listing.id if listing else None))

    # Okunmamışları okundu yap
    db.session.execute(
        db.update(Message)
        .where(
            and_(
                Message.receiver_id == current_user.id,
                Message.sender_id == other.id,
                Message.is_read.is_(False),
            )
        )
        .values(is_read=True)
    )
    db.session.commit()

    stmt = (
        db.select(Message)
        .where(
            or_(
                and_(Message.sender_id == current_user.id, Message.receiver_id == other.id),
                and_(Message.sender_id == other.id, Message.receiver_id == current_user.id),
            )
        )
        .order_by(Message.created_at.asc())
    )
    if listing:
        stmt = stmt.where(or_(Message.listing_id == listing.id, Message.listing_id.is_(None)))

    messages = db.session.scalars(stmt).all()
    return render_template(
        "messages/thread.html",
        other=other,
        listing=listing,
        messages=messages,
        form=form,
        title=f"Sohbet — {other.username}",
    )


@bp.route("/ilan/<int:listing_id>/yazdir", methods=["GET"])
@login_required
def start_from_listing(listing_id):
    listing = db.get_or_404(Listing, listing_id)
    if listing.user_id == current_user.id:
        flash("Kendi ilanına mesaj atamazsın.", "warning")
        return redirect(url_for("listings.detail", listing_id=listing.id))
    return redirect(url_for("messages.thread", other_id=listing.user_id, listing_id=listing.id))
