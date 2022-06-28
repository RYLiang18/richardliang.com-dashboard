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

def is_date(data):
    regex = r"(^[\d]{2}/[\d]{2}/[\d]{4}$)|(^present$)"
    return bool(re.search(regex, data))

class CreateExperience(FlaskForm):
    company_name = StringField("Company Name", validators=[InputRequired])
    start_date = StringField("Start Date", validators=[InputRequired])
    end_date = StringField("End Date", validators=[InputRequired])
    about = StringField("About Experience", validators=[InputRequired])

    def validate_start_date(form, field):
        if not is_date(field.data):
            raise ValidationError(
                "Date must be in the format \"MM/DD/YYYY\" or \"present\""
            )
    
    def validate_end_date(form, field):
        if not is_date(field.data):
            raise ValidationError(
                "Date must be in the format \"MM/DD/YYYY\" or \"present\""
            )