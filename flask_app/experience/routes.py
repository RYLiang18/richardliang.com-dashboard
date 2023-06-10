from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_app.experience.forms import CreateExperienceForm
from flask_login import login_required, current_user
from flask_app.models import (
    Experience,
    ExperienceBullet,
    ExperienceTechnology,
    ExperienceLink,
    load_user,
    Link,
)
from flask_app.utils import current_time

experience_blueprint = Blueprint(
    "experience", __name__, url_prefix="/experience", template_folder="./templates"
)


@experience_blueprint.route("/")
@login_required
def index():
    experiences = Experience.objects()

    return render_template(
        "experience.html",
        title=f"{current_user.username}'s experiences",
        experiences=experiences,
    )


@experience_blueprint.route("/create_experience", methods=["GET", "POST"])
@login_required
def create_experience():
    create_experience_form = CreateExperienceForm()

    if create_experience_form.validate_on_submit():
        new_experience = Experience(
            owner=load_user(current_user.username),
            company_name=create_experience_form.company_name.data,
            position=create_experience_form.position.data,
            start_date=create_experience_form.start_date.data,
            end_date=create_experience_form.end_date.data,
            about=create_experience_form.about.data,
            creation_datetime=current_time(),
        )
        new_experience.save()

        return redirect(url_for("experience.index"))

    return render_template(
        "create_experience.html",
        title="Experience - Create Experience",
        form=create_experience_form,
    )


@experience_blueprint.route(
    "/view_experience/<experience_creation_datetime>", methods=["GET"]
)
@login_required
def view_experience(experience_creation_datetime):
    session["url"] = url_for(
        "experience.view_experience",
        experience_creation_datetime=experience_creation_datetime,
    )

    experience = Experience.objects(
        owner=load_user(current_user.username),
        creation_datetime=experience_creation_datetime,
    ).first()

    if experience is None:
        # TODO: return 404
        pass

    tech_stack = ExperienceTechnology.objects(experience=experience)
    bullet_points = ExperienceBullet.objects(experience=experience)
    experienceLinks = Link.objects(parent=experience)

    # ExperienceLink.objects(
    #     experience = experience
    # )

    return render_template(
        "view_experience.html",
        title="Experience Details",
        experience=experience,
        tech_stack=tech_stack,
        bullet_points=bullet_points,
        links=experienceLinks,
    )
