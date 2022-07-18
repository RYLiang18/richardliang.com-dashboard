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
)


class UpdateLinkForm(FlaskForm):
    link_name = StringField("Link Name", validators=[InputRequired()])
    url = URLField("Link URL", validators=[InputRequired()])
    update = SubmitField("Update")

class CreateLinkForm(FlaskForm):
    link_name = StringField("Link Name", validators=[InputRequired()])
    url = URLField("Link URL", validators=[InputRequired()])
    submit = SubmitField("Add")