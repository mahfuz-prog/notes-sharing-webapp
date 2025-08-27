from flask import Blueprint, jsonify
from flaskapp.main import service


# main blueprint
main_bp = Blueprint("main", __name__)


@main_bp.route("/home/")
def home():
    return jsonify(service.homepage_stats()), 200


@main_bp.route("/single-note/", methods=["POST"])
def single_note():
    """
    request json
    {username: "", note_id: "", Optional[pin: ""]}
    """
    return jsonify(service.get_single_note()), 200


@main_bp.route("/user-profile/<string:username>/")
def user_profile(username):
    return jsonify(service.get_user_note_list(username)), 200
