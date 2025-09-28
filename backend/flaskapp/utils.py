import jwt
import logging
from flask import Flask
from functools import wraps
from flaskapp.db_models import User
from flask import request, current_app, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException
from flaskapp.exceptions import (
    RequestJsonError,
    TokenMissingError,
    TokenExpiredError,
    TokenInvalidError,
    TokenPrefixError,
    UserNotFoundError,
    InternalServerError,
    ForbiddenAuthError,
)


# error handler
def register_error_handlers(app: Flask):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {"error": e.description}
        return jsonify(response), e.code


# take pydantic model and validate a request
def response_body_validator(validator):
    try:
        validated = validator(**request.get_json())
        return validated
    except ValidationError as e:
        logging.error(f"Invalid request body. Error: {str(e)}")
        raise RequestJsonError()


# protected route
def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            logging.error("Token is missing!")
            raise TokenMissingError()

        # validate prefix
        if not auth_header.startswith(current_app.config["AUTH_PREFIX"]):
            logging.error("Invalid token prefix!")
            raise TokenPrefixError()

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            logging.error("Token is missing!")
            raise TokenMissingError()

        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )

            current_user = User.query.filter_by(id=data.get("id")).first()
            if not current_user:
                logging.error(f"User not found for token={token}")
                raise UserNotFoundError()
        except UserNotFoundError:
            raise
        except jwt.ExpiredSignatureError:
            logging.error(f"Token has expired! token={token}")
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            logging.error(f"Invalid token={token}")
            raise TokenInvalidError()
        except Exception as e:
            logging.error(f"Failed to validate jwt. Error {str(e)}")
            raise InternalServerError()

        return f(current_user, *args, **kwargs)

    return inner


# forbidden route for already authenticated user
def logout_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if "Authorization" in request.headers:
            auth_header = request.headers.get("Authorization")
            logging.warning(f"This token {auth_header} request a logged out route")
            raise ForbiddenAuthError()
        return f(*args, **kwargs)

    return inner
