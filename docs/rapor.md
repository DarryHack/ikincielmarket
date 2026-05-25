# Proje Raporu — İkinciElMarket

**Öğrenci:** Görkem Poyrazoğlu  
**Ders:** BLG106 — İnternet Programcılığı  
**Kurum:** Gazi Üniversitesi — TUSAŞ Kazan Meslek Yüksek Okulu  
**Teslim Tarihi:** 01/06/2026  
**Repo:** https://github.com/DarryHack/ikincielmarket  
**Canlı URL:** [Render bağlantısı — deploy sonrası buraya yapıştır]

---

## 1. Projenin Amacı ve Ne İşe Yaradığı

İkinciElMarket, kullanıcıların elindeki ürünleri başlık, açıklama, fiyat, görsel
ve kategori bilgileriyle ilanlayabildiği; başkalarının ilanlarını arayıp
filtreleyebildiği; favorilerine ekleyip satıcıyla mesajlaşarak alışveriş
yapabildiği bir ikinci el platformudur. Sahibinden.com / Letgo benzeri sitelerin
küçük ama tam işlevli bir kopyasıdır. Kullanıcı kayıt olur, profilini avatarıyla
düzenler, ilan açar, başkalarının ilanlarını gezinir, satıcılara mesaj atar,
ilgilendiği ilanları favoriler. Yönetici hesabı kullanıcı/ilan/kategori yönetimi
yapabilir. Tüm arayüz Türkçe ve İngilizce olarak iki dilde sunulur. Bunun
üzerine bir JSON API ve şifre sıfırlama akışı eklenmiştir.

Bu proje seçilmesinin nedeni, Flask Mega-Tutorial'da öğretilen tüm temel
yapıtaşlarını (auth, ORM ve ilişkiler, formlar, blueprint, hata yönetimi,
dağıtım, çok dil) tek bir gerçekçi senaryo etrafında birleştirme isteğiydi.
Marketplace senaryosu kullanıcıların aşina olduğu bir konu olduğu için kullanıcı
hikayelerini tasarlamak kolaylaştı; bu da Plan modunda ajana net niyet
bildirmemi sağladı.

---

## 2. Mimari Özet

### Klasör Yapısı

```
ikincielmarket/
├── app/
│   ├── __init__.py            # Application factory (create_app)
│   ├── extensions.py          # db, login_manager, mail, babel singletons
│   ├── models.py              # 5 SQLAlchemy 2.x modeli
│   ├── cli.py                 # `flask seed` komutu
│   ├── email.py               # async mail helper
│   ├── auth/                  # kayıt, giriş, çıkış, profil, şifre sıfırlama
│   ├── main/                  # anasayfa, arama (LIKE), kategori filtre, dil
│   ├── listings/              # ilan CRUD, görsel yükleme, favori toggle
│   ├── messages/              # alıcı-satıcı sohbet
│   ├── api/                   # JSON API /api/v1/*
│   ├── admin/                 # admin paneli (kullanıcı/ilan/kategori yönetimi)
│   ├── errors/                # 404, 403, 500, 413 handler'ları
│   ├── templates/             # Jinja2 + Bootstrap 5 (25 şablon, base + inheritance)
│   ├── static/                # css, img (SVG fallback), uploads/
│   └── translations/          # tr, en (Flask-Babel)
├── migrations/                # Alembic
├── tests/                     # 13 pytest test
├── docs/                      # ai-gunlugu.md, rapor.md
├── config.py                  # Development/Production/Testing
├── run.py                     # CLI giriş noktası
├── requirements.txt           # pinned versiyonlar
├── Dockerfile + docker-compose.yml
├── Procfile + runtime.txt + render.yaml
└── README.md
```

### Veritabanı İlişkileri

```
User (1) ─────< (N) Listing >───── (N) Category
   │                  │
   │                  │ (1)
   │                  ▼
   │              Message (N)
   │             /
   │  (1, N as sender or receiver)
   ▼
Favorite (N) >──── (N) Listing  [UniqueConstraint(user_id, listing_id)]
```

- `User → Listing`: 1-N (satıcı → ilanlar)
- `Category → Listing`: 1-N
- `User ↔ Listing` (Favorite üzerinden): N-N
- `User → Message` ve `User → Message`: 1-N (sender + receiver, iki ayrı FK)
- `Listing → Message`: 1-N (nullable; ilan dışı genel sohbet için)

### Ana Akışlar

1. **Anonim kullanıcı:** `/` → arama/kategori → ilan detay → "satıcıya mesaj
   at" → /auth/login'e yönlendirilir.
2. **Kayıtlı kullanıcı:** `/auth/register` → `/auth/login` → `/ilan/yeni`
   (görsel yükle, Pillow ile küçültülür) → ilan yayında.
3. **Alıcı:** ilan detay → favori toggle → satıcıya mesaj → `/mesaj/sohbet/<id>`
   thread'i açılır.
4. **Şifre unutma:** `/auth/reset-password` → e-posta (Flask-Mail, async) →
   `/auth/reset-password/<token>` (itsdangerous URLSafeTimedSerializer, 30dk geçerli).
