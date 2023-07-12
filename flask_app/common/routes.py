from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from flask_app.common.forms import (
    SubmitLinkForm,
    SubmitSimpleStringContentForm,
    UpdateDateForm,
    UpdateImageLinkForm,
    UpdateLongDescriptionForm,
)
from flask_app.models import Experience, HomepageDetails, Link, StringContent, load_user
from flask_app.utils import current_time, translate

common_blueprint = Blueprint(
    "common", __name__, url_prefix="/common", template_folder="./templates"
)

link_parent_collections = [HomepageDetails, Experience]
string_content_parent_collections = [Experience]
model_map = {"HomepageDetails": HomepageDetails, "Experience": Experience}


# -- utility functions
# child document refers to either Link or StringContent
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


# -- routes --
@common_blueprint.route(
    "/update_date/<model>/<document_creation_datetime>/<property_name>",
    methods=["GET", "POST"],
)
@login_required
def update_date(model, document_creation_datetime, property_name):
    document = (
        model_map[model]
        .objects(
            owner=load_user(current_user.username),
            creation_datetime=document_creation_datetime,
        )
        .first()
    )

    if document is None:
        return render_template("404.html", title="🪦")

    update_date_form = UpdateDateForm(content=getattr(document, property_name))
    if update_date_form.validate_on_submit():
        document.update(**{property_name: update_date_form.content.data})
        return redirect(session["url"])

    return render_template(
        "submit_simple_content.html",
        form=update_date_form,
        title=f"Update {translate(document.__class__.__name__)} - {translate(property_name)}",
    )


@common_blueprint.route(
    "/update_image_link_property>/<model>/<document_creation_datetime>",
    methods=["GET", "POST"],
)
@login_required
def update_image_link_property(model, document_creation_datetime):
    document = (
        model_map[model]
        .objects(
            owner=load_user(current_user.username),
            creation_datetime=document_creation_datetime,
        )
        .first()
    )

    if document is None:
        return render_template("404.html", title="🪦")

    update_image_link_form = UpdateImageLinkForm(content=document.image_link)

    if update_image_link_form.validate_on_submit():
        document.update(image_link=update_image_link_form.content.data)
        return redirect(session["url"])

    return render_template(
        "submit_simple_content.html",
        form=update_image_link_form,
        title=f"Update {translate(document.__class__.__name__)} - Profile Picture",
    )


@common_blueprint.route(
    "/update_name_like_property/<model>/<document_creation_datetime>/<property_name>",
    methods=["GET", "POST"],
)
@login_required
def update_name_like_property(model, document_creation_datetime, property_name):
    document = (
        model_map[model]
        .objects(
            owner=load_user(current_user.username),
            creation_datetime=document_creation_datetime,
        )
        .first()
    )

    if document is None:
        return render_template("404.html", title="🪦")

    update_name_like_property_form = SubmitSimpleStringContentForm(
        content=getattr(document, property_name)
    )

    if update_name_like_property_form.validate_on_submit():
        document.update(**{property_name: update_name_like_property_form.content.data})

        return redirect(session["url"])

    return render_template(
        "submit_simple_content.html",
        form=update_name_like_property_form,
        title=f"Update {translate(document.__class__.__name__)} - {translate(property_name)}",
    )


