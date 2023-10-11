from flask_login import UserMixin, current_user

from flask_app import db, login_manager
from flask_app.utils import b64_decode


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)  # primary key
    password = db.StringField(required=True)

    def get_id(self):
        return self.username


class Link(db.Document):
    parent = db.GenericReferenceField(required=True)  # primary key
    link_name = db.StringField(required=True)
    url = db.URLField(required=True)
    creation_datetime = db.StringField(required=True)  # primary key


# encapsulates bullet points and technology badges
class StringContent(db.Document):
    parent = db.GenericReferenceField(required=True)  # primary key
    content_type = db.StringField(required=True)
    content = db.StringField(required=True)
    creation_datetime = db.StringField(required=True)  # primary key


class HomepageDetails(db.Document):
    owner = db.ReferenceField(User, required=True)  # primary key
    creation_datetime = db.StringField(required=True)
    full_name = db.StringField(required=True)
    email = db.EmailField(required=True)
    image_link = db.URLField(required=True)
    short_description = db.StringField(required=True)
    long_description_b64 = db.StringField(required=True)

    def parse_long_description(self):
        return b64_decode(self.long_description_b64)


class Experience(db.Document):
    owner = db.ReferenceField(User, required=True)  # primary key
    company_name = db.StringField(required=True)
    position = db.StringField(required=True)
    start_date = db.StringField(required=True)
    end_date = db.StringField(required=True)
    image_link = db.URLField(required=True)
    long_description_b64 = db.StringField(required=True)
    creation_datetime = db.StringField(required=True)  # primary key

    def parse_long_description(self):
        return b64_decode(self.long_description_b64)


class Project(db.Document):
    owner = db.ReferenceField(User, required=True)  # primary key
    project_name = db.StringField(required=True)
    start_date = db.StringField(required=True)
    end_date = db.StringField()
    image_link = db.URLField(required=True)
    long_description_b64 = db.StringField(required=True)
    creation_datetime = db.StringField(required=True)  # primary key

    def parse_long_description(self):
        return b64_decode(self.long_description_b64)
