"""Flask CLI komutları: seed, admin oluştur."""
import click
from flask import current_app
from flask.cli import with_appcontext
from app.extensions import db
from app.models import User, Category, Listing


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


def register_cli(app):
    app.cli.add_command(seed_command)
