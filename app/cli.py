"""Flask CLI komutları: seed, admin oluştur, demo verisi."""
from __future__ import annotations
import shutil
from pathlib import Path
import click
from flask import current_app
from flask.cli import with_appcontext
from app.extensions import db
from app.models import User, Category, Listing, Favorite, Message


DEFAULT_CATEGORIES = [
    ("Elektronik", "elektronik"),
    ("Ev & Yaşam", "ev-yasam"),
    ("Moda", "moda"),
    ("Oyun & Hobi", "oyun-hobi"),
    ("Spor", "spor"),
    ("Kitap & Müzik", "kitap-muzik"),
    ("Araç", "arac"),
    ("Diğer", "diger"),
]


@click.command("seed")
@with_appcontext
def seed_command():
    """Varsayılan kategorileri ve admin kullanıcıyı oluşturur."""
    created_cats = 0
    for name, slug in DEFAULT_CATEGORIES:
        if not db.session.scalar(db.select(Category).where(Category.slug == slug)):
            db.session.add(Category(name=name, slug=slug))
            created_cats += 1
    db.session.commit()
    click.echo(f"Kategori eklendi: {created_cats} (toplam: {len(DEFAULT_CATEGORIES)})")

    admin_email = current_app.config["ADMIN_EMAIL"]
    admin_pw = current_app.config["ADMIN_PASSWORD"]
    admin = db.session.scalar(db.select(User).where(User.email == admin_email))
    if not admin:
        admin = User(username="admin", email=admin_email, is_admin=True)
        admin.set_password(admin_pw)
        db.session.add(admin)
        db.session.commit()
        click.echo(f"Admin oluşturuldu: {admin_email} / {admin_pw}")
    else:
        if not admin.is_admin:
            admin.is_admin = True
            db.session.commit()
        click.echo(f"Admin zaten var: {admin_email}")


DEMO_LISTINGS = [
    ("iPhone 13 128GB", "iphone", "elektronik", 18500,
     "1 yıl kullanılmış iPhone 13. Aksesuarları ve kutusu mevcut. Pil sağlığı %92, "
     "ekran ve kasa kusursuz. Garanti bitti, fatura var. Takasa kapalı, kapıda ödeme yok.",
     "Ankara / Çankaya"),
    ("MacBook Air M1 8/256", "laptop", "elektronik", 24000,
     "2021 model MacBook Air M1, 8GB RAM 256GB SSD. Üniversite için aldım, çok az kullandım. "
     "Şarj döngüsü 120. Kutusu kayıp ama orijinal şarj cihazı dahil.",
     "İstanbul / Beşiktaş"),
    ("Bianchi Yol Bisikleti", "bisiklet", "spor", 8500,
     "Bianchi Via Nirone 7, beden 53. Karbon çatal, alüminyum kadro. Yıllık bakımı yapıldı, "
     "kaset ve zincir geçen ay yenilendi. Acil ihtiyaçtan satıyorum.",
     "İzmir / Karşıyaka"),
    ("İtalyan 3'lü Deri Koltuk", "koltuk", "ev-yasam", 6200,
     "Hakiki deri, 3 yaş, leke yok. Renk: bordo. Boyutlar 220x95cm. Taşınma sebebiyle "
     "satıyorum, taşıma alıcıya ait. Ankara içi ücretsiz teslim olanağı var.",
     "Ankara / Çayyolu"),
    ("Yaşar Kemal Tüm Eserleri (24 cilt)", "kitap", "kitap-muzik", 1800,
     "YKY baskısı, hepsi okunmuş ama özenli kullanılmış. Bir tanesi ciltsiz, "
     "diğerleri ciltli. Edebiyat öğrencilerinin gözünden kaçırmaması gereken bir set.",
     "İstanbul / Kadıköy"),
    ("Canon EOS R6 Mark II Body", "kamera", "elektronik", 65000,
     "10 ay kullanılmış, 2300 deklanşör. Hiç düşürülmedi, çizik yok. Kutu, şarj, kayış mevcut. "
     "İkinci bir gövdeye geçtiğim için satıyorum. Fatura ve garanti.",
     "Ankara / Kızılay"),
    ("Sony WH-1000XM5 Kulaklık", "kulaklik", "elektronik", 8900,
     "6 ay kullanılmış kablosuz kulaklık. Şarj 30 saat, ANC mükemmel. Kutusu ve kabloları "
     "var. Pil durumu yeni gibi.",
     "Bursa / Nilüfer"),
    ("IKEA BEKANT Çalışma Masası", "masa", "ev-yasam", 2400,
     "160x80cm beyaz IKEA BEKANT. 1 yaş, kullanım izi yok. Üzerine monitör kolu monte edildi, "
     "delikler arka tarafta. Taşımayı alıcı yapacak; söküp veriyorum.",
     "Eskişehir / Tepebaşı"),
]