@common_blueprint.route(
    "/create_link/<parent_model>/<parent_document_creation_datetime>",
    methods=["GET", "POST"],
)
@login_required
def create_link(parent_model, parent_document_creation_datetime=None):
    create_link_form = SubmitLinkForm()

    if create_link_form.validate_on_submit():
        parent_document = (
            model_map[parent_model]
            .objects(
                owner=load_user(current_user.username),
                creation_datetime=parent_document_creation_datetime,
            )
            .first()
        )

        new_link = Link(
            parent=parent_document,
            link_name=create_link_form.link_name.data,
            url=create_link_form.url.data,
            creation_datetime=current_time(),
        )

        new_link.save()
        return redirect(session["url"])

    return render_template(
        "submit_link.html",
        form=create_link_form,
        title=f"Create Link Form - {translate(parent_model)}",
    )


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
        return render_template("404.html", title="🪦")

    update_link_form = SubmitLinkForm(link_name=link.link_name, url=link.url)

    if update_link_form.validate_on_submit():
        link.update(
            link_name=update_link_form.link_name.data, url=update_link_form.url.data
        )
        return redirect(session["url"])

    return render_template(
        "submit_link.html", form=update_link_form, title="Update Link Form"
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
        return render_template("404.html", title="🪦")

    link.delete()

    return redirect(session["url"])


@common_blueprint.route(
    "/create_child_string_content/<parent_model>/<parent_document_creation_datetime>/<content_type>",
    methods=["GET", "POST"],
)
@login_required
def create_child_string_content(
    parent_model, parent_document_creation_datetime, content_type
):
    create_string_content_form = SubmitSimpleStringContentForm()

    if create_string_content_form.validate_on_submit():
        parent_document = (
            model_map[parent_model]
            .objects(
                owner=load_user(current_user.username),
                creation_datetime=parent_document_creation_datetime,
            )
            .first()
        )

        new_string_content_document = StringContent(
            parent=parent_document,
            content_type=content_type,
            content=create_string_content_form.content.data,
            creation_datetime=current_time(),
        )

        new_string_content_document.save()
        return redirect(session["url"])

    return render_template(
        "submit_simple_content.html",
        form=create_string_content_form,
        title=f"{translate(parent_model)} - Create {translate(content_type)}",
    )


@common_blueprint.route(
    "/update_child_string_content/<parent_document_creation_datetime>/<string_content_creation_datetime>/<content_type>",
    methods=["GET", "POST"],
)
@login_required
def update_child_string_content(
    parent_document_creation_datetime, string_content_creation_datetime, content_type
):
    child_string_content_document = get_child_document(
        parent_document_creation_datetime,
        string_content_creation_datetime,
        string_content_parent_collections,
        StringContent,
        content_type,
    )

    if child_string_content_document is None:
        return render_template("404.html", title="🪦")

    update_string_content_form = SubmitSimpleStringContentForm(
        content=child_string_content_document.content
    )

    if update_string_content_form.validate_on_submit():
        child_string_content_document.update(
            content=update_string_content_form.content.data
        )

        return redirect(session["url"])

    return render_template(
        "submit_simple_content.html",
        form=update_string_content_form,
        title=f"Update {translate(content_type)}",
    )


@common_blueprint.route(
    "/delete_string_content/<parent_document_creation_datetime>/<string_content_creation_datetime>/<content_type>",
    methods=["GET", "POST"],
)
@login_required
def delete_string_content(
    parent_document_creation_datetime, string_content_creation_datetime, content_type
):
    child_string_content_document = get_child_document(
        parent_document_creation_datetime,
        string_content_creation_datetime,
        string_content_parent_collections,
        StringContent,
        content_type,
    )

    if child_string_content_document is None:
        return render_template("404.html", title="🪦")

    child_string_content_document.delete()

    return redirect(session["url"])


@common_blueprint.route(
    "/update_long_description/<model>/<document_creation_datetime>",
    methods=["GET", "POST"],
)
@login_required
def update_long_description(model, document_creation_datetime):
    document = (
        model_map[model]
        .objects(
            owner=load_user(current_user.username),
            creation_datetime=document_creation_datetime,
        )
        .first()
    )

    if document is None:
        return render_template("404.html", title="🪦")

    update_long_description_form = UpdateLongDescriptionForm(
        content=document.long_description
    )

    if update_long_description_form.validate_on_submit():
        document.update(long_description=update_long_description_form.content.data)

        return redirect(session["url"])

    return render_template(
        "submit_long_description.html",
        form=update_long_description_form,
        title=f"Update {translate(document.__class__.__name__)} - Long Description",
    )