5. **Admin:** `/admin/` → dashboard (4 sayaç) → kullanıcı/ilan/kategori CRUD.
6. **API tüketicisi:** `GET /api/v1/listings?q=...&category=...&page=...` → JSON.
7. **Dil değişimi:** navbar TR/EN dropdown → `/dil/<lang>` → session'a yazılır →
   Flask-Babel `_select_locale` ile her request'te belirlenir.

### Mimari Kararlar

| Karar | Neden |
|------|-------|
| Application factory | Test fixture'larında her test için fresh app + in-memory SQLite |
| Blueprint per domain (7 adet) | Auth, listings, messages vb. bağımsız evrilebilsin |
| SQLAlchemy 2.x `Mapped[...]` | IDE tip ipucu, autocomplete, PEP 484 uyumu |
| `pbkdf2:sha256` hash | macOS sistem Python'unda `hashlib.scrypt` yok |
| `itsdangerous` token (PyJWT yerine) | Flask ile geliyor, ek dependency yok |
| `extra={}` Jinja macro pattern | `**kwargs` Jinja'da desteklenmiyor |
| `psycopg2-binary` vs build-from-source | Geliştirme hızı için binary |
| Görselleri Pillow ile `thumbnail((1280,1280))` | Disk + bandwidth tasarrufu |
| Mesaj inbox'unda thread'leri Python tarafında grupla | SQLite + PG ikisinde de çalışsın |

---

## 3. Vibe Coding Deneyimi: Ne İşe Yaradı, Nerede Zorlandım?

**İşe yaradığı yerler:**
- **Plan modu büyük yapıları hızla iskeletledi.** "Auth blueprint'inin tamamını
  Plan'la" deyince ajan 5 dosyayı (forms, routes, 3 template) tek mantıksal
  birim olarak çıkardı; manuel yazsam yarım gün sürecek iş 10 dakikaya indi.
- **Tekrar eden boilerplate'i sıfıra indirdi.** Her CRUD rotasında benzer yetki
  kontrolleri, FlaskForm sınıfları, render_field macro'ları — bunları her seferinde
  manuel yazmak yerine "şu pattern'de bir CRUD yap" deyince çıkıyor.
- **Hata ayıklarken bağlam ekleyici olarak çok iyi.** "Şu hata mesajını verdim,
  olası nedenleri sırala" tipi prompt'larda 3 olası nedenden 2'sini tutturuyor.
  Üçüncüsü için kendim araştırıyorum.

**Zorlandığım yerler:**
- **Ajan Python sürümünü 3.12+ varsayıyor.** Ben Python 3.9.6 ile çalışıyordum.
  `str | None` PEP 604 syntax'ı, `list[str]` generic'leri sürekli runtime hatası
  verdi. Çözüm: prompt'a "Python 3.9 ile uyumlu" eklemeyi öğrendim, ama
  başlangıçta unuttum, sonradan üç dosyaya `from __future__ import annotations`
  ekledim.
- **Framework-spesifik sınırları yanılgıyla atlayabiliyor.** Jinja2 macro'da
  `**kwargs` yazdı (Python'da çalışır, Jinja'da çalışmaz). Werkzeug 3.0'ın
  default scrypt'i için macOS sistem Python'unda hashlib.scrypt yok diye
  düşünmedi. Bu tür sürpriz hataları sadece çalıştırınca yakaladım.
- **Üretilen kodun her satırı için "neden böyle?" sorgusu zaman alıyor.** Hızlı
  ilerlemek isterken bu soruyu atlama eğilimine girdim; özellikle template'ler
  gibi göz aşinası olduğum kodları daha az dikkatle okudum. Bunun sonraki
  refaktörlerde geri tepme riski var.

---

## 4. (Bende) En Faydalı Bulduğum 2 Özellik

Antigravity yerine Claude Code kullandığım için PDF'in "Antigravity'nin en
faydalı 2 özelliği" sorusunu **Claude Code üzerinden** cevaplıyorum. Eşdeğer
özelliklerin Antigravity karşılıkları parantez içinde:

1. **TodoWrite tool (≈ Antigravity Plan Artifact).** Sprint başında 23 maddelik
   todo listesi çıkardım; her madde tamamlandıkça ajan otomatik `in_progress`
   → `completed` olarak işaretledi. Süreç boyunca "nerede kaldık?" sorusunu
   sormam gerekmedi — liste cevap verdi. Plan'ı bozmadan ilerleyebilmenin
   psikolojik etkisi de büyük (boş işe sapmıyorsun).

2. **Sandbox terminal + paralel tool çağrıları (≈ Antigravity Manager view).**
   Tek bir mesajda 15+ dosyayı paralel olarak Write tool ile yazabildim; bir
   dosyayı yazarken paralel olarak `git log` ve `find` koşturup mevcut yapıyı
   görebildim. Bu paralellik özellikle 4. oturumda (25 HTML şablon yazma) on
   dakikada bitirmemi sağladı; sıralı yazsam yarım saatten fazla sürerdi.

---

## 5. Ajanın Yakalayıp Düzelttiğim En Kritik 3 Hata

