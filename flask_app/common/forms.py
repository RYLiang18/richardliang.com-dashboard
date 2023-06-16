import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields import EmailField, URLField
from wtforms.validators import InputRequired, ValidationError

from flask_app.utils import is_date, is_url


class BaseLinkForm(FlaskForm):
    link_name = StringField("Link Name", validators=[InputRequired()])
    url = URLField("Link URL", validators=[InputRequired()])

    def validate_url(form, field):
        if not is_url(field.data):
            raise ValidationError("URL must be formatted correctly")


class CreateLinkForm(BaseLinkForm):
    submit = SubmitField("Add")


class UpdateLinkForm(BaseLinkForm):
    update = SubmitField("Update")


class SubmitSimpleStringContentForm(FlaskForm):
    content = StringField("Content", validators=[InputRequired()])
    submit = SubmitField("Submit")


# class CreateStringContentForm(BaseStringContentForm):
#     submit = SubmitField("Add")


# class UpdateStringContentForm(BaseStringContentForm):
#     update = SubmitField("Update")


class UpdateDateForm(FlaskForm):
    content = StringField("Date", validators=[InputRequired()])
    submit = SubmitField("Update")

    def validate_content(form, field):
        if not is_date(field.data):
            raise ValidationError(
                'Date must be in the format "MM/DD/YYYY" or "present"'
            )
