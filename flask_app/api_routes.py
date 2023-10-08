from flask import Blueprint, jsonify

from flask_app.models import HomepageDetails, Link, load_user

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
    homepage_details_links_resp = [
        {"link_name": homepage_details_link.link_name, "url": homepage_details_link.url}
        for homepage_details_link in homepage_details_links
    ]

    resp = {
        "owner_username": homepage_details.owner.username,
        "creation_datetime": homepage_details.creation_datetime,
        "full_name": homepage_details.full_name,
        "email": homepage_details.email,
        "profile_picture_link": homepage_details.image_link,
        "description": homepage_details.description,
        "personal_links": homepage_details_links_resp,
        "long_description": homepage_details.long_description,
    }

    return jsonify(resp)
