from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)
from flask_login import(
    login_required,
    current_user
)
from flask_app.models import (
    HomepageDetails, 
    load_user,
    Link
)
from flask_app.homepage.forms import (
    FullNameUpdateForm,
    PFPLinkUpdateForm,
    DescriptionUpdateForm,
    PersonalLinkAddForm,
    PersonalLinkUpdateForm,
    AboutMeUpdateForm,
    EmailUpdateForm
)
from flask_app.utils import current_time

homepage_blueprint = Blueprint("homepage", __name__, url_prefix='/homepage', template_folder='./templates')

def matching_username(username):
    return current_user.username == username

@homepage_blueprint.route("/")
@login_required
def index():
    homepage_details = HomepageDetails.objects(
        owner=load_user(current_user.username)
    ).first()

    return render_template(
        "homepage.html", 
        title=f"{current_user.username}\'s homepage",
        homepage_details = homepage_details
    )

@homepage_blueprint.route("/update_full_name", methods=["GET", "POST"])
@login_required
def update_full_name():
    full_name_update_form = FullNameUpdateForm()
    if full_name_update_form.validate_on_submit():
        homepage_details = HomepageDetails.objects(owner=current_user).first()
        homepage_details.update(full_name = full_name_update_form.full_name.data)

        return redirect(url_for('homepage.index'))
    
    return render_template(
        "update_full_name.html", form=full_name_update_form, title="Homepage - Update Full Name"
    )

@homepage_blueprint.route("/update_email", methods=["GET", "POST"])
@login_required
def update_email():
    email_update_form = EmailUpdateForm()

    if email_update_form.validate_on_submit():
        homepage_details = HomepageDetails.objects(owner=current_user).first()
        homepage_details.update(email = email_update_form.email.data)

        return redirect(url_for('homepage.index'))
    
    return render_template(
        "update_email.html", form=email_update_form, title="Homepage - Update Email"
    )


@homepage_blueprint.route("/update_pfp_link", methods=["GET", "POST"])
@login_required
def update_pfp_link():
    pfp_link_update_form = PFPLinkUpdateForm()

    if pfp_link_update_form.validate_on_submit():
        homepage_details = HomepageDetails.objects(owner=current_user).first()
        homepage_details.update(pfp_link = pfp_link_update_form.url.data)

        return redirect(url_for('homepage.index'))
    
    return render_template(
        "update_pfp_link.html", form=pfp_link_update_form, title="Homepage - Update PFP Link"
    )

@homepage_blueprint.route("/update_description", methods=["GET", "POST"])
@login_required
def update_description():
    homepage_details = HomepageDetails.objects(owner=current_user).first()

    description_update_form = DescriptionUpdateForm(
        description = homepage_details.description
    )

    if description_update_form.validate_on_submit():
        homepage_details.update(description = description_update_form.description.data)

        return redirect(url_for('homepage.index'))
    
    return render_template(
        "update_description.html", form=description_update_form, title="Homepage - Update Description"
    )

@homepage_blueprint.route(
    "/update_link/<link_owner_username>/<link_datetime_str>", methods=["GET", "POST"]
)
@login_required
def update_personal_link(link_owner_username, link_datetime_str):
    # // KEEP OTHERS FROM EDITING YOUR LINKS! ////
    if current_user.username != link_owner_username:
        flash("You can\'t edit someone else\'s link!")
        return redirect(url_for('homepage.index'))
    # ////////////////////////////////////////////
    
    personal_link = Link.objects(
        owner=load_user(link_owner_username), datetime_str = link_datetime_str
    ).first()
    
    personal_link_update_form = PersonalLinkUpdateForm(
        link_name = personal_link.link_name,
        url = personal_link.url
    )

    if personal_link_update_form.validate_on_submit():
        personal_link.update(
            link_name = personal_link_update_form.link_name.data,
            url = personal_link_update_form.url.data
        )

        return redirect(url_for('homepage.index'))

    return render_template(
        "update_personal_link.html", form=personal_link_update_form, title="Homepage - Update Personal Link"
    )


@homepage_blueprint.route(
    "/delete_link/<link_owner_username>/<link_datetime_str>", methods=["GET"]
)
@login_required
def delete_personal_link(link_owner_username, link_datetime_str):
    # // KEEP OTHERS FROM EDITING YOUR LINKS! ////
    if current_user.username != link_owner_username:
        flash("You can\'t edit someone else\'s link!")
        return redirect(url_for('homepage.index'))
    # ////////////////////////////////////////////

    # delete the link
    personal_link = Link.objects(
        owner=load_user(link_owner_username), datetime_str = link_datetime_str
    ).first()
    personal_link_pk = personal_link.pk
    personal_link.delete()

    # delete the link from homepage_details
    # there is no cascading delete in mongodb I guess
    HomepageDetails.objects().update_one(pull__links=personal_link_pk)

    return redirect(url_for('homepage.index'))

@homepage_blueprint.route("/add_link", methods=["GET", "POST"])
@login_required
def add_personal_link():
    link_add_form = PersonalLinkAddForm()

    if link_add_form.validate_on_submit():
        new_link = Link(
            owner = load_user(current_user.username),
            link_name = link_add_form.link_name.data,
            url = link_add_form.url.data,
            datetime_str = current_time()
        )
        new_link.save()

        homepage_details = HomepageDetails.objects(owner=current_user).first()
        homepage_details.links.append(new_link)
        homepage_details.save()

        return redirect(url_for('homepage.index'))
    
    return render_template(
        "add_personal_link.html", form=link_add_form, title="Homepage - Add New Link"
    )

@homepage_blueprint.route("/update_about_me", methods=["GET", "POST"])
@login_required
def update_about_me():
    homepage_details = HomepageDetails.objects(owner=current_user).first()

    about_me_update_form = AboutMeUpdateForm(
        about_me = homepage_details.about_me
    )

    if about_me_update_form.validate_on_submit():
        homepage_details.update(
            about_me = about_me_update_form.about_me.data
        )

        return redirect(url_for('homepage.index'))
    
    return render_template(
        "update_about_me.html", form=about_me_update_form, title="Homepage - Update About Me"
    )