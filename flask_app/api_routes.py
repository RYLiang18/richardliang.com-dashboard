from flask import Blueprint, jsonify

from flask_app.models import HomepageDetails, load_user

api_blueprint = Blueprint("api", __name__, url_prefix="/api")


@api_blueprint.route("/view_homepage_details/<username>", methods=["GET"])
def view_homepage_details(username):
    homepage_details = HomepageDetails.objects(owner=load_user(username)).first()

    if homepage_details is None:
        return jsonify(
            {
                "error": f"homepage details document not found. The user [{username}] may not exist, or they may not have a homepage yet"
            }
        )

    resp = {
        "full_name": homepage_details.full_name,
        "email": homepage_details.email,
        "image_link": homepage_details.image_link,
        "description": homepage_details.description,
        "long_description": homepage_details.long_description,
    }

    return jsonify(resp)
