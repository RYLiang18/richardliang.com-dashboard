from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from flask_app import bcrypt, ipsum
from flask_app.models import HomepageDetails, User, load_user
from flask_app.users.forms import LoginForm
from flask_app.utils import current_time

users_blueprint = Blueprint("users", __name__, template_folder="./templates")


def new_default_homepage():
    default_homepage_details = HomepageDetails(
        owner=load_user(current_user.username),
        full_name="Replace with your full name",
        email="your_email@example.com",
        image_link="https://i.imgur.com/5r7v03y.png",
        description="replace me with a short description of yourself",
        long_description=ipsum(),
        creation_datetime=current_time(),
    )
    default_homepage_details.save()


@users_blueprint.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("homepage.index"))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.objects(username=login_form.username.data).first()
        if user is not None and bcrypt.check_password_hash(
            user.password, login_form.password.data
        ):
            # CASE: successful login
            login_user(user)

            # give current_user a default homepage if it doesn't exist.
            # since each user must own a HomepageDetails document, we can assume that
            # if the user does not have one, current_user is new, and we'll have to give them
            # a default homepage
            homepage_details = HomepageDetails.objects(
                owner=load_user(current_user.username)
            ).first()

            if not homepage_details:
                new_default_homepage()

            return redirect(url_for("homepage.index"))
        else:
            # CASE: unsuccessful login
            flash("username or password incorrect")
            return redirect(url_for("users.login"))

    return render_template("login.html", form=login_form, title="login")


@users_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.login"))
