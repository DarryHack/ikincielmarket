# Ekran Görüntüleri Rehberi

Bu klasör AI günlüğü ve rapor için ekran görüntülerine ev sahipliği yapar.
PDF Bölüm 6.4: **en az 5 ekran görüntüsü gerekli**.

## Çek + Buraya Koy (önerilen liste)

| Dosya Adı | Ne Çekeceksin |
|-----------|---------------|
| `01-anasayfa.png` | Anasayfa, 8 demo ilan görünür, kategori sidebar açık |
| `02-kayit-formu.png` | `/auth/register` form sayfası |
| `03-ilan-detay.png` | Bir ilan detay sayfası, "Satıcıya mesaj at" + "Favoriye ekle" butonları |
| `04-yeni-ilan-formu.png` | `/ilan/yeni`, görsel upload alanı dolu |
| `05-admin-dashboard.png` | `/admin/`, 4 sayaç görünür |
| `06-mesaj-thread.png` | İki kullanıcı arası sohbet penceresi |
| `07-mobil-gorunum.png` | Chrome DevTools cihaz emülasyonu (iPhone) açık |
| `08-api-json.png` | `/api/v1/listings` JSON çıktısı tarayıcıda |
| `09-404-sayfa.png` | `/yokboyle` özel 404 sayfası |
| `10-dil-en.png` | İngilizce arayüz (EN'e geçtikten sonra) |

## Nasıl çekilir?

### macOS
- **Pencere:** `Cmd + Shift + 4`, sonra `Space` → tıkla.
- **Belirli alan:** `Cmd + Shift + 4` → sürükle.
- Çıkan dosyayı buraya sürükle ve yeniden adlandır.

### Windows
- **Snipping Tool** (Win + Shift + S).

## AI Günlüğüne / Rapora Bağla

Markdown'da:

```markdown
![Anasayfa](img/01-anasayfa.png)
```

PDF ekran görüntülerine "kanıt" olarak bakacak — bunlar dosyaların gerçek
varlığını (Antigravity'nin Walkthrough panelinin yerine) gösterir.
