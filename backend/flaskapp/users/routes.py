from flask import Blueprint
from flaskapp.users import service
from flaskapp.utils import login_required, logout_required


users_bp = Blueprint("users", __name__)


# create user
@users_bp.route("/sign-up/", methods=["POST"])
@logout_required
def sign_up():
    return service.two_step_verification()


# verify signup otp and store the user in the database
@users_bp.route("/verify/", methods=["POST"])
@logout_required
def verify():
    return service.register_user()


# login
@users_bp.route("/log-in/", methods=["POST"])
@logout_required
def log_in():
    return service.get_token()


# reset password
@users_bp.route("/reset-password/", methods=["POST"])
@logout_required
def reset_password():
    return service.forgot_password()


# verify reset otp
@users_bp.route("/verify-reset-otp/", methods=["POST"])
@logout_required
def verify_reset_otp():
    return service.verify_reset_otp()


# set new password
@users_bp.route("/new-password/", methods=["POST"])
@logout_required
def new_pass():
    return service.change_password()


# account endpoint
@users_bp.route("/account/")
@login_required
def account(current_user):
    return service.user_profile(current_user)
