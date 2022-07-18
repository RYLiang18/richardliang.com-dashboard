from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)
from flask_login import(
    current_user,
    login_user,
    logout_user,
    login_required
)
from flask_app.users.forms import(
    LoginForm
)
from flask_app.models import (
    User,
    HomepageDetails,
    load_user
)
from flask_app import bcrypt, ipsum

users_blueprint = Blueprint("users", __name__, template_folder='./templates')

def new_default_homepage():
    current_time = datetime.now().strftime("%B%d%Y%H%M%S%f")
    default_homepage_details = HomepageDetails(
        owner = load_user(current_user.username),
        full_name = "Replace with your full name",
        email = "your_email@example.com",
        pfp_link = "https://i.imgur.com/rdKHsyK.jpg",
        description = "replace me with a short description of yourself",
        about_me = ipsum(),
        creation_time=current_time
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