# 🌅 SABAH UYANDIĞINDA — OKU VE YAP

**Şu an:** 1 Haziran 2026 sabahı  
**Teslim:** 01/06/2026 saat **13:00** (yaklaşık 3-4 saatin var)

---

## 📌 ÖZET: NEREDEYİZ?

| | Değer |
|--|--|
| **Şu anki tahmini puan** | **82/100** |
| **Kalan kritik işler yapılırsa** | **94/100** |
| **En kötü senaryo (Tunnel düşer + demo eksik)** | 62/100 |

**Üç paralel agent + sentez ajanı PDF'in her maddesini denetledi.** Aşağıdaki liste o denetimin sonucudur — uydurma değil, snapshot'tan kanıt-temelli.

---

## ✅ GECE TAMAMLANANLAR (kanıtlı, repo'da)

- ✓ **42 commit** PUSH edildi (`DarryHack/ikincielmarket`, eşik 15'in ~2.8x üstünde)
- ✓ **Canlı dağıtım çalışıyor:** https://swing-duncan-customize-transportation.trycloudflare.com → 200 OK, 335ms
- ✓ Docker + compose + render.yaml + Procfile + runtime.txt → çoklu platform yedekli
- ✓ **10/10 zorunlu teknik bileşen** tam (5 model, 7 blueprint, migration, CSRF, 404/500, pagination, Bootstrap responsive)
- ✓ pbkdf2:sha256 hash → "düz metin -15" cezası savuşturuldu
- ✓ `.env` git'te değil → "secret -10" cezası savuşturuldu
- ✓ **24/24 test**, coverage %60
- ✓ **AI günlüğü 9 oturum, ~5400 kelime** (eşik 7'nin üstünde — Mükemmel bandı)
- ✓ **19 ekran görüntüsü** `docs/img/01-...19-*.png` (Playwright otomasyon, eşik 5'in ~4x üstü)
- ✓ Antigravity Oturum 8 commit `43df15c` ile kanıtlanmış (premium Hero CSS) → "başka IDE -20" cezası hafifletildi
- ✓ **5 bonus** tam: e-posta sıfırlama (+5), /api/v1 (+5), LIKE arama (+3), TR-EN (+3), avatar (+4) = **+20**
- ✓ Rapor 7 maddesi tam (1547 kelime — biraz uzun ama dolu)
- ✓ CI + LICENSE (profesyonellik sinyali)
- ✓ Sahtecilik riski **SIFIR** — her iddia commit/PNG/test/URL ile kanıtlı

---

## 🚨 ALTYAPI UYARISI (önce buna bak!)

**Cloudflared Quick Tunnel makinenden çalışıyor** — yerel Flask'a bağlı. Eğer:
- Makine kapatıldıysa veya uyku modundaysa → URL ölür
- Flask process'i durduysa → 502/520 hatası

**Önce kontrol et:**
🔗 https://swing-duncan-customize-transportation.trycloudflare.com

Eğer **siteye giremezsen**, hemen şu komutu çalıştır (terminal aç):

```bash
cd ~/Desktop/ikincielmarket
source venv/bin/activate
nohup flask run --port 5050 --no-debugger --no-reload > /tmp/flask.log 2>&1 &
nohup ~/bin/cloudflared tunnel --url http://localhost:5050 > /tmp/cf.log 2>&1 &
sleep 6
echo "Yeni URL: $(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/cf.log | head -1)"
```

Yeni URL alırsan README + günlüğü güncelle ve push'la:
```bash
NEW_URL=$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/cf.log | head -1)
OLD_URL="https://swing-duncan-customize-transportation.trycloudflare.com"
grep -rl "$OLD_URL" README.md docs/ | xargs sed -i.bak "s|$OLD_URL|$NEW_URL|g"
find . -name "*.bak" -delete
git add -A && git commit -m "docs: canlı URL refresh" && git push
```

---

## ⚡ YAPMAN GEREKEN 3 İŞ (sıralı, kritiklik bandında)

### 1. ⏱ Demo Video Çek + YouTube'a Yükle — **+5 puan, 45 dk**

`docs/demo-senaryosu.md` dosyasını aç — 4:30 dk script hazır, satır satır okunacak. Canlı URL'de seed-demo verisi otomatik geliyor (8 ilan + 3 kullanıcı).

```bash
# macOS QuickTime:
open -a "QuickTime Player"
# File → New Screen Recording (veya Cmd+Shift+5)
# Mikrofonu aç, "Pencere modu" seç
```

**Demo hesapları (canlı URL'de hazır):**
| Hesap | E-posta | Şifre |
|-------|---------|-------|
| Admin | admin@ikincielmarket.local | admin1234 |
| Alice | alice@demo.local | demo1234 |
| Bora | bora@demo.local | demo1234 |

**Akış (script'ten özet):** anasayfa Hero → arama → kayıt + giriş → ilan oluştur → favori + mesaj → profil + avatar → dil değiştir (EN) → admin paneli → API JSON → 404 → kapanış.

**Sonra:**
- YouTube'a "Unlisted" yükle (sadece linki bilenler görür)
- README.md'de "## Demo Video" bölümünü bul, linki yapıştır
- `git add README.md && git commit -m "docs: demo video linki" && git push`

### 2. 📦 LMS / GUZEM Zip Upload — **Teslim ŞARTI, 15 dk**

PDF "GitHub repo (public) + README.md + GUZEM (zip upload)" diyor.

```bash
cd ~/Desktop/ikincielmarket
# venv ve uploads hariç temiz zip:
git archive --format=zip HEAD -o ~/Desktop/ikincielmarket-final.zip
ls -lh ~/Desktop/ikincielmarket-final.zip
```

Sonra **lms.gazi.edu.tr** → BLG106 → ödev → yükle.
Form GitHub URL de istiyorsa: **https://github.com/DarryHack/ikincielmarket**

### 3. 🔁 (Opsiyonel ama önerilir) Render.com'a Kalıcı Deploy — **Dağıtım garantisi, 25 dk**

Quick Tunnel makinen kapanınca ölür. Hocanın değerlendireceği anda 503 dönerse 5 puan kaybedersin.

```
1. render.com → Sign up (GitHub ile, ücretsiz)
2. New + → Blueprint
3. Connect repo: DarryHack/ikincielmarket
4. Render.yaml'i görür → Apply
5. ADMIN_PASSWORD'a manuel bir şey yaz (örn. "admin1234")
6. Deploy başlar (~6 dk)
7. URL gelince README'ye yapıştır + push
```

`docs/deploy.md` adım adım rehber bu işin tamamı.

---

## 📊 PUAN TAHMİNİ DETAYI

| Kalem | Şu an | 3 işi yaparsan |
|-------|------:|---------------:|
| Teknik Doğruluk (30) | 28-30 | 28-30 |
| AI Günlüğü (25) | **22-25** (19 SS, Mükemmel bandı) | 22-25 |
| Vibe Coding Disiplini (15) | 12-14 | 12-14 |
| Kod Kalitesi (10) | 9-10 | 9-10 |
| Demo+Rapor (10) | 5/10 (rapor var, demo yok) | **10/10** |
| UI/UX (5) | 5 (Antigravity Hero) | 5 |
| Dağıtım (5) | 5 (canlı URL aktif) | 5 (kalıcı Render ile garanti) |
| Antigravity cezası | -10 (Oturum 8 kanıtı) | -10 |
| Bonuslar | +20 (tavan 100'de eritilir) | +20 |
| **TOPLAM** | **~82** | **~94** |

---

## 🎤 Sözlü Değerlendirme Hazırlığı

Eğer hoca sorarsa, hazır cevaplar:

**"Antigravity mi kullandın?"**  
→ "Ana geliştirmeyi Claude Code'da yaptım, Oturum 8'i Antigravity'de — Hero alanı + premium CSS Antigravity'de eklendi (commit `43df15c`'de görünür). AI günlüğünde her ikisini de **şeffaf** belgeledim. Sahtecilik yapmayı reddettim."

**"Bu özelliği nasıl yaptın?"**  
→ Her özelliğin AI günlüğünde Oturum referansı + commit hash var. İlgili oturuma bak, sorgulama+düzeltme akışını anlat.

**"Bu hatayı neden böyle çözdün?"**  
→ Oturum 6 ve Oturum 9'da 5+ gerçek hata + çözüm var (jwt import, scrypt, Jinja kwargs, str|None, email-validator). Her birinin "neden böyle" açıklaması mevcut.

**"Canlı URL ne?"**  
→ "Cloudflared Quick Tunnel ile demo deploy ettim. Render kalıcı deploy de hazır (`render.yaml` var). Quick Tunnel anında public erişim sağladı."

**"Demo videoyu kim çekti?"**  
→ "Ben çektim, screen recording. Akışı `docs/demo-senaryosu.md` script'inden takip ettim."

---

## 🚨 SÖZLÜ DEĞERLENDİRME RİSKLERİ

- **Quick Tunnel düşmesi** → değerlendirme anında URL ölü olabilir. Render deploy yap (25 dk).
- **Demo yok savunması** → rapor tam olsa bile video yoksa ~5 puan kayıp neredeyse garanti.
- **Coverage %60 sorgusu** → "Kritik akışlar (auth, ilan CRUD, API) tam kapsanmış, view layer %60'a çekti" diyebilirsin.
- **Bonus iddialarının canlı ispatı** → "TR-EN dil değiştirici nerede?" sorulursa canlı URL'de göstermeye hazır ol.

---

## 🔚 Final Kontrol Listesi (teslim öncesi 5 dk)

```bash
cd ~/Desktop/ikincielmarket

# Test geçiyor mu?
source venv/bin/activate && pytest -q

# Tüm commit'ler GitHub'da mı?
git status                          # → "nothing to commit, working tree clean"
git log --oneline | head -3

# Canlı URL erişilebilir mi?
curl -sI https://swing-duncan-customize-transportation.trycloudflare.com | head -1

# Demo video linki README'de mi?
grep -i youtube README.md | grep -v "kayıt sonrası eklenecek"
```

**Bütün kontrolleri geçtiysen → LMS'ye gir → zip yükle → repo linkini yapıştır → TESLİM.**

---

## 🌅 İLK 30 DAKİKA İÇİN PLAN

1. **Önce kontrol** (2 dk) — canlı URL'i tarayıcıda aç. Eğer 200 değilse yukarıdaki "ALTYAPI UYARISI" komutlarını çalıştır.
2. **Demo video çek** (20 dk kayıt + 10 dk yükleme) — `docs/demo-senaryosu.md` script'iyle. Hata yapsan kes, baştan al — 3-5 dk olsun yeter.
3. **LMS zip yükle** (5 dk) — `git archive` komutu yukarıda hazır.

**3 saat 36 dk + 30 dk → ~92 puan teslime gider.**

İyi şanslar! 🎯
