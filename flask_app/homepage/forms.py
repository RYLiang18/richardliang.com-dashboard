import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields import EmailField, URLField
from wtforms.validators import InputRequired, ValidationError


class FullNameUpdateForm(FlaskForm):
    full_name = StringField("Full Name", validators=[InputRequired()])
    update = SubmitField("Update")


class EmailUpdateForm(FlaskForm):
    content = EmailField("Email", validators=[InputRequired()])
    submit = SubmitField("Update")


class ShortDescriptionUpdateForm(FlaskForm):
    content = StringField("Short Description", validators=[InputRequired()])
    submit = SubmitField("Update")
