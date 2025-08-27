import re
import jwt
from flask import Flask
from functools import wraps
from flaskapp.db_models import User
from flask import request, current_app, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {"error": e.description}
        return jsonify(response), e.code


# ===============================================
# protected route
def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Token is missing!"}), 401

        # check the secret to ensure only the request is coming only from our frontend
        if auth_header.startswith(current_app.config["AUTH_PREFIX"]):
            token = auth_header.split(" ")[1]

        # if no token found
        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        # loading data from jwt can throw exceptions
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = User.query.filter_by(id=data.get("id")).first()
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401

        # return user with args and kwargs to access in route
        return f(current_user, *args, **kwargs)

    return inner


# ===============================================
# forbidden route for already authenticated user
def logout_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if "Authorization" in request.headers:
            return jsonify({"error": "Forbidden response!"}), 403
        return f(*args, **kwargs)

    return inner


# =======================================
# Constants for users Validation
MAX_NAME_LENGTH = 20
MIN_NAME_LENGTH = 3
MAX_EMAIL_LENGTH = 254
MIN_EMAIL_LENGTH = 5
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
OTP_LENGTH = 6
MIN_PASS_LENGTH = 8
MAX_PASS_LENGTH = 20
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,20}$")

# Constants for notes validation
MAX_NOTE_ID_LENGTH = 7
MIN_TITLE_LENGTH = 1
MAX_TITLE_LENGTH = 100
MIN_TEXT_LENGTH = 1
MAX_TEXT_LENGTH = 20000
MIN_PIN_LENGTH = 3
MAX_PIN_LENGTH = 8


# validator decorator
def validate_request_json(fields_to_validate):
    """
    Decorator to validate incoming JSON request data against specified rules.
    Passed validated and stripped fields as keyword arguments to the decorated function.

    Args:
            { 'email': {'required': True, 'min_len': MIN_EMAIL_LENGTH, 'max_len': MAX_EMAIL_LENGTH, 'regex': EMAIL_REGEX} }
            { 'required': bool, 'min_len': int, 'max_len': int, 'regex': re.Pattern }
    """

    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            response_data = request.get_json()

            # check for empty JSON body
            if not response_data:
                return jsonify({"error": "Request must be JSON."}), 400

            validated_stripped_data = {}
            validation_errors = []

            # loop over all given items
            for field_name, rules in fields_to_validate.items():
                value = response_data.get(field_name)
                is_required = rules.get("required", False)
                min_len = rules.get("min_len")
                max_len = rules.get("max_len")
                regex = rules.get("regex")

                stripped_value = None
                if value is not None:
                    stripped_value = str(value).strip()

                # 1. Check if required and empty
                if is_required and (stripped_value is None or stripped_value == ""):
                    validation_errors.append(
                        f"{field_name.capitalize()} cannot be empty."
                    )
                    # Skip further validation for this field if it's empty and required
                    continue

                # Only proceed with length/regex if a non-empty value is provided
                if stripped_value is not None and stripped_value != "":
                    # Minimum length validation
                    if min_len is not None and len(stripped_value) < min_len:
                        validation_errors.append(
                            f"{field_name.capitalize()} must be at least {min_len} characters."
                        )
                        continue

                    # Maximum length validation
                    if max_len is not None and len(stripped_value) > max_len:
                        validation_errors.append(
                            f"{field_name.capitalize()} must be at most {max_len} characters."
                        )
                        continue

                    # Regex validation (email, password)
                    if regex and not regex.fullmatch(stripped_value):
                        validation_errors.append(f"Invalid {field_name} format.")
                        continue

                # Store the processed/stripped value
                validated_stripped_data[f"{field_name}_stripped"] = stripped_value

            if validation_errors:
                # Return the first encountered error message, as per original style
                return jsonify({"error": validation_errors[0]}), 400

            # Pass validated and stripped data as keyword arguments to the route function
            return f(*args, **kwargs, **validated_stripped_data)

        return inner

    return decorator


def validate_pydantic(model_class):
    """Flask decorator to validate JSON request using a Pydantic model"""

    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            try:
                json_data = request.get_json()
                if not json_data:
                    return jsonify({"error": "Request must be JSON."}), 400

                validated_data = model_class(**json_data)
            except ValidationError as e:
                # Return first error message
                first_error = e.errors()[0]
                field = first_error.get("loc")[0]
                msg = first_error.get("msg")
                return jsonify({"error": f"{field}: {msg}"}), 400

            # Pass validated Pydantic object to route
            return f(*args, **kwargs, validated_data=validated_data)

        return inner

    return decorator
