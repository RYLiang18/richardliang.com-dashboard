import re
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

class FullNameUpdateForm(FlaskForm):
    full_name = StringField("Full Name", validators=[InputRequired()])
    update = SubmitField("Update")

class EmailUpdateForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    update = SubmitField("Update")

class PFPLinkUpdateForm(FlaskForm):
    url = URLField(
        "Image URL (ending in .jpg, .png, etc...)",
        validators = [InputRequired()]
    )
    update = SubmitField("Update")
    
    def validate_url(form, field):
        jpg_regex = r"\.jpg$"
        png_regex = r"\.png$"

        if (not re.search(jpg_regex, field.data)) and (not re.search(png_regex, field.data)):
            raise ValidationError("URL must end in .jpg or .png")

class DescriptionUpdateForm(FlaskForm):
    description = TextAreaField("Description", validators=[InputRequired()])
    update = SubmitField("Update")

class AboutMeUpdateForm(FlaskForm):
    about_me = TextAreaField("About Me", validators=[InputRequired()])
    update = SubmitField("Update")