def _copy_seed_image(slug: str) -> str | None:
    src = Path(current_app.root_path) / "static" / "img" / "seed" / f"{slug}.svg"
    if not src.exists():
        return None
    dst_dir = Path(current_app.config["UPLOAD_FOLDER"]) / "listings"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_name = f"seed-{slug}.svg"
    dst = dst_dir / dst_name
    if not dst.exists():
        shutil.copy(src, dst)
    return dst_name


@click.command("seed-demo")
@with_appcontext
def seed_demo_command():
    """Demo videosu için örnek kullanıcılar + 8 ilan + favori + mesaj ekler."""
    # Demo kullanıcılar
    demo_users = [
        ("alice", "alice@demo.local", "demo1234", "Yaşadığım şehirde takasla satıyorum."),
        ("bora", "bora@demo.local", "demo1234", "Fotoğrafçı, ikinci ele meraklı."),
        ("ceren", "ceren@demo.local", "demo1234", "Kitap koleksiyonu satıyorum."),
    ]
    created_users = []
    for u, e, p, bio in demo_users:
        existing = db.session.scalar(db.select(User).where(User.email == e))
        if existing:
            created_users.append(existing)
            continue
        user = User(username=u, email=e, bio=bio)
        user.set_password(p)
        db.session.add(user)
        created_users.append(user)
    db.session.commit()

    cats_by_slug = {c.slug: c for c in db.session.scalars(db.select(Category))}

    # Demo ilanlar (sırayla 3 kullanıcıya dağıt)
    created_count = 0
    for i, (title, img_slug, cat_slug, price, desc, loc) in enumerate(DEMO_LISTINGS):
        if db.session.scalar(db.select(Listing).where(Listing.title == title)):
            continue
        listing = Listing(
            title=title,
            description=desc,
            price=price,
            location=loc,
            user_id=created_users[i % len(created_users)].id,
            category_id=cats_by_slug[cat_slug].id,
            image=_copy_seed_image(img_slug),
        )
        db.session.add(listing)
        created_count += 1
    db.session.commit()

    # Bir favori + bir mesaj thread'i
    sample_listing = db.session.scalar(db.select(Listing).order_by(Listing.id))
    if sample_listing and len(created_users) >= 2:
        if not db.session.scalar(
            db.select(Favorite).where(
                (Favorite.user_id == created_users[1].id) & (Favorite.listing_id == sample_listing.id)
            )
        ):
            db.session.add(Favorite(user_id=created_users[1].id, listing_id=sample_listing.id))
        if not db.session.scalar(db.select(Message).where(Message.listing_id == sample_listing.id)):
            db.session.add(Message(
                sender_id=created_users[1].id,
                receiver_id=sample_listing.user_id,
                listing_id=sample_listing.id,
                body="Selam, hâlâ satılık mı? Fiyatta esneklik var mı?",
            ))
            db.session.add(Message(
                sender_id=sample_listing.user_id,
                receiver_id=created_users[1].id,
                listing_id=sample_listing.id,
                body="Merhaba, evet satılık. Pazarlık payı az, ama görüşürüz.",
            ))
        db.session.commit()

    click.echo(f"Demo kullanıcı: {len(created_users)}  |  ilan eklendi: {created_count}")
    click.echo("Giriş: alice@demo.local / demo1234")


def register_cli(app):
    app.cli.add_command(seed_command)
    app.cli.add_command(seed_demo_command)
