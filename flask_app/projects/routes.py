from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from flask_app.models import Project, load_user
from flask_app.projects.forms import CreateProjectForm
from flask_app.utils import current_time

projects_blueprint = Blueprint(
    "projects", __name__, url_prefix="/projects", template_folder="./templates"
)


@projects_blueprint.route("/")
@login_required
def index():
    projects = Project.objects()

    return render_template(
        "projects.html",
        title=f"{current_user.username}'s experiences",
        projects=projects,
    )


@projects_blueprint.route("/create_experience", methods=["GET", "POST"])
@login_required
def create_project():
    create_project_form = CreateProjectForm()
    if create_project_form.validate_on_submit():
        new_project = Project(
            owner=load_user(current_user.username),
            project_name=create_project_form.project_name.data,
            start_date=create_project_form.start_date.data,
            end_date=create_project_form.end_date.data,
            image_link="https://i.imgur.com/nMIu8OU.jpg",
            long_description=create_project_form.long_description.data,
            creation_datetime=current_time(),
        )
        new_project.save()

        return redirect(url_for("projects.index"))

    return render_template(
        "create_project.html",
        title="Projects - Create Project",
        form=create_project_form,
    )
