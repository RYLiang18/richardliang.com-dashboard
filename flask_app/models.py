from flask_login import (
    UserMixin,
    current_user
)
from flask_app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)

    def get_id(self):
        return self.username

class Link(db.Document):
    owner = db.ReferenceField(User, required=True)
    link_name = db.StringField(required=True)
    url = db.URLField(required=True)

    # using StringField instead of DateTimeField since time is part of ID that
    # will be passed into a route URL
    datetime_str = db.StringField(required=True)

    def get_id(self):
        return [self.owner.username, self.datetime_str]

class HomepageDetails(db.Document):
    owner = db.ReferenceField(User, required=True)
    full_name = db.StringField(required=True)
    email = db.EmailField(required=True)
    pfp_link = db.URLField(required=True)
    description = db.StringField(required=True)
    links = db.ListField(db.ReferenceField(Link))
    about_me = db.StringField(required=True)

    def get_id(self):
        return self.owner.username
    
    def parse_about_me(self):
        return self.about_me.split('\n')

class Experience(db.Document):
    owner = db.ReferenceField(User, required=True)
    company_name = db.StringField(required=True)
    position = db.StringField(required=True)
    start_date = db.StringField(required=True)
    end_date = db.StringField(required=True)
    about = db.StringField(required=True)
    creation_time = db.StringField(required=True)

    def parse_about(self):
        return self.about.split('\n')

class ExperienceTechnology(db.Document):
    owner = db.ReferenceField(User, required=True)
    experience = db.ReferenceField(Experience, required=True)
    tech = db.StringField()
    creation_time = db.StringField(required=True)

    def get_id(self):
        return [self.owner.username, self.creation_time]

class ExperienceBullet(db.Document):
    owner = db.ReferenceField(User, required=True)
    experience = db.ReferenceField(Experience, required=True)

    # using StringField instead of DateTimeField since time is part of ID that
    # will be passed into a route URL
    creation_time = db.StringField(required=True)
    content = db.StringField(required=True)

    def get_id(self):
        return [self.owner.username, self.creation_time]

class ExperienceLink(db.Document):
    owner = db.ReferenceField(User, required=True)
    experience = db.ReferenceField(Experience, required=True)
    link_name = db.StringField(required=True)
    url = db.URLField(required=True)
    creation_time = db.StringField(required=True)

    def get_id(self):
        return [self.owner.username, self.creation_time]