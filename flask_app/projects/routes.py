from flask import Blueprint, render_template
from flask_login import current_user, login_required

from flask_app.models import Project

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
