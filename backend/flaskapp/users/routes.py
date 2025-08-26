import jwt
import datetime
from flaskapp.db_models import User
from flaskapp.users.messages import send_otp
from flaskapp import redis_client, bcrypt, db
from flask import Blueprint, jsonify, current_app
from flaskapp.users.utils import generate_otp
from flaskapp.utils import (
    login_required,
    logout_required,
    validate_request_json,
    MAX_NAME_LENGTH,
    MIN_NAME_LENGTH,
    MAX_EMAIL_LENGTH,
    MIN_EMAIL_LENGTH,
    EMAIL_REGEX,
    OTP_LENGTH,
    MIN_PASS_LENGTH,
    MAX_PASS_LENGTH,
    PASSWORD_REGEX,
)


# users blueprint
users_bp = Blueprint("users", __name__)


# =================================================================
# create user
@users_bp.route("/sign-up/", methods=["POST"])
@logout_required
@validate_request_json(
    {
        "name": {
            "required": True,
            "min_len": MIN_NAME_LENGTH,
            "max_len": MAX_NAME_LENGTH,
        },
        "email": {
            "required": True,
            "min_len": MIN_EMAIL_LENGTH,
            "max_len": MAX_EMAIL_LENGTH,
            "regex": EMAIL_REGEX,
        },
    }
)
def sign_up(name_stripped, email_stripped):
    # Check if username and email already exist
    errors = {}
    if User.check_name(name_stripped):
        errors["nameStatus"] = "Username already taken."

    if User.check_email(email_stripped):
        errors["emailStatus"] = "Email already taken."

    # 409 Conflict for duplicate entries
    if errors:
        return jsonify(errors), 409

    # Generate OTP and send it
    otp = generate_otp()
    is_sent = send_otp(otp, email_stripped)

    # email sent fail
    if not is_sent:
        return jsonify({"error": "Failed to send OTP."}), 500

    # if otp, try after 2 minutes
    stored_otp = redis_client.get(email_stripped)
    if stored_otp:
        return jsonify({"error": "Please try again after 2 minutes."}), 400

    # if email sent than store the otp with email for 2 minutes
    redis_client.setex(email_stripped, 120, otp)

    return jsonify({"message": "OTP sent to email."}), 200


# =================================================================
# verify signup otp and store the user in the database
@users_bp.route("/verify/", methods=["POST"])
@logout_required
@validate_request_json(
    {
        "otp": {"required": True, "min_len": OTP_LENGTH, "max_len": OTP_LENGTH},
        "name": {
            "required": True,
            "min_len": MIN_NAME_LENGTH,
            "max_len": MAX_NAME_LENGTH,
        },
        "email": {
            "required": True,
            "min_len": MIN_EMAIL_LENGTH,
            "max_len": MAX_EMAIL_LENGTH,
            "regex": EMAIL_REGEX,
        },
        "password": {
            "required": True,
            "min_len": MIN_PASS_LENGTH,
            "max_len": MAX_PASS_LENGTH,
            "regex": PASSWORD_REGEX,
        },
    }
)
def verify(otp_stripped, name_stripped, email_stripped, password_stripped):
    # check stored otp for given email in redis cache
    stored_otp = redis_client.get(email_stripped)

    # check otp in redis client and if there is a otp, match with given otp
    if not stored_otp or stored_otp != otp_stripped:
        return jsonify({"error": "Timeout or invalid OTP."}), 400

    if User.check_name(name_stripped):
        return jsonify({"error": "Username already taken."}), 400

    if User.check_email(email_stripped):
        return jsonify({"error": "Email already taken."}), 400

    # store in database
    hashed_pass = bcrypt.generate_password_hash(password_stripped, rounds=13).decode(
        "utf-8"
    )
    name_stripped = name_stripped.replace(" ", "-").lower()
    user = User(username=name_stripped, email=email_stripped, password=hashed_pass)
    db.session.add(user)
    db.session.commit()
    redis_client.delete(email_stripped)

    return jsonify({"message": "Signup successful."}), 200


