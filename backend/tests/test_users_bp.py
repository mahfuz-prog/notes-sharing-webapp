from flaskapp import db
from flaskapp.caching import RedisKeys, redis_client


# signup endpoint
def test_sign_up(client, test_user_1, db_session):
    # create a user to test username & email already taken
    db_session.add(test_user_1)
    db_session.commit()

    payload = {"username": test_user_1.username, "email": "new@gmail.com"}
    response = client.post("/api-v1/users/sign-up/", json=payload)
    assert response.status_code == 409
    assert response.get_json()["error"]["nameStatus"] == "Username already taken"

    payload = {"username": "new_name", "email": test_user_1.email}
    response = client.post("/api-v1/users/sign-up/", json=payload)
    assert response.status_code == 409
    assert response.get_json()["error"]["emailStatus"] == "Email already taken"

    # delete the user from db
    db_session.delete(test_user_1)
    db_session.commit()

    payload = {"username": test_user_1.username, "email": test_user_1.email}
    response = client.post("/api-v1/users/sign-up/", json=payload)
    assert response.status_code == 200
    assert response.get_json().get("message") == "OTP sent to email"


# verify endpoint
def test_verify(client, test_user_1):
    payload = {
        "username": test_user_1.username,
        "email": test_user_1.email,
        "password": "Asdf1111",
        "otp": "123456",
    }

    response = client.post("/api-v1/users/verify/", json=payload)
    assert response.status_code == 400
    assert response.get_json()["error"] == "Timeout or invalid OTP"

    # set otp in redis to bypass 2-step
    otp_key = RedisKeys.sign_up(test_user_1.email)
    redis_client.set(otp_key, "123456")

    # successfully register a user
    response = client.post("/api-v1/users/verify/", json=payload)
    assert response.status_code == 201
    assert response.get_json().get("message") == "User created"


# verify error
def test_verify_error(client, test_user_1, monkeypatch):
    payload = {
        "username": test_user_1.username,
        "email": test_user_1.email,
        "password": "Asdf1111",
        "otp": "123456",
    }

    # set invalid otp
    otp_key = RedisKeys.sign_up(test_user_1.email)
    redis_client.set(otp_key, "12345")

    response = client.post("/api-v1/users/verify/", json=payload)
    assert response.status_code == 400
    assert response.get_json().get("error") == "Timeout or invalid OTP"

    # set a valid otp
    redis_client.set(otp_key, "123456")

    # force commit to fail
    def fail_commit():
        raise Exception

    monkeypatch.setattr(db.session, "commit", fail_commit)

    response = client.post("/api-v1/users/verify/", json=payload)
    assert response.status_code == 500
    assert response.get_json().get("error") == "An unexpected error occurred"


# login endpoint
def test_log_in(client, db_session, test_user_1):
    db_session.add(test_user_1)
    db_session.commit()

    # invalid password
    payload = {"email": test_user_1.email, "password": "invalid"}
    response = client.post("/api-v1/users/log-in/", json=payload)
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid credentials"

    # login
    payload = {"email": test_user_1.email, "password": "string"}
    response = client.post("/api-v1/users/log-in/", json=payload)
    assert response.status_code == 200
    assert response.get_json()["username"] == test_user_1.username
    assert "token" in response.get_json()


# reset password/forgot password endpoint
def test_reset_password(client, db_session, test_user_1):
    db_session.add(test_user_1)
    db_session.commit()

    response = client.post(
        "/api-v1/users/reset-password/", json={"email": test_user_1.email}
    )
    assert response.status_code == 200
    otp_key = RedisKeys.reset_password(test_user_1.email)
    assert redis_client.get(otp_key)
    assert response.get_json()["message"] == "OTP sent to email"


def test_reset_password_error(client, test_user_1):
    # set a otp explicitly to raise OtpRetryLimitError
    otp_key = RedisKeys.reset_password(test_user_1.email)
    redis_client.set(otp_key, "123456")
    response = client.post(
        "/api-v1/users/reset-password/", json={"email": test_user_1.email}
    )
    assert response.status_code == 429
    assert response.get_json()["error"] == "Please try again after 2 minutes"

    # user not found
    redis_client.delete(otp_key)
    response = client.post(
        "/api-v1/users/reset-password/", json={"email": test_user_1.email}
    )
    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found!"


# test verify reset otp endpoint
def test_verify_reset_otp(client, test_user_1):
    # explicitly set a otp
    otp_key = RedisKeys.reset_password(test_user_1.email)
    redis_client.set(otp_key, "123456")

    # invalid otp
    payload = {"email": test_user_1.email, "otp": "123457"}
    response = client.post("/api-v1/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400
    assert response.get_json()["error"] == "Timeout or invalid OTP"

    # valid otp
    payload = {"email": test_user_1.email, "otp": "123456"}
    response = client.post("/api-v1/users/verify-reset-otp/", json=payload)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Otp matched"


# change password endpoint
def test_new_pass(client, db_session, test_user_1):
    db_session.add(test_user_1)
    db_session.commit()

    # explicitly set a otp
    otp_key = RedisKeys.reset_password(test_user_1.email)
    redis_client.set(otp_key, "123456")

    payload = {"email": test_user_1.email, "password": "Asdf1111", "otp": "123456"}
    response = client.post("/api-v1/users/new-password/", json=payload)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Password changed"

    # login
    payload = {"email": test_user_1.email, "password": "Asdf1111"}
    response = client.post("/api-v1/users/log-in/", json=payload)
    assert response.status_code == 200

    data = response.get_json()
    assert data["username"] == test_user_1.username
    assert "token" in data


# account endpoint
def test_account(client, auth_headers_1, test_user_1):
    response = client.get("/api-v1/users/account/", headers=auth_headers_1)
    assert response.status_code == 200

    data = response.get_json()
    assert data["name"] == test_user_1.username
    assert data["email"] == test_user_1.email