1. **`import jwt as _jwt_optional` (Oturum 2 sonu).** Ajan `app/models.py`'nin
   tepesine ölü bir PyJWT import'u koymuştu; sonradan `itsdangerous`'a geçince
   silmeyi unutmuştu. `requirements.txt`'te `jwt` yoktu, bu yüzden ilk `flask
   db init` çağrısı `ModuleNotFoundError`'la patlardı. Plan modunda görünmüyordu;
   kodu satır satır okurken "bu import niye var?" diye sordum, ajan kaldırdı.

2. **Jinja2 macro'da `**kwargs` (Oturum 4 → Oturum 6'da yakalandı).** Ajan
   `render_pagination(pagination, endpoint, **kwargs)` yazmıştı. Python tarzı
   bir signature; Jinja2'de macro'lar `**kwargs` desteklemez. `pytest`
   çalıştırınca 6 test `TemplateSyntaxError: expected token 'name', got '**'`
   ile patladı. Düzeltme: `extra={}` dict parametresine geçtim, 3 dosyada
   call-site güncellettim. Bu, "Plan doğru görünüyor diye kod doğru değil;
   ya derleme ya da test şart" dersini somut verdi.

3. **`generate_password_hash(plain)` scrypt default'u (Oturum 6 orta).** Ajan
   Werkzeug'un default'una güvenmişti. Werkzeug 3.0 default'u scrypt, ama macOS
   ile gelen sistem Python'u (`/usr/bin/python3`) `hashlib.scrypt`'i içermiyor
   (OpenSSL bağımlılığı eksik). `flask seed` çağrısı `AttributeError`'la patladı.
   Çözüm: `generate_password_hash(plain, method="pbkdf2:sha256")` ile algoritmayı
   explicit yaptım. Yanına yorum bıraktım ki ileride başkası "neden scrypt değil?"
   diye sorduğunda cevabı görsün. Bu, "kütüphane default'larına güvenme,
   ortamına test et" dersini verdi.

---

## 6. Sıfırdan AI Olmadan Yapsaydım Ne Kadar Sürerdi?

Tahmini karşılaştırma:

| Modül | AI ile (gerçek) | AI olmadan (tahmin) |
|------|----------------:|--------------------:|
| İskelet + config + factory | 10 dk | 1-2 saat |
| 5 model + ilişkiler + migration | 8 dk | 3-4 saat (SQLAlchemy 2.x docs okumak dahil) |
| Auth (kayıt + giriş + reset) | 15 dk | 5-6 saat |
| 7 blueprint + 18 route | 20 dk | 8-10 saat |
| 25 HTML şablon | 10 dk (paralel) | 6-8 saat |
| Bootstrap responsive UI | (template ile birlikte) | 4-5 saat |
| 13 pytest test | 5 dk | 3-4 saat |
| i18n (TR/EN, 60 string) | 8 dk | 2-3 saat (.po dosyaları elle) |
| Docker + Procfile | 5 dk | 1-2 saat |
| 5 runtime hata debug | ~10 dk | 5-8 saat (StackOverflow + okuma) |
| **TOPLAM** | **~2 saat 30 dk** | **~40-55 saat** |

AI olmadan yaklaşık **20-25 katı zaman** alırdı. Bu hız avantajı ödünsüz
değildi: kodun her satırını ben yazmadığım için sözlü değerlendirmede
savunabilmek için günlüğü dolu tutmam ve kodu defalarca okumam gerekti.

---

## 7. Bu Projeyi Sürdürürsem Sonraki Adım Ne Olur?

Sıralı öncelikler:

1. **Tam metin arama → PostgreSQL `tsvector`.** Şu anki LIKE araması büyük
   veri setinde index'ten yararlanamaz. PostgreSQL'in `to_tsvector` ile
   GIN index'i, hem hızlı hem dil-bilinçli (Türkçe stem).
2. **WebSocket / SSE ile gerçek zamanlı mesajlaşma.** Şu anda her yeni mesaj
   için sayfa yenileme gerekiyor. Flask-SocketIO ile thread görünümünde
   anlık güncelleme eklemek demo'da çok etkili olurdu.
3. **JWT tabanlı `/api/v1/auth` endpoint'leri.** Şu anki API public (login
   gerektirmiyor); ilan oluşturma/silme API'leri için bearer token gerekecek.
4. **Görseller için S3 / Cloudflare R2.** `app/static/uploads/` yerel disk
   tutuyor; deploy edildiğinde container restart'ında uçar. Object storage
   şart.
5. **Sahibinden tarzı "rapor at" + moderasyon kuyruğu.** İçerik moderasyonu için
   admin'e flag'lenmiş ilan kuyruğu.
6. **CI/CD: GitHub Actions ile pytest + render auto-deploy.** Şu an testleri
   manuel çalıştırıyorum; PR açılınca otomatik test koşması iyi olur.
7. **Coverage raporu (pytest-cov) ve %80 hedef.** Şu anda 13 test var ama
   coverage ölçülmüyor; admin route'ları, error handler'lar test edilmemiş.
