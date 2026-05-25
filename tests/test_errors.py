"""Hata sayfaları + i18n route testleri."""


def test_404_returns_custom_page(client):
    resp = client.get("/yokboyle")
    assert resp.status_code == 404
    assert "404".encode() in resp.data


def test_language_switcher_persists(client):
    resp = client.get("/dil/en", follow_redirects=False)
    assert resp.status_code == 302
    with client.session_transaction() as sess:
        assert sess.get("lang") == "en"


def test_unknown_language_ignored(client):
    resp = client.get("/dil/xx", follow_redirects=False)
    assert resp.status_code == 302
    with client.session_transaction() as sess:
        assert sess.get("lang") != "xx"


def test_about_page_renders(client):
    resp = client.get("/hakkimizda")
    assert resp.status_code == 200
