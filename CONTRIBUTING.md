# Katkıda Bulunma Rehberi

İkinciElMarket'e katkıda bulunmak istediğin için teşekkürler. Bu rehber, kodun
genel kalitesini korumayı amaçlıyor.

## Geliştirme Ortamı

```bash
git clone https://github.com/DarryHack/ikincielmarket.git
cd ikincielmarket
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # SECRET_KEY'i değiştir
flask db upgrade
flask seed
flask seed-demo
flask run
```

## Testleri Çalıştırmak

```bash
pytest                       # tüm testler
pytest -v                    # detaylı
pytest --cov=app             # coverage raporu
pytest tests/test_auth.py    # tek dosya
```

## Pull Request Akışı

1. Fork → branch (`feat/yeni-ozellik` veya `fix/sorun-no`).
2. Değişikliğini yap, **mutlaka pytest geçsin**.
3. Yeni özellik için yeni test ekle (`tests/test_*.py`).
4. Commit mesajı [Conventional Commits](https://www.conventionalcommits.org/) formatında:
   - `feat:` yeni özellik
   - `fix:` hata düzeltmesi
   - `docs:` dokümantasyon
   - `test:` test ekleme/iyileştirme
   - `chore:` build, config, vs.
5. PR aç, başlığa kısa özet, gövdeye "ne", "neden", "test plan" yaz.

## Kod Standartları

- **Format:** PEP 8. Tab değil 4 boşluk.
- **Type hints:** Mümkün olduğunda kullan (`def foo(x: int) -> str:`).
- **Python 3.9+ uyumluluğu:** `str | None` yerine `Optional[str]` veya
  dosyanın tepesine `from __future__ import annotations`.
- **SQLAlchemy:** 2.x stili (`Mapped[...]`, `mapped_column`, `db.select(...)`).
- **Türkçe mesajlar:** flash, hata, e-posta için Türkçe. Kod yorumları için TR/EN
  serbest, ama tutarlı ol.
- **i18n:** UI string'lerini `{{ _("Metin") }}` ile sar; yeni string eklersen
  `pybabel extract && pybabel update && pybabel compile` çalıştır.

## Güvenlik

Güvenlik açığı bulduysan **public issue açma**.
`SECURITY.md` dosyasını oku ve oradaki yola gör.

## Ortam Değişkenleri

- `SECRET_KEY` — rastgele 32+ byte. Asla repo'ya koyma.
- `DATABASE_URL` — production'da PostgreSQL.
- `MAIL_*` — şifre sıfırlama için. Boşsa Flask uygulaması logla yetinir.
- `ADMIN_EMAIL` / `ADMIN_PASSWORD` — ilk `flask seed`'de oluşturulur.

## Çalıştırma & Migration

```bash
flask db migrate -m "açıklama"   # model değişikliği sonrası
flask db upgrade                  # migration'ı uygula
flask db downgrade                # bir önceki sürüme dön
```

## Klasör Mantığı

Yeni bir alan eklersen (örn. "yorum sistemi"):

1. `app/comments/` blueprint oluştur (`__init__.py`, `routes.py`, `forms.py`).
2. `app/templates/comments/` ekle.
3. `app/__init__.py`'de `register_blueprint` çağrısı.
4. Modeli `app/models.py`'a ekle (yeni dosya açma — tek yerde dursun).
5. Migration üret + uygula.
6. Test ekle (`tests/test_comments.py`).
