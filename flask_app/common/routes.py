from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from flask_app.models import (
    Experience,
    HomepageDetails,
    HomepageDetailsLink,
    ExperienceLink,
    ExperienceBullet,
    load_user,
    Link,
)
from flask_app.common.forms import (
    CreateLinkForm,
    UpdateLinkForm,
    CreateContentForm,
    UpdateContentForm,
)
from flask_app.utils import current_time

common_blueprint = Blueprint(
    "common", __name__, url_prefix="/common", template_folder="./templates"
)

parent_collections = [HomepageDetails, Experience]
link_collections = [HomepageDetailsLink, ExperienceLink]
bullet_collections = [ExperienceBullet]


@common_blueprint.route(
    "/create_link/<link_model>",
    methods=["GET", "POST"],
    defaults={"parent_document_creation_datetime": None},
)
@common_blueprint.route(
    "/create_link/<link_model>/<parent_document_creation_datetime>",
    methods=["GET", "POST"],
)
@login_required
def create_link(link_model, parent_document_creation_datetime=None):
    create_link_form = CreateLinkForm()

    if create_link_form.validate_on_submit():
        parent_document = None
        if link_model == "HomepageDetailsLink":
            parent_document = HomepageDetails.objects(
                owner=load_user(current_user.username),
                creation_datetime=parent_document_creation_datetime,
            ).first()
        elif link_model == "ExperienceLink":
            parent_document = Experience.objects(
                owner=load_user(current_user.username),
                creation_datetime=parent_document_creation_datetime,
            ).first()

        new_link = Link(
            parent=parent_document,
            link_name=create_link_form.link_name.data,
            url=create_link_form.url.data,
            creation_datetime=current_time(),
        )

        #     new_link = HomepageDetailsLink(
        #         owner=load_user(current_user.username),
        #         link_name=create_link_form.link_name.data,
        #         url=create_link_form.url.data,
        #         creation_datetime=current_time(),
        #     )

        # # CASE: Experience
        # elif link_model == "ExperienceLink":
        #     related_experience = Experience.objects(
        #         owner=load_user(current_user.username),
        #         creation_datetime=related_document_creation_date,
        #     ).first()

        #     new_link = ExperienceLink(
        #         owner=load_user(current_user.username),
        #         link_name=create_link_form.link_name.data,
        #         url=create_link_form.url.data,
        #         creation_datetime=current_time(),
        #         experience=related_experience,
        #     )

        new_link.save()
        return redirect(session["url"])

    return render_template(
        "create_link.html",
        form=create_link_form,
        title=f"Create Link Form - {link_model}",
    )


def get_link_document(parent_document_creation_datetime, link_creation_datetime):
    parent_document = None
    for parent_collection in parent_collections:
        parent_document = parent_collection.objects(
            owner=load_user(current_user.username),
            creation_datetime=parent_document_creation_datetime,
        ).first()
        if parent_document is not None:
            break
    return Link.objects(
        parent=parent_document, creation_datetime=link_creation_datetime
    ).first()


@common_blueprint.route(
    "/update_link/<parent_document_creation_datetime>/<link_creation_datetime>",
    methods=["GET", "POST"],
)
@login_required
def update_link(parent_document_creation_datetime, link_creation_datetime):
    # finding the parent
    link = get_link_document(parent_document_creation_datetime, link_creation_datetime)

    if link is None:
        # TODO: return 404
        pass

    update_link_form = UpdateLinkForm(link_name=link.link_name, url=link.url)

    if update_link_form.validate_on_submit():
        link.update(
            link_name=update_link_form.link_name.data, url=update_link_form.url.data
        )
        return redirect(session["url"])

    return render_template(
        "update_link.html", form=update_link_form, title="Update Link Form"
    )
    # link = None
    # for link_collection in link_collections:
    #     link = link_collection.objects(
    #         owner=load_user(current_user.username), creation_datetime=link_creation_datetime
    #     ).first()

    #     if link is not None:
    #         break

    # if link is None:
    #     # TODO: return 404
    #     pass

    # update_link_form = UpdateLinkForm(link_name=link.link_name, url=link.url)

    # if update_link_form.validate_on_submit():
    #     link.update(
    #         link_name=update_link_form.link_name.data, url=update_link_form.url.data
    #     )

    #     return redirect(session["url"])

    # return render_template(
    #     "update_link.html", form=update_link_form, title="Update Link Form"
    # )


