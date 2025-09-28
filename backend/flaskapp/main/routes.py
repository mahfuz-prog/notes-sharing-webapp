from flask import Blueprint
from flaskapp.main import service


# main blueprint
main_bp = Blueprint("main", __name__)


@main_bp.route("/home/")
def home():
    return service.homepage_stats()


@main_bp.route("/single-note/", methods=["POST"])
def single_note():
    return service.get_single_note()


@main_bp.route("/user-profile/<string:username>/")
def user_profile(username):
    return service.get_user_note_list(username)