# =================================================================
# login
@users_bp.route("/log-in/", methods=["POST"])
@logout_required
@validate_request_json(
    {
        "email": {
            "required": True,
            "min_len": MIN_EMAIL_LENGTH,
            "max_len": MAX_EMAIL_LENGTH,
            "regex": EMAIL_REGEX,
        },
        "password": {
            "required": True,
            "min_len": MIN_PASS_LENGTH,
            "max_len": MAX_PASS_LENGTH,
            "regex": PASSWORD_REGEX,
        },
    }
)
def log_in(email_stripped, password_stripped):
    # load user
    user = User.query.filter_by(email=email_stripped).first()
    if not user or not bcrypt.check_password_hash(user.password, password_stripped):
        return jsonify({"error": "Invalid credentials!"}), 400

    # create jwt token
    token = jwt.encode(
        {
            "id": user.id,
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(minutes=current_app.config["JWT_TIMEOUT_MINUTES"]),
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    data = {"username": user.username, "token": token}

    return jsonify(data), 200


# =================================================================
# reset password
@users_bp.route("/reset-password/", methods=["POST"])
@logout_required
@validate_request_json(
    {
        "email": {
            "required": True,
            "min_len": MIN_EMAIL_LENGTH,
            "max_len": MAX_EMAIL_LENGTH,
            "regex": EMAIL_REGEX,
        }
    }
)
def reset_password(email_stripped):
    # load user
    user = User.query.filter_by(email=email_stripped).first()
    if not user:
        return jsonify({"error": "Please check your email address."}), 400

    # if otp already in cache than need to wait 2 minutes
    stored_otp = redis_client.get(email_stripped)
    if stored_otp:
        return jsonify({"error": "Please try again after 2 minutes."}), 400

    # Generate OTP and send it
    otp = generate_otp()
    is_sent = send_otp(otp, email_stripped)
    if not is_sent:
        return jsonify({"error": "Failed to send OTP."}), 500

    # if email sent than store the otp with email for 2 minutes
    redis_client.setex(email_stripped, 120, otp)

    return jsonify({"message": "OTP sent to email."}), 200


# =================================================================
# verify reset otp
@users_bp.route("/verify-reset-otp/", methods=["POST"])
@logout_required
@validate_request_json(
    {
        "email": {
            "required": True,
            "min_len": MIN_EMAIL_LENGTH,
            "max_len": MAX_EMAIL_LENGTH,
            "regex": EMAIL_REGEX,
        },
        "otp": {"required": True, "min_len": OTP_LENGTH, "max_len": OTP_LENGTH},
    }
)
def verify_reset_otp(email_stripped, otp_stripped):
    # check stored otp for given email in redis cache
    stored_otp = redis_client.get(email_stripped)
    if not stored_otp or stored_otp != otp_stripped:
        return jsonify({"error": "Timeout or invalid OTP."}), 400

    return jsonify({"message": "Otp matched."}), 200


# =================================================================
# set new password
@users_bp.route("/new-password/", methods=["POST"])
@logout_required
@validate_request_json(
    {
        "email": {
            "required": True,
            "min_len": MIN_EMAIL_LENGTH,
            "max_len": MAX_EMAIL_LENGTH,
            "regex": EMAIL_REGEX,
        },
        "password": {
            "required": True,
            "min_len": MIN_PASS_LENGTH,
            "max_len": MAX_PASS_LENGTH,
            "regex": PASSWORD_REGEX,
        },
        "otp": {"required": True, "min_len": OTP_LENGTH, "max_len": OTP_LENGTH},
    }
)
def new_pass(email_stripped, otp_stripped, password_stripped):
    # check stored otp for given email in redis cache
    stored_otp = redis_client.get(email_stripped)
    if not stored_otp or stored_otp != otp_stripped:
        return jsonify({"error": "Timeout or invalid OTP."}), 400

    # store new password in database
    user = User.query.filter_by(email=email_stripped).first()
    hashed_pass = bcrypt.generate_password_hash(password_stripped, rounds=13).decode(
        "utf-8"
    )
    user.password = hashed_pass
    db.session.commit()
    redis_client.delete(email_stripped)

    return jsonify({"message": "Password changed."}), 200


# =================================================================
# account endpoint
@users_bp.route("/account/")
@login_required
def account(current_user):
    data = {"name": current_user.username, "email": current_user.email}

    return jsonify(data), 200
