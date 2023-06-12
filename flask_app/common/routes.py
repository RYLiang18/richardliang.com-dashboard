from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from flask_app.common.forms import (
    CreateLinkForm,
    CreateStringContentForm,
    UpdateLinkForm,
    UpdateNameForm,
    UpdateStringContentForm,
)
from flask_app.constants import bullet_type
from flask_app.models import Experience, HomepageDetails, Link, StringContent, load_user
from flask_app.utils import current_time

common_blueprint = Blueprint(
    "common", __name__, url_prefix="/common", template_folder="./templates"
)

link_parent_collections = [HomepageDetails, Experience]
string_content_parent_collections = [Experience]
model_map = {"homepage_details": HomepageDetails, "experience": Experience}


@common_blueprint.route(
    "/update_property/<model>/<document_creation_datetime>/<property_name>"
)
@login_required()
def update_name_property(model, document_creation_datetime, property_name):
    document = model_map[model].objects(
        owner=load_user(current_user), creation_datetime=document_creation_datetime
    )
    if document is None:
        # TODO: return 404
        pass

    update_name_form = UpdateNameForm(name=document.name)
    # left off here


@common_blueprint.route(
    "/create_link/<parent_model>/<parent_document_creation_datetime>",
    methods=["GET", "POST"],
)
@login_required
def create_link(parent_model, parent_document_creation_datetime=None):
    create_link_form = CreateLinkForm()

    if create_link_form.validate_on_submit():
        parent_document = None
        if parent_model == "HomepageDetails":
            parent_document = HomepageDetails.objects(
                owner=load_user(current_user.username),
                creation_datetime=parent_document_creation_datetime,
            ).first()
        elif parent_model == "Experience":
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

        new_link.save()
        return redirect(session["url"])

    return render_template(
        "create_link.html",
        form=create_link_form,
        title=f"Create Link Form - {parent_model}",
    )


def get_child_document(
    parent_document_creation_datetime,
    child_document_creation_datetime,
    parent_collections,
    target_collection,
    string_content_type="",
):
    parent_document = None
    for parent_collection in parent_collections:
        parent_document = parent_collection.objects(
            owner=load_user(current_user.username),
            creation_datetime=parent_document_creation_datetime,
        ).first()
        if parent_document is not None:
            break
    if target_collection == Link:
        return target_collection.objects(
            parent=parent_document, creation_datetime=child_document_creation_datetime
        ).first()
    elif target_collection == StringContent:
        return target_collection.objects(
            parent=parent_document,
            creation_datetime=child_document_creation_datetime,
            content_type=string_content_type,
        ).first()


@common_blueprint.route(
    "/update_link/<parent_document_creation_datetime>/<link_creation_datetime>",
    methods=["GET", "POST"],
)
@login_required
def update_link(parent_document_creation_datetime, link_creation_datetime):
    # finding the parent
    link = get_child_document(
        parent_document_creation_datetime,
        link_creation_datetime,
        link_parent_collections,
        Link,
    )

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


@common_blueprint.route(
    "/delete_link/<parent_document_creation_datetime>/<link_creation_datetime>",
    methods=["GET", "POST"],
)
@login_required
def delete_link(parent_document_creation_datetime, link_creation_datetime):
    link = get_child_document(
        parent_document_creation_datetime,
        link_creation_datetime,
        link_parent_collections,
        Link,
    )

    if link is None:
        # TODO: return 404
        pass

    link.delete()

    return redirect(session["url"])


@common_blueprint.route(
    "/create_string_content/<parent_model>/<parent_document_creation_datetime>/<content_type>",
    methods=["GET", "POST"],
)
@login_required
def create_string_content(
    parent_model, parent_document_creation_datetime, content_type
):
    create_string_content_form = CreateStringContentForm()

    if create_string_content_form.validate_on_submit():
        parent_document = None

        if parent_model == "Experience":
            parent_document = Experience.objects(
                owner=load_user(current_user.username),
                creation_datetime=parent_document_creation_datetime,
            ).first()

        new_string_content_document = StringContent(
            parent=parent_document,
            content_type=content_type,
            content=create_string_content_form.content.data,
            creation_datetime=current_time(),
        )

        new_string_content_document.save()
        return redirect(session["url"])

    return render_template(
        "create_string_content.html",
        form=create_string_content_form,
        title=f"{parent_model} - Create {content_type}",
    )


@common_blueprint.route(
    "/update_string_content/<parent_document_creation_datetime>/<string_content_creation_datetime>/<content_type>",
    methods=["GET", "POST"],
)
@login_required
def update_string_content(
    parent_document_creation_datetime, string_content_creation_datetime, content_type
):
    string_content_document = get_child_document(
        parent_document_creation_datetime,
        string_content_creation_datetime,
        string_content_parent_collections,
        StringContent,
        content_type,
    )

    if string_content_document is None:
        # TODO: return 404
        pass

    update_string_content_form = UpdateStringContentForm(
        content=string_content_document.content
    )

    if update_string_content_form.validate_on_submit():
        string_content_document.update(content=update_string_content_form.content.data)

        return redirect(session["url"])

    return render_template(
        "update_string_content.html",
        form=update_string_content_form,
        title=f"Update {content_type}",
    )


@common_blueprint.route(
    "/delete_string_content/<parent_document_creation_datetime>/<string_content_creation_datetime>/<content_type>",
    methods=["GET", "POST"],
)
@login_required
def delete_string_content(
    parent_document_creation_datetime, string_content_creation_datetime, content_type
):
    string_content_document = get_child_document(
        parent_document_creation_datetime,
        string_content_creation_datetime,
        string_content_parent_collections,
        StringContent,
        content_type,
    )

    if string_content_document is None:
        # TODO: return 404
        pass

    string_content_document.delete()

    return redirect(session["url"])
