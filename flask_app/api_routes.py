from flask import Blueprint, jsonify

from flask_app.constants import bullet_type, technology_type
from flask_app.models import (
    Experience,
    HomepageDetails,
    Link,
    Project,
    StringContent,
    load_user,
)

api_blueprint = Blueprint("api", __name__, url_prefix="/api")


@api_blueprint.route("/homepage_details/<username>", methods=["GET"])
def homepage_details(username):
    homepage_details = HomepageDetails.objects(owner=load_user(username)).first()

    if homepage_details is None:
        return jsonify(
            {
                "error": f"homepage details document not found. The user [{username}] may not exist, or they may not have initiated a homepage yet"
            }
        )

    homepage_details_links = Link.objects(parent=homepage_details)

    return jsonify(
        {
            "owner_username": homepage_details.owner.username,
            "creation_datetime": homepage_details.creation_datetime,
            "full_name": homepage_details.full_name,
            "email": homepage_details.email,
            "profile_picture_link": homepage_details.image_link,
            "description": homepage_details.short_description,
            "personal_links": [
                {
                    "link_name": link.link_name,
                    "url": link.url,
                }
                for link in homepage_details_links
            ],
            "long_description_b64": homepage_details.long_description_b64,
        }
    )


@api_blueprint.route("/experiences/<username>", methods=["GET"])
def experiences(username):
    experiences = Experience.objects(owner=load_user(username))
    return jsonify(
        {
            "experiences": [
                {
                    "owner_username": experience.owner.username,
                    "creation_datetime": experience.creation_datetime,
                    "company_name": experience.company_name,
                    "position": experience.position,
                    "start_date": experience.start_date,
                    "end_date": experience.end_date,
                    "image_link": experience.image_link,
                }
                for experience in experiences
            ]
        }
    )


@api_blueprint.route("/one_experience/<username>/<creation_datetime>", methods=["GET"])
def one_experience(username, creation_datetime):
    experience = Experience.objects(
        owner=load_user(username), creation_datetime=creation_datetime
    ).first()

    experience_links = Link.objects(parent=experience)
    experience_technologies = StringContent.objects(
        parent=experience, content_type=technology_type
    )
    experience_bullets = StringContent.objects(
        parent=experience, content_type=bullet_type
    )

    return jsonify(
        {
            "experience": {
                "owner_username": experience.owner.username,
                "creation_datetime": experience.creation_datetime,
                "company_name": experience.company_name,
                "position": experience.position,
                "start_date": experience.start_date,
                "end_date": experience.end_date,
                "image_link": experience.image_link,
                "links": [
                    {"link_name": link.link_name, "url": link.url}
                    for link in experience_links
                ],
                "tech_stack": [
                    technology.content for technology in experience_technologies
                ],
                "bullets": [bullet.content for bullet in experience_bullets],
                "long_description_b64": experience.long_description_b64,
            }
        }
    )


@api_blueprint.route("/projects/<username>", methods=["GET"])
def projects(username):
    projects = Project.objects(owner=load_user(username))
    return jsonify(
        {
            "projects": [
                {
                    "owner_username": project.owner.username,
                    "creation_datetime": project.creation_datetime,
                    "project_name": project.project_name,
                    "start_date": project.start_date,
                    "end_date": project.end_date,
                    "image_link": project.image_link,
                }
                for project in projects
            ]
        }
    )


@api_blueprint.route("/one_project/<username>/<creation_datetime>", methods=["GET"])
def one_project(username, creation_datetime):
    project = Project.objects(
        owner=load_user(username), creation_datetime=creation_datetime
    ).first()

    project_links = Link.objects(parent=project)
    project_technologies = StringContent.objects(
        parent=project, content_type=technology_type
    )
    project_bullets = StringContent.objects(parent=project, content_type=bullet_type)

    return jsonify(
        {
            "project": {
                "owner_username": project.owner.username,
                "creation_datetime": project.creation_datetime,
                "project_name": project.project_name,
                "start_date": project.start_date,
                "end_date": project.end_date,
                "image_link": project.image_link,
                "links": [
                    {"link_name": link.link_name, "url": link.url}
                    for link in project_links
                ],
                "tech_stack": [
                    technology.content for technology in project_technologies
                ],
                "bullets": [bullet.content for bullet in project_bullets],
                "long_description_b64": project.long_description_b64,
            }
        }
    )
