"""Kayıt / giriş / çıkış akış testleri."""
from app.models import User


def test_register_creates_user(client, db):
    """Geçerli form gönderildiğinde kullanıcı oluşmalı."""
    resp = client.post(
        "/auth/register",
        data={
            "username": "yeni",
            "email": "yeni@test.com",
            "password": "abc123",
            "confirm": "abc123",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    user = db.session.scalar(db.select(User).where(User.email == "yeni@test.com"))
    assert user is not None
    assert user.password_hash != "abc123"


def test_register_duplicate_email_rejected(client, db):
    """Aynı e-posta ile ikinci kayıt reddedilmeli."""
    u = User(username="ali", email="ali@test.com")
    u.set_password("x")
    db.session.add(u)
    db.session.commit()

    resp = client.post(
        "/auth/register",
        data={
            "username": "ali2",
            "email": "ali@test.com",
            "password": "yyy123",
            "confirm": "yyy123",
        },
    )
    assert resp.status_code == 200
    assert "zaten kayıtlı".encode("utf-8") in resp.data


def test_login_success_and_logout(client, db):
    """Doğru şifre ile giriş, sonra çıkış."""
    u = User(username="veli", email="veli@test.com")
    u.set_password("sifre1")
    db.session.add(u)
    db.session.commit()

    resp = client.post(
        "/auth/login",
        data={"email": "veli@test.com", "password": "sifre1"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "Hoş geldin".encode("utf-8") in resp.data

    resp = client.get("/auth/logout", follow_redirects=True)
    assert resp.status_code == 200


def test_login_wrong_password(client, db):
    """Yanlış şifre — flash mesaj göstermeli."""
    u = User(username="ayse", email="ayse@test.com")
    u.set_password("dogru")
    db.session.add(u)
    db.session.commit()

    resp = client.post(
        "/auth/login",
        data={"email": "ayse@test.com", "password": "yanlis"},
        follow_redirects=True,
    )
    assert "hatalı".encode("utf-8") in resp.data


def test_protected_page_redirects_when_anonymous(client):
    """login_required sayfalar anonim kullanıcıyı login'e yönlendirmeli."""
    resp = client.get("/ilan/yeni", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers["Location"]
