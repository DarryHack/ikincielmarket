from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    body = TextAreaField("Mesaj", validators=[DataRequired(), Length(min=1, max=2000)])
    listing_id = HiddenField()
    receiver_id = HiddenField()
    submit = SubmitField("Gönder")
