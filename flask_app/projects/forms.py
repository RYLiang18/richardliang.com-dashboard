import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields import EmailField, URLField
from wtforms.validators import InputRequired, ValidationError

from flask_app.utils import is_date


class CreateProjectForm(FlaskForm):
    project_name = StringField("Project Name", validators=[InputRequired()])
    start_date = StringField("Start Date", validators=[InputRequired()])
    end_date = StringField("End Date", validators=[InputRequired()])
    long_description = TextAreaField("Long Description", validators=[InputRequired()])
    submit = SubmitField("Submit")

    def validate_start_date(form, field):
        if not is_date(field.data):
            raise ValidationError(
                'Date must be in the format "MM/DD/YYYY" or "present"'
            )

    def validate_end_date(form, field):
        if not is_date(field.data):
            raise ValidationError(
                'Date must be in the format "MM/DD/YYYY" or "present"'
            )
