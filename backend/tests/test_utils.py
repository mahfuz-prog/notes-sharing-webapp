import jwt
import time
import datetime
from flask import current_app


# test logout_required decorator from signup route
def test_logout_required(client):
    headers = {"Authorization": "basic thisisavalidtokenfortesting"}
    response = client.post("/api-v1/users/sign-up/", headers=headers)
    assert response.status_code == 403
    assert response.get_json().get("error") == "Forbidden response!"


# take pydantic model and validate the request data
def test_response_body_validator(client):
    payload = {
        "username": "name",
        "email": "test_email",
    }
    response = client.post("/api-v1/users/sign-up/", json=payload)
    assert response.status_code == 400
    assert response.get_json().get("error") == "Bad request"


# test login_required decorator from account route
def test_login_required(client, monkeypatch):
    # without authorization header
    response = client.get("/api-v1/users/account/")
    assert response.status_code == 401
    assert response.get_json().get("error") == "Token is missing!"

    # invalid prefix
    headers = {"Authorization": "invalid thisisavalidtokenfortesting"}
    response = client.get("/api-v1/users/account/", headers=headers)
    assert response.status_code == 401
    assert response.get_json().get("error") == "Invalid token prefix!"

    # only prefix
    headers = {"Authorization": "basic "}
    response = client.get("/api-v1/users/account/", headers=headers)
    assert response.status_code == 401
    assert response.get_json().get("error") == "Invalid token!"

    # create a token
    token = jwt.encode(
        {
            "id": 9999999,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=1),
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    # Token expired
    time.sleep(1)
    headers = {"Authorization": f"basic {token}"}
    response = client.get("/api-v1/users/account/", headers=headers)
    assert response.status_code == 401
    assert response.get_json().get("error") == "Token has expired!"

    # invalid token
    headers = {"Authorization": "basic invalidtoken"}
    response = client.get("/api-v1/users/account/", headers=headers)
    assert response.status_code == 401
    assert response.get_json().get("error") == "Invalid token!"

    # Patch jwt.decode to raise a generic Exception
    def mock_jwt_decode(*args, **kwargs):
        raise Exception

    monkeypatch.setattr("flaskapp.utils.jwt.decode", mock_jwt_decode)

    # Use a valid-looking header
    headers = {"Authorization": "basic sometoken"}
    response = client.get("/api-v1/users/account/", headers=headers)

    assert response.status_code == 500
    assert response.get_json().get("error") == "An unexpected error occurred"
