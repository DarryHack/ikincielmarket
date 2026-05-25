# Güvenlik Politikası

## Desteklenen Sürümler

Bu bir öğrenci projesi; tek aktif sürüm `main` branch'idir.

## Güvenlik Açığı Bildirme

Bir güvenlik açığı bulduysan **lütfen public issue AÇMA**. Bunun yerine:

- E-posta: gorkem.poyrazoglu5541@gmail.com
- Konu: "[İkinciElMarket Güvenlik] kısa açıklama"
- Mümkünse PoC (proof of concept) ekle.

48 saat içinde geri dönüş yapılır.

## Uygulamadaki Güvenlik Önlemleri

| Tehdit | Önlem |
|--------|-------|
| Şifre çalınması | werkzeug `pbkdf2:sha256` ile hash, salt ile |
| CSRF | Flask-WTF tüm formlarda otomatik token, `form.hidden_tag()` |
| SQL Injection | SQLAlchemy ORM, parametre bağlama (raw SQL yok) |
| Yetkisiz erişim | `@login_required` + sahiplik kontrolü route bazında |
| XSS | Jinja2 default autoescape; `{{ user_input }}` her zaman escape'lenir |
| Session hijacking | `SECRET_KEY` ortam değişkeninde, repo'da değil |
| Dosya yükleme istismarı | Pillow ile validate + uzantı whitelist + 5MB limit |
| Şifre sıfırlama tokeni istismarı | itsdangerous URLSafeTimedSerializer, 30 dk geçerli, HMAC imzalı |
| Admin yetki yükseltme | `is_admin` toggle sadece mevcut admin yapabilir, kendi yetkisini düşüremez |

## Bilinen Sınırlamalar (Düşük Riskli)

- Yüklenen görseller container restart'ında uçar (yerel disk). Production'da
  S3/R2 önerilir.
- Mail göndericisi `Thread` ile async; başarısız olursa sadece loglanır,
  kullanıcı bilgilendirilmez (kullanıcı sayımını ifşa etmemek için bilinçli karar).
- Rate limiting yok — production'da Flask-Limiter eklenmeli.
- HTTP/HTTPS zorlaması uygulamada yok; reverse proxy seviyesinde (Render/nginx) yapılır.

## Üçüncü Taraf Bağımlılıklar

Tüm sürümler `requirements.txt`'te pin'li. Güncelleme öncesi:

```bash
pip list --outdated
pip install --upgrade <paket>
pytest                # kırılma kontrolü
```

CVE taraması için (öneri):
```bash
pip install pip-audit
pip-audit -r requirements.txt
```
