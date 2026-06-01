# Demo Videosu Senaryosu (3-5 dakika)

PDF "3-5 dk, uygulamanın temel akışını gösteren ekran kaydı" istiyor.
Aşağıdaki senaryo ~4 dakikalık akıcı bir tur sağlar.

## Hazırlık

1. **Canlı URL:** https://swing-duncan-customize-transportation.trycloudflare.com
   (Cloudflared Quick Tunnel, seed-demo otomatik yüklü: 8 ilan + 3 demo kullanıcı +
   1 favori + 1 mesaj thread). Yerel alternatif: http://localhost:5050.
2. **Kayıt aracı:**
   - macOS: QuickTime Player → File → New Screen Recording (Cmd+Shift+5)
   - Windows: OBS Studio (ücretsiz) veya Xbox Game Bar (Win+G)
3. **Tarayıcıyı tek pencere yap, kayıt alanını sadece o pencere olarak seç.**
4. **Yer imi çubuğunu gizle**, dikkat dağıtmasın (Cmd+Shift+B).
5. **Mikrofonu aç**, sesini de kaydet — boş video iyi değil.

## Senaryo (saniye saniye)

### 00:00-00:15 — Açılış
> "Merhaba, ben [Adınız Soyadınız]. Gazi Üniversitesi BLG106 İnternet Programcılığı
> dersi için geliştirdiğim İkinciElMarket'i tanıtıyorum. Uygulamanın modern ve 
> mobil uyumlu bir arayüze sahip olması için premium CSS ve Hero alanı ekledim."

- URL'i tarayıcı çubuğunda göster (canlı Render URL'i veya localhost).
- Anasayfa açılsın — Yeni eklediğimiz şık Hero alanı ve 8 ilan kartı görünür.

### 00:15-00:45 — Anasayfa, Arama, Kategori
> "Anasayfada son ilanlar görünüyor. Sol tarafta kategoriler var, üstte arama
> kutusu. 'iphone' aratıyorum..."

- Arama kutusuna "iphone" yaz, sonuç gelsin.
- Aramayı temizle, "Elektronik" kategorisine tıkla → filtrelenmiş liste.

> "Aynı anda hem kategori hem arama filtresi uygulanabiliyor; query parametreleri
> URL'de görünüyor."

- Adres çubuğunu bir saniye göster (`?kategori=elektronik&q=iphone`).

### 00:45-01:20 — Kayıt + Giriş
> "Yeni kullanıcı olarak kayıt olalım."

- Sağ üst "Kayıt ol" → form aç.
- `demo_kullanici`, `demo@test.com`, `demo1234`, `demo1234` → Submit.
- "Giriş yap" → aynı bilgilerle gir.

> "Şifreler werkzeug ile pbkdf2:sha256 algoritmasıyla hash'leniyor. Veritabanında
> düz metin tutulmuyor. Tüm formlarda CSRF token aktif."

(Bunu söylerken görsel olarak sadece flash mesajı yeterli — "Hoş geldin, demo_kullanici!")

### 01:20-02:00 — İlan Ekleme + Görsel Yükleme
> "Sağ üst 'İlan ver'."

- Form aç. Doldur:
  - Başlık: "PlayStation 5 Standart"
  - Kategori: Oyun & Hobi
  - Fiyat: 14500
  - Konum: "Ankara"
  - Açıklama: "1 yıl kullanılmış, kutusu mevcut, 2 oyun ve 1 ek kol dahil."
  - Görsel: bir JPG seç (sürükle-bırak)
- Kaydet → ilan detay sayfası açılır.

> "Görsel Pillow ile arka planda maksimum 1280px'e küçültülüyor; disk kullanımı
> kontrol altında."

### 02:00-02:30 — Favori + Mesajlaşma
> "Demo kullanıcısı `alice` ile iletişime geçelim. Onun ilanını açıyorum."

- Anasayfa → bir iPhone ilanına tıkla (alice'in).
- "Favorilere ekle" tıkla → flash mesaj.
- "Satıcıya mesaj at" tıkla → thread açılır.
- Mesaj kutusuna "Selam, görüşebilir miyiz?" yaz, gönder.
- "Mesajlar" navbar'a tıkla → inbox'ta thread görünür, okunmamış sayacı.

### 02:30-03:00 — Profil + Avatar + Dil
> "Profilimi güncelleyelim — bio ve avatar."

- Sağ üst avatar → "Profili düzenle" → bio yaz, avatar yükle → Kaydet.
- Sağ üst dil dropdown → "English" → arayüz İngilizce'ye dönsün.
- Tekrar "Türkçe" yap.

### 03:00-03:30 — Admin Paneli
> "Çıkış yapıp admin hesabıyla girelim — admin@ikincielmarket.local."

- Çıkış → Giriş (admin / şifre).
- Sağ üst sarı "Yönetim" → dashboard (4 sayaç: kullanıcı, ilan, kategori, mesaj).
- "Kullanıcılar" → liste → admin toggle gösterimi.
- "Kategoriler" → yeni kategori ekle (örn. "Telefon Aksesuarı" / "telefon-aksesuar").
- "Tüm İlanlar" → bir ilanı sil (admin yetkisiyle).

### 03:30-04:00 — JSON API + Hata Sayfaları
> "API endpoint'leri public — başka bir uygulama bunları tüketebilir."

- Adres çubuğunda `/api/v1/listings` → JSON çıktısı.
- `/api/v1/categories` → 8+ kategori JSON.
- Bir bozuk URL: `/yokboyle` → özel 404 sayfası.

### 04:00-04:30 — GitHub + Kapanış
> "Kodun tamamı GitHub'da public: github.com/DarryHack/ikincielmarket. 23 anlamlı
> commit, 13 birim testi, Türkçe + İngilizce arayüz, JSON API, e-posta şifre
> sıfırlama, Docker desteği. Geliştirme sürecimin tam kaydı docs/ai-gunlugu.md'de.
> Dinlediğiniz için teşekkürler."

- GitHub sekmesini aç, repo'yu göster (özellikle commit listesini scroll).

## İpuçları

- **Videoyu kısa tut** — 4:30'u geçme.
- **Hızlandırılmış kayıt:** Tüm tıklamaları normal yap; QuickTime ile çekip
  iMovie/CapCut'ta x1.5 hızlandırarak istersen.
- **Ses kalitesi:** AirPods/headset varsa onu kullan, dahili mic'ten kötü çıkar.
- **Yükleme:**
  - YouTube'a "Unlisted" olarak yükle (sadece linki bilen görsün).
  - Veya Google Drive'a yükle, paylaşım: "Linke sahip olan herkes görebilir".
- **README'ye ekle:**
  ```markdown
  ## Demo Video
  [YouTube link]
  ```
  Sonra `git commit -m "docs: demo video linki" && git push`.

## Eğer "Bir dakika eksik kaldı" Dersen

Ek 30-60 saniye için:
- Mobil görünüm: Chrome DevTools → cihaz emülasyonu (iPhone) → site responsive görünsün.
- Şifre sıfırlama akışı: `/auth/reset-password` → e-posta gir → "Linki gönderdik"
  flash mesajını göster (gerçek e-posta gerekmiyor demo için).
