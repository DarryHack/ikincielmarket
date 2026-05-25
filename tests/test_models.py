"""User modeli üzerine birim testler."""
from app.models import User


def test_password_is_hashed_not_plain(app, db):
    """Şifre HASH'lenmiş olmalı, düz metin asla saklanmamalı."""
    u = User(username="ali", email="ali@test.com")
    u.set_password("gizli123")
    db.session.add(u)
    db.session.commit()

    assert u.password_hash != "gizli123"
    assert len(u.password_hash) > 20


def test_check_password_works(app, db):
    """check_password doğru/yanlış şifreyi ayırt etmeli."""
    u = User(username="veli", email="veli@test.com")
    u.set_password("dogru123")
    db.session.add(u)
    db.session.commit()

    assert u.check_password("dogru123") is True
    assert u.check_password("yanlis") is False


def test_reset_token_roundtrip(app, db):
    """Şifre sıfırlama token'ı oluşturulup doğrulanabilmeli."""
    u = User(username="ayse", email="ayse@test.com")
    u.set_password("x")
    db.session.add(u)
    db.session.commit()

    token = u.generate_reset_token()
    recovered = User.verify_reset_token(token)
    assert recovered is not None
    assert recovered.id == u.id


def test_invalid_token_returns_none(app, db):
    """Bozuk token None döndürmeli."""
    assert User.verify_reset_token("bogus.token.value") is None
