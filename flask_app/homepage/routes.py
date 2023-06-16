from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from flask_app.homepage.forms import (
    AboutMeUpdateForm,
    DescriptionUpdateForm,
    EmailUpdateForm,
    PFPLinkUpdateForm,
)
from flask_app.models import HomepageDetails, Link, load_user  # Link
from flask_app.utils import current_time

homepage_blueprint = Blueprint(
    "homepage", __name__, url_prefix="/homepage", template_folder="./templates"
)


def matching_username(username):
    return current_user.username == username


@homepage_blueprint.route("/")
@login_required
def index():
    session["url"] = url_for("homepage.index")

    homepage_details = HomepageDetails.objects(
        owner=load_user(current_user.username)
    ).first()

    homepage_details_links = Link.objects(parent=homepage_details)

    return render_template(
        "homepage.html",
        title=f"{current_user.username}'s homepage",
        homepage_details=homepage_details,
        links=homepage_details_links,
    )


@homepage_blueprint.route("/update_email", methods=["GET", "POST"])
@login_required
def update_email():
    email_update_form = EmailUpdateForm()

    if email_update_form.validate_on_submit():
        homepage_details = HomepageDetails.objects(owner=current_user).first()
        homepage_details.update(email=email_update_form.content.data)

        return redirect(url_for("homepage.index"))

    return render_template(
        "submit_simple_content.html",
        form=email_update_form,
        title="Homepage - Update Email",
    )


@homepage_blueprint.route("/update_pfp_link", methods=["GET", "POST"])
@login_required
def update_pfp_link():
    pfp_link_update_form = PFPLinkUpdateForm()

    if pfp_link_update_form.validate_on_submit():
        homepage_details = HomepageDetails.objects(owner=current_user).first()
        homepage_details.update(pfp_link=pfp_link_update_form.content.data)

        return redirect(url_for("homepage.index"))

    return render_template(
        "submit_simple_content.html",
        form=pfp_link_update_form,
        title="Homepage - Update PFP Link",
    )


@homepage_blueprint.route("/update_description", methods=["GET", "POST"])
@login_required
def update_description():
    homepage_details = HomepageDetails.objects(owner=current_user).first()

    description_update_form = DescriptionUpdateForm(
        description=homepage_details.description
    )

    if description_update_form.validate_on_submit():
        homepage_details.update(description=description_update_form.description.data)

        return redirect(url_for("homepage.index"))

    return render_template(
        "update_description.html",
        form=description_update_form,
        title="Homepage - Update Description",
    )


@homepage_blueprint.route("/update_about_me", methods=["GET", "POST"])
@login_required
def update_about_me():
    homepage_details = HomepageDetails.objects(owner=current_user).first()

    about_me_update_form = AboutMeUpdateForm(about_me=homepage_details.about_me)

    if about_me_update_form.validate_on_submit():
        homepage_details.update(about_me=about_me_update_form.about_me.data)

        return redirect(url_for("homepage.index"))

    return render_template(
        "update_about_me.html",
        form=about_me_update_form,
        title="Homepage - Update About Me",
    )
