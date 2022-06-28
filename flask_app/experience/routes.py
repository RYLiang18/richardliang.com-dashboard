from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for
)
from flask_app.experience.forms import CreateExperienceForm
from flask_login import(
    login_required,
    current_user
)
from flask_app.models import (
    Experience,
    load_user
)

experience_blueprint = Blueprint("experience", __name__, url_prefix="/experience", template_folder='./templates')

@experience_blueprint.route("/")
@login_required
def index():
    return render_template(
        "experience.html", title=f"{current_user.username}\'s experience"
    )

@experience_blueprint.route("/create_experience", methods=["GET", "POST"])
@login_required
def create_experience():
    create_experience_form = CreateExperienceForm()

    if create_experience_form.validate_on_submit():
        new_experience = Experience(
            owner = load_user(current_user.username),
            company_name = create_experience_form.company_name.data,
            position = create_experience_form.position.data,
            start_date = create_experience_form.start_date.data,
            end_date = create_experience_form.end_date.data,
            about = create_experience_form.about.data
        )
        new_experience.save()

        return redirect(url_for("experience.index"))

    return render_template(
        "create_experience.html",
        title = "Experience - Create Experience",
        form = create_experience_form
    )