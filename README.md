# İkinciElMarket

[![CI](https://github.com/DarryHack/ikincielmarket/actions/workflows/ci.yml/badge.svg)](https://github.com/DarryHack/ikincielmarket/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-black)
![License](https://img.shields.io/badge/license-MIT-green)

Basit bir ikinci el alım-satım platformu. Flask 3 + SQLAlchemy 2 + Bootstrap 5.

Gazi Üniversitesi TUSAŞ Kazan MYO — **BLG106 İnternet Programcılığı** dersi dönem projesi.

## Özellikler

| Alan | Var mı |
|------|--------|
| Application factory + 7 blueprint | ✅ |
| 5 model (User, Category, Listing, Favorite, Message) | ✅ |
| Kayıt / giriş / çıkış (Flask-Login + hash'li şifre) | ✅ |
| Şifre sıfırlama (e-posta + zaman damgalı token) | ✅ |
| İlan CRUD + görsel yükleme (Pillow ile küçültme) | ✅ |
| Kategori filtreleme + arama (LIKE) | ✅ |
| Favoriler | ✅ |
| Alıcı-satıcı mesajlaşma | ✅ |
| Profil sayfası + avatar | ✅ |
| JSON API `/api/v1/...` | ✅ |
| Admin paneli (kullanıcı/ilan/kategori yönetimi) | ✅ |
| Türkçe + İngilizce arayüz (Flask-Babel) | ✅ |
| 404 / 403 / 500 / 413 özel hata sayfaları | ✅ |
| Pagination | ✅ |
| Pytest birim + entegrasyon testleri | ✅ |
| Docker + docker-compose (PostgreSQL) | ✅ |
| Render/Railway için Procfile | ✅ |

## Hızlı Başlangıç

**Canlı demo:** https://swing-duncan-customize-transportation.trycloudflare.com

```bash
# 1. Klonla
git clone https://github.com/DarryHack/ikincielmarket.git
cd ikincielmarket

# 2. Sanal ortam
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Bağımlılıklar
pip install -r requirements.txt

# 4. .env oluştur
cp .env.example .env
# .env içindeki SECRET_KEY'i değiştir!

# 5. Veritabanı
flask db upgrade            # tabloları oluştur
flask seed                  # kategoriler + admin (admin@... / admin1234)

# 6. Çalıştır
flask run
# http://localhost:5000
```

## Geliştirme Komutları

| Komut | Ne yapar |
|------|----------|
| `flask run` | Geliştirme sunucusu |
| `flask db migrate -m "msg"` | Yeni migration üret |
| `flask db upgrade` | Migration'ları uygula |
| `flask seed` | Kategori + admin seed |
| `pytest` | Testleri çalıştır |
| `pybabel extract -F babel.cfg -o messages.pot .` | Çeviri stringlerini topla |
| `pybabel update -i messages.pot -d app/translations` | Mevcut çevirileri güncelle |
| `pybabel compile -d app/translations` | .po → .mo derle |

## Docker ile Çalıştırma

```bash
docker-compose up --build
# http://localhost:5000  — PostgreSQL ile birlikte
```

İlk kez çalıştırırken:
```bash
docker-compose exec web flask seed
```

## Klasör Yapısı

```
ikincielmarket/
├── app/
│   ├── __init__.py            # Application factory
│   ├── extensions.py          # db, login_manager, mail, babel
│   ├── models.py              # SQLAlchemy 2.x modeller
│   ├── cli.py                 # flask seed komutu
│   ├── email.py               # async mail helper
│   ├── auth/                  # kayıt/giriş/profil/şifre sıfırlama
│   ├── main/                  # anasayfa + arama + dil
│   ├── listings/              # ilan CRUD + favoriler
│   ├── messages/              # alıcı-satıcı mesajlaşma
│   ├── api/                   # JSON API /api/v1/*
│   ├── admin/                 # admin paneli
│   ├── errors/                # 404/403/500/413
│   ├── templates/             # Jinja2 + Bootstrap 5
│   ├── static/                # css/img/uploads
│   └── translations/          # tr/en (Babel)
├── migrations/                # Alembic
├── tests/                     # pytest
├── docs/
│   ├── ai-gunlugu.md          # AI ajan oturum kayıtları
│   └── rapor.md               # Proje raporu
├── config.py
├── run.py
├── requirements.txt
├── Dockerfile + docker-compose.yml
├── Procfile + runtime.txt     # Render/Railway için
└── README.md
```

## Demo Video

🎬 **YouTube:** https://youtu.be/VHOwLuhkBYw

4:46 dk ekran kaydı — kayıt + giriş + ilan oluşturma + arama + favori + mesajlaşma + dil
değişimi + admin paneli akışları. Senaryo: `docs/demo-senaryosu.md`. Canlı URL'de seed-demo
verisi (3 kullanıcı + 8 ilan + 1 favori + 1 mesaj thread) önceden yüklü.

**Müzik:** "Inspired" — Kevin MacLeod (incompetech.com), Creative Commons BY 4.0 lisansı.

## Ekran Görüntüleri

19 otomatik üretilmiş ekran görüntüsü `docs/img/` altında — anonim/kullanıcı/admin/EN/mobil
varyantları dahil. Üretim script'i: `scripts/take_screenshots.py` (Playwright headless).
İlişkili oturumların eşleştirmesi için bkz. `docs/ai-gunlugu.md` → **Ek A**.

## Kullanılan Teknolojiler

- **Backend:** Flask 3, SQLAlchemy 2 (Mapped/mapped_column), Flask-Migrate, Flask-Login, Flask-WTF, Flask-Mail, Flask-Babel
- **Frontend:** Bootstrap 5, Bootstrap Icons, Jinja2
- **Veritabanı:** SQLite (dev) / PostgreSQL (prod)
- **Test:** pytest + pytest-flask
- **Görsel:** Pillow (otomatik küçültme)
- **Deploy:** gunicorn, Docker, Render/Railway

## Güvenlik

- Şifreler `werkzeug.security.generate_password_hash` ile bcrypt-benzeri hash'lenir
- Tüm formlarda Flask-WTF CSRF koruması aktif
- `SECRET_KEY`, mail şifresi vb. `.env` üzerinden, `.gitignore`'da
- ORM kullanılır, raw SQL yok (SQL injection riski yok)
- `login_required` + sahiplik kontrolü ilan düzenleme/silmede
- Yüklenen dosyalar uzantı + Pillow doğrulamasından geçer, max 5MB
