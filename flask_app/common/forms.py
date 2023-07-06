import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields import EmailField, URLField
from wtforms.validators import InputRequired, ValidationError

from flask_app.utils import is_date, is_url


class SubmitLinkForm(FlaskForm):
    link_name = StringField("Link Name", validators=[InputRequired()])
    url = URLField("Link URL", validators=[InputRequired()])

    def validate_url(form, field):
        if not is_url(field.data):
            raise ValidationError("URL must be formatted correctly")

    submit = SubmitField("Submit")


class SubmitSimpleStringContentForm(FlaskForm):
    content = StringField("Content", validators=[InputRequired()])
    submit = SubmitField("Submit")


class UpdateDateForm(FlaskForm):
    content = StringField("Date", validators=[InputRequired()])
    submit = SubmitField("Update")

    def validate_content(form, field):
        if not is_date(field.data):
            raise ValidationError(
                'Date must be in the format "MM/DD/YYYY" or "present"'
            )


class UpdateImageLinkForm(FlaskForm):
    content = URLField(
        "Image URL (ending in .jpg, .png, etc...)", validators=[InputRequired()]
    )
    submit = SubmitField("Update")

    def validate_content(form, field):
        image_extensions = {".jpg": r"\.jpg$", ".png": r"\.png$", ".jpeg": r"\.jpeg$"}

        valid = False
        for _, image_extension_regex in image_extensions.items():
            valid = valid or re.search(image_extension_regex, field.data)

        if not valid:
            raise ValidationError(
                f"supported URL prefixes: {', '.join(list(image_extensions.keys()))}"
            )
