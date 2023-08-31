from flask import Blueprint, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from flask_app.constants import bullet_type, technology_type
from flask_app.models import Link, Project, StringContent, load_user
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
        title=f"{current_user.username}'s projects",
        projects=projects,
    )


@projects_blueprint.route("/create_project", methods=["GET", "POST"])
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


@projects_blueprint.route("/view_project/<project_creation_datetime>", methods=["GET"])
@login_required
def view_project(project_creation_datetime):
    session["url"] = url_for(
        "projects.view_project",
        project_creation_datetime=project_creation_datetime,
    )
    project = Project.objects(
        owner=load_user(current_user.username),
        creation_datetime=project_creation_datetime,
    ).first()

    if project is None:
        return render_template("404.html", title="🪦")

    string_contents = {
        technology_type: StringContent.objects(
            parent=project, content_type=technology_type
        ),
        bullet_type: StringContent.objects(parent=project, content_type=bullet_type),
    }

    string_content_headers = {
        technology_type: "Tech Stack",
        bullet_type: "Bullet Points",
    }

    projectLinks = Link.objects(parent=project)

    return render_template(
        "view_project.html",
        title="Project Details",
        project=project,
        string_contents=string_contents,
        string_content_headers=string_content_headers,
        string_content_types=[technology_type, bullet_type],
        links=projectLinks,
    )
