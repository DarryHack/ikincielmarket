from decimal import Decimal
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ListingForm(FlaskForm):
    title = StringField("Başlık", validators=[DataRequired(), Length(min=3, max=140)])
    description = TextAreaField("Açıklama", validators=[DataRequired(), Length(min=10, max=4000)])
    price = DecimalField(
        "Fiyat (₺)", places=2, validators=[DataRequired(), NumberRange(min=0, max=10_000_000)]
    )
    location = StringField("Konum", validators=[Length(max=120)])
    category_id = SelectField("Kategori", coerce=int, validators=[DataRequired()])
    image = FileField(
        "Görsel",
        validators=[FileAllowed(["jpg", "jpeg", "png", "gif", "webp"], "Sadece resim dosyaları.")],
    )
    submit = SubmitField("Kaydet")


class DeleteListingForm(FlaskForm):
    submit = SubmitField("Sil")
