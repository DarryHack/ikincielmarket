# Deploy Rehberi

İki seçenek: **Cloudflared Quick Tunnel** (hesap yok, anında, geçici) veya
**Render.com** (kalıcı, free tier).

## Seçenek 1: Cloudflared Quick Tunnel (en hızlı, hesap yok)

```bash
# 1. Cloudflared (zaten kuruluysa atla)
brew install cloudflared
# veya: https://github.com/cloudflare/cloudflared/releases

# 2. Flask'ı yerelde başlat
cd ~/Desktop/ikincielmarket
source venv/bin/activate
flask seed && flask seed-demo
nohup flask run --port 5050 > /tmp/flask.log 2>&1 &

# 3. Quick Tunnel aç
cloudflared tunnel --url http://localhost:5050
# Çıktıda: https://random-words.trycloudflare.com
# Bu URL'i README'ye ve docs/rapor.md'ye ekle, push'la.
```

Sınır: makine kapanırsa veya cloudflared process biterse URL ölür. Demo süresi için yeterli.

## Seçenek 2: Render.com (ücretsiz, kalıcı)

Render'ın free tier'ı bu proje için yeterli (uyku moduna geçer, ilk istekte ~30 sn
uyanır — demo için sorun değil).

## Tek Tıkla Deploy (Önerilen)

Repo'da `render.yaml` var, bu Render'ın "Blueprint" formatı. Adımlar:

1. https://render.com → **Sign Up** (GitHub ile gir — onaylar).
2. Dashboard → **New +** → **Blueprint**.
3. **Connect a repository** → `DarryHack/ikincielmarket` seç → **Connect**.
4. Render `render.yaml`'i okur ve **iki kaynak** görürsün:
   - `ikincielmarket` (Web Service)
   - `ikincielmarket-db` (PostgreSQL)
5. **ADMIN_PASSWORD** alanı boş — elle bir şifre yaz (örn. `admin1234` — sonra değiştir).
6. **Apply** → Render build başlatır (~5-8 dk):
   - `pip install -r requirements.txt`
   - `pybabel compile -d app/translations`
   - `flask db upgrade` (tablolar oluşur)
   - `flask seed` (kategoriler + admin)
   - `flask seed-demo` (8 örnek ilan + 3 demo kullanıcı)
   - `gunicorn run:app` (uygulama açılır)
7. Yeşil "Live" rozetini görünce: **URL: https://ikincielmarket.onrender.com** (veya
   benzeri otomatik subdomain).

## URL'i README'ye Ekle

Build başarılı olduğunda Render sana bir URL verir. README.md'de bul:

```markdown
**Canlı demo:** [Buraya Render/Railway URL ekle]
```

Bunu gerçek URL ile değiştir:

```markdown
**Canlı demo:** https://ikincielmarket-XXXX.onrender.com
```

Sonra:

```bash
git add README.md docs/rapor.md
git commit -m "docs: canlı URL eklendi"
git push
```

## Manuel Deploy (Eğer Blueprint Çalışmazsa)

1. Render → New + → **PostgreSQL** → ad: `ikincielmarket-db`, plan: Free → Create.
2. Veritabanı oluştuğunda **Internal Database URL**'i kopyala.
3. Render → New + → **Web Service** → GitHub repo bağla → `ikincielmarket`.
4. Ayarlar:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt && pybabel compile -d app/translations`
   - **Pre-Deploy Command:** `flask db upgrade && flask seed && flask seed-demo`
   - **Start Command:** `gunicorn run:app`
5. **Environment Variables:**
   | Key | Value |
   |-----|-------|
   | `PYTHON_VERSION` | `3.12.4` |
   | `FLASK_APP` | `run.py` |
   | `FLASK_CONFIG` | `production` |
   | `SECRET_KEY` | (Generate butonu) |
   | `DATABASE_URL` | (yukarıda kopyaladığın) |
   | `ADMIN_EMAIL` | `admin@ikincielmarket.local` |
   | `ADMIN_PASSWORD` | (kendi şifren) |
6. **Create Web Service** → bekle → URL'i kopyala.

## Sorun Giderme

- **Build fail: `flask seed` AttributeError hashlib.scrypt:**  
  Bu macOS sorunuydu, Linux Python 3.12'de yok. Eğer çıkarsa
  `requirements.txt`'te Werkzeug versiyonunu pin'le.

- **`flask db upgrade` "no such command":**  
  `FLASK_APP=run.py` env var'ı tanımlı mı kontrol et.

- **404 static dosyalar:**  
  `app/static/uploads/listings/` boş — `seed-demo` koyduğu SVG'ler var mı bak.
  Render container restart'ında uploads kaybolur; production'da S3/R2 öneriyoruz
  (rapor 7. madde).

- **i18n çevirileri görünmüyor:**  
  Build'de `pybabel compile` çalıştı mı kontrol et. `app/translations/*/LC_MESSAGES/messages.mo`
  dosyaları olmalı.

## Alternatif: Docker Compose (yerel)

Render açmak istemiyorsan tamamen yerel test:

```bash
docker compose up --build
# http://localhost:5000
# İlk açılışta:
docker compose exec web flask seed
docker compose exec web flask seed-demo
```

PostgreSQL + Flask birlikte ayağa kalkar. Veriler `pgdata` volume'unda kalıcı.
