"""JSON API endpoint testleri."""
from app.models import User, Category, Listing


def _seed(db):
    cat = Category(name="Elektronik", slug="elektronik")
    db.session.add(cat)
    u = User(username="s", email="s@t.com")
    u.set_password("x")
    db.session.add(u)
    db.session.commit()
    for i in range(3):
        db.session.add(Listing(
            title=f"Ürün {i}",
            description="lorem ipsum dolor",
            price=100 + i,
            user_id=u.id,
            category_id=cat.id,
        ))
    db.session.commit()
    return cat


def test_api_listings_pagination(client, db):
    _seed(db)
    resp = client.get("/api/v1/listings?per_page=2")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] == 3
    assert len(data["items"]) == 2
    assert data["pages"] == 2


def test_api_listings_search(client, db):
    _seed(db)
    resp = client.get("/api/v1/listings?q=Ürün+1")
    assert resp.status_code == 200
    items = resp.get_json()["items"]
    assert len(items) == 1
    assert "Ürün 1" in items[0]["title"]


def test_api_listings_category_filter(client, db):
    _seed(db)
    resp = client.get("/api/v1/listings?category=elektronik")
    assert resp.status_code == 200
    assert resp.get_json()["total"] == 3


def test_api_listings_unknown_category_404(client, db):
    _seed(db)
    resp = client.get("/api/v1/listings?category=yokboyle")
    assert resp.status_code == 404


def test_api_listing_detail(client, db):
    _seed(db)
    resp = client.get("/api/v1/listings/1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "title" in data
    assert "seller" in data
    assert "category" in data


def test_api_listing_detail_not_found(client, db):
    resp = client.get("/api/v1/listings/9999")
    assert resp.status_code == 404


def test_api_categories(client, db):
    _seed(db)
    resp = client.get("/api/v1/categories")
    assert resp.status_code == 200
    cats = resp.get_json()
    assert len(cats) >= 1
    assert cats[0]["slug"] == "elektronik"
