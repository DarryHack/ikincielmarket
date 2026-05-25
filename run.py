"""Geliştirme sunucusu giriş noktası."""
import os
from app import create_app, db
from app.models import User, Category, Listing, Favorite, Message

app = create_app(os.environ.get("FLASK_CONFIG", "development"))


@app.shell_context_processor
def shell_context():
    return {
        "db": db,
        "User": User,
        "Category": Category,
        "Listing": Listing,
        "Favorite": Favorite,
        "Message": Message,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