@common_blueprint.route(
    "/delete_link/<parent_document_creation_datetime>/<link_creation_datetime>",
    methods=["GET", "POST"],
)
@login_required
def delete_link(parent_document_creation_datetime, link_creation_datetime):
    link = get_link_document(parent_document_creation_datetime, link_creation_datetime)

    if link is None:
        # TODO: return 404
        pass

    if link is None:
        # TODO: return 404
        pass
    # for link_collection in link_collections:
    #     link = link_collection.objects(
    #         owner=load_user(current_user.username), creation_datetime=link_creation_datetime
    #     ).first()

    #     if link is not None:
    #         break

    # if link is None:
    #     # TODO: return 404
    #     pass

    link.delete()

    return redirect(session["url"])


@common_blueprint.route(
    "/create_bullet/<bullet_model>/<related_document_creation_date>",
    methods=["GET", "POST"],
)
@login_required
def create_bullet(bullet_model, related_document_creation_date):
    create_bullet_form = CreateContentForm()

    if create_bullet_form.validate_on_submit():
        new_bullet = None

        if bullet_model == "ExperienceBullet":
            related_experience = Experience.objects(
                owner=load_user(current_user.username),
                creation_datetime=related_document_creation_date,
            ).first()

            new_bullet = ExperienceBullet(
                owner=load_user(current_user.username),
                creation_datetime=current_time(),
                experience=related_experience,
                content=create_bullet_form.content.data,
            )

        # TODO: 2nd case - Projects Bullet

        new_bullet.save()
        return redirect(session["url"])

    return render_template(
        "create_bullet.html",
        form=create_bullet_form,
        title=f"Create Link Form - {bullet_model}",
    )


@common_blueprint.route(
    "/update_bullet/<bullet_creation_datetime>", methods=["GET", "POST"]
)
@login_required
def update_bullet(bullet_creation_datetime):
    bullet = None
    for bullet_collection in bullet_collections:
        bullet = bullet_collection.objects(
            owner=load_user(current_user.username),
            creation_datetime=bullet_creation_datetime,
        ).first()

        if bullet is not None:
            break

    if bullet is None:
        # TODO: return 404
        pass

    update_bullet_form = UpdateContentForm(content=bullet.content)

    if update_bullet_form.validate_on_submit():
        bullet.update(content=update_bullet_form.content.data)

        return redirect(session["url"])

    return render_template(
        "update_bullet.html", form=update_bullet_form, title="Update Bullet Form"
    )


@common_blueprint.route(
    "/delete_bullet/<bullet_creation_datetime>", methods=["GET", "POST"]
)
@login_required
def delete_bullet(bullet_creation_datetime):
    bullet = None
    for bullet_collection in bullet_collections:
        bullet = bullet_collection.objects(
            owner=load_user(current_user.username),
            creation_datetime=bullet_creation_datetime,
        ).first()

        if bullet is not None:
            break

    if bullet is None:
        # TODO: return 404
        pass

    bullet.delete()

    return redirect(session["url"])


@common_blueprint.route(
    "/create_technology/<technology_model>/<related_document_creation_date>",
    methods=["GET", "POST"],
)
@login_required
def create_technology(technology_model, related_document_creation_date):
    create_technology_form = CreateContentForm()

    if create_technology_form.validate_on_submit():
        new_technology = None

        if technology_model == "ExperienceTechnology":
            pass
            # TODO: left off here
