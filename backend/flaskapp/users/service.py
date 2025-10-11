import jwt
import random
import logging
import datetime
from typing import Union, Tuple
from flask import jsonify, current_app, Response
from flaskapp import bcrypt, db
from flaskapp.caching import redis_client, RedisKeys
from flaskapp.users import model
from flaskapp.db_models import User
from flaskapp.users.messages import send_otp
from flaskapp.utils import response_body_validator
from flaskapp.exceptions import (
    UserEmailConflictError,
    UserUserNameConflictError,
    OtpRetryLimitError,
    OtpError,
    InternalServerError,
    AuthenticationError,
    UserNotFoundError,
)


# generate a random 6 digit code
def generate_otp() -> str:
    otp = random.randint(0, 999999)
    return f"{otp:06}"


# send verification code
def two_step_verification() -> Union[Response, Tuple[Response, int]]:
    validated = response_body_validator(model.SignUpRequest)

    # check username in db
    if User.check_name(validated.username):
        logging.warning(f"Username: {validated.username} already taken")
        raise UserUserNameConflictError()

    # check email in db
    if User.check_email(validated.email):
        logging.warning(f"Email: {validated.email} already taken")
        raise UserEmailConflictError()

    # Generate OTP and send it
    otp = generate_otp()
    send_otp(otp, validated.email)

    otp_key = RedisKeys.sign_up(validated.email)

    # too many request
    stored_otp = redis_client.get(otp_key)
    if stored_otp:
        logging.warning(f"Too many signup request for {validated.email}")
        raise OtpRetryLimitError()

    # store email and otp for 2 minutes
    redis_client.setex(otp_key, 60 * 2, otp)
    return jsonify({"message": "OTP sent to email"}), 200


# after verification save the user
def register_user() -> Union[Response, Tuple[Response, int]]:
    validated = response_body_validator(model.VerifyRequest)

    # check stored otp for given email in redis cache
    otp_key = RedisKeys.sign_up(validated.email)
    stored_otp = redis_client.get(otp_key)

    # check otp in redis client and if there is a otp, match with given otp
    if not stored_otp or stored_otp != validated.otp:
        raise OtpError()

    hashed_pass = bcrypt.generate_password_hash(validated.password, rounds=13).decode(
        "utf-8"
    )
    username = validated.username.replace(" ", "-").lower()

    try:
        user = User(username=username, email=validated.email, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        redis_client.delete(otp_key)
    except Exception as e:
        logging.error(f"User registration failed. Error: {str(e)}")
        raise InternalServerError()

    return jsonify({"message": "User created"}), 201


def get_user_by_email(email: str) -> User:
    try:
        user = User.query.filter_by(email=email).first()
        if user is None:
            logging.warning(f"User not found for email={email}")
            raise UserNotFoundError()
        return user
    except UserNotFoundError:
        raise
    except Exception as e:
        logging.error(f"Failed to get user. Error: {str(e)}")
        raise InternalServerError()


def authenticate_user(email, password) -> User:
    user = get_user_by_email(email)

    if not bcrypt.check_password_hash(user.password, password):
        logging.warning(f"Authentication failed password mitchmatched email={email}")
        raise AuthenticationError()
    return user


# login
def get_token() -> Union[Response, Tuple[Response, int]]:
    validated = response_body_validator(model.LogInRequest)
    user = authenticate_user(validated.email, validated.password)

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

    return jsonify({"username": user.username, "token": token}), 200


# reset password
def forgot_password() -> Union[Response, Tuple[Response, int]]:
    validated = response_body_validator(model.ResetPasswordRequest)

    otp_key = RedisKeys.reset_password(validated.email)
    # if otp already in cache than need to wait 2 minutes
    stored_otp = redis_client.get(otp_key)
    if stored_otp:
        logging.warning(f"Too many reset password request for {validated.email}")
        raise OtpRetryLimitError()

    # check if the user registered
    if not User.check_email(validated.email):
        logging.warning(f"User not found for reset password. email={validated.email}")
        raise UserNotFoundError()

    # Generate OTP and send it
    otp = generate_otp()
    send_otp(otp, validated.email)

    # if email sent than store the otp with email for 2 minutes
    redis_client.setex(otp_key, 60 * 2, otp)

    return jsonify({"message": "OTP sent to email"}), 200


# verify reset otp
def verify_reset_otp() -> Union[Response, Tuple[Response, int]]:
    validated = response_body_validator(model.VerifyResetOtpRequest)

    otp_key = RedisKeys.reset_password(validated.email)

    # check stored otp for given email in redis cache
    stored_otp = redis_client.get(otp_key)
    if not stored_otp or stored_otp != validated.otp:
        raise OtpError()

    return jsonify({"message": "Otp matched"}), 200


# change password
def change_password() -> Union[Response, Tuple[Response, int]]:
    validated = response_body_validator(model.ChangePasswordRequest)

    otp_key = RedisKeys.reset_password(validated.email)

    # check stored otp for given email in redis cache
    stored_otp = redis_client.get(otp_key)
    if not stored_otp or stored_otp != validated.otp:
        raise OtpError()

    try:
        # store new password in database
        user = User.query.filter_by(email=validated.email).first()
        hashed_pass = bcrypt.generate_password_hash(
            validated.password, rounds=13
        ).decode("utf-8")
        user.password = hashed_pass
        db.session.commit()
        redis_client.delete(validated.email)
    except Exception as e:
        logging.error(
            f"Failed to change password for email={validated.email}. Error: {str(e)}"
        )
        raise InternalServerError()

    return jsonify({"message": "Password changed"}), 200


# user profile
def user_profile(current_user) -> Union[Response, Tuple[Response, int]]:
    return jsonify({"name": current_user.username, "email": current_user.email}), 200
