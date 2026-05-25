"""İlan CRUD ve yetki kontrol testleri."""
from io import BytesIO
from app.models import User, Category, Listing


def _login(client, email, password):
    return client.post(
        "/auth/login", data={"email": email, "password": password}, follow_redirects=True
    )


def _seed_user(db, username="u", email="u@t.com", password="x"):
    u = User(username=username, email=email)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return u


def _seed_category(db, name="Elektronik", slug="elektronik"):
    c = Category(name=name, slug=slug)
    db.session.add(c)
    db.session.commit()
    return c


def test_anyone_can_view_index(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_create_listing_requires_login(client):
    resp = client.get("/ilan/yeni", follow_redirects=False)
    assert resp.status_code == 302


def test_owner_can_edit_others_cannot(app, client, db):
    """Sahip düzenleyebilir, başkası 403 almalı."""
    owner = _seed_user(db, "owner", "owner@t.com", "pw")
    other = _seed_user(db, "other", "other@t.com", "pw")
    cat = _seed_category(db)
    listing = Listing(
        title="Test", description="Aciklama", price=10, user_id=owner.id, category_id=cat.id
    )
    db.session.add(listing)
    db.session.commit()
    lid = listing.id

    # Owner: GET düzenleme sayfası 200
    _login(client, "owner@t.com", "pw")
    resp = client.get(f"/ilan/{lid}/duzenle")
    assert resp.status_code == 200

    # Başkası: 403
    client.get("/auth/logout")
    _login(client, "other@t.com", "pw")
    resp = client.get(f"/ilan/{lid}/duzenle")
    assert resp.status_code == 403


def test_api_listings_returns_json(app, client, db):
    cat = _seed_category(db)
    seller = _seed_user(db, "s", "s@t.com", "x")
    db.session.add(
        Listing(title="iPhone", description="lorem", price=5000, user_id=seller.id, category_id=cat.id)
    )
    db.session.commit()

    resp = client.get("/api/v1/listings")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 1
    assert data["items"][0]["title"] == "iPhone"
