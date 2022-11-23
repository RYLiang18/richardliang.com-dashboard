from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField
)
from wtforms.fields import (
    URLField,
    EmailField
)
from wtforms.validators import (
    InputRequired,
    ValidationError
)

from flask_app.utils import is_url
import re


class CreateLinkForm(FlaskForm):
    link_name = StringField("Link Name", validators=[InputRequired()])
    url = URLField("Link URL", validators=[InputRequired()])
    submit = SubmitField("Add")

    def validate_url(form, field):
        if not is_url(field.data):
            raise ValidationError("URL must be formatted correctly")


class UpdateLinkForm(FlaskForm):
    link_name = StringField("Link Name", validators=[InputRequired()])
    url = URLField("Link URL", validators=[InputRequired()])
    update = SubmitField("Update")

    def validate_url(form, field):
        if not is_url(field.data):
            raise ValidationError("URL must be formatted correctly")


class CreateBulletForm(FlaskForm):
    content = StringField("Content", validators=[InputRequired()])
    submit = SubmitField("Add")