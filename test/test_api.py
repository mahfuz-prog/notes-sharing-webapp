import json
import time

# test config
with open('../frontend_config.json', 'r') as config_file:
    conf = json.load(config_file)

AUTH_PREFIX = conf.get('AUTH_PREFIX')



'''
Add email and password for user_1 and user_2
password: Asdf1111 like this.
'''
user_1 = {
    "name": "test user 1",
    "test_email": "",
    "test_pass": "",
    "token": "",
}

user_2 = {
    "name": "test user 2",
    "test_email": "",
    "test_pass": "",
    "token": ""
}


# ====================================================================================
# ====================================================================================
# users blueprint
# ====================================================================================
# ====================================================================================

# sign-up endpoint
def test_sign_up(api_client):
    # already loggedin user can't access signup
    headers = {
        "Authorization": f"{AUTH_PREFIX} thisisavalidtokenfortesting"
    }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", headers=headers)
    assert response.status_code == 403, "Expected status code 403"
    assert response.json().get("error") == "Forbidden response!"

    # =========================================
    # without payload
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # =========================================
    # empty name
    payload = { "email": user_1["test_email"] }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name cannot be empty."

    # =========================================
    # minimum name
    payload = { "name": "as", "email": user_1["test_email"] }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name must be at least 3 characters."

    # =========================================
    # maximum name
    payload = { "name": "asd" * 20, "email": user_1["test_email"] }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name must be at most 20 characters."
  
    # =========================================
    # empty email
    payload = { "name": user_1["name"] }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email cannot be empty."

    # =========================================
    # invalid email format
    payload = { "name": user_1["name"], "email": "asdfddfd" }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid email format."

    # ===================================
    # create user 1
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
    }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    if response.status_code == 409:
        if response.json().get("nameStatus"):
            assert response.json().get("nameStatus") == "Username already taken."
        if response.json().get("emailStatus"):
            assert response.json().get("emailStatus") == "Email already taken."

    if response.status_code == 200:
        assert response.json().get("message") == "OTP sent to email."

    # ===================================
    # create user 2
    payload = {
        "name": user_2["name"],
        "email": user_2["test_email"],
    }
    response = api_client.post(f"{api_client.base_url}/users/sign-up/", json=payload)
    if response.status_code == 409:
        if response.json().get("nameStatus"):
            assert response.json().get("nameStatus") == "Username already taken."
        if response.json().get("emailStatus"):
            assert response.json().get("emailStatus") == "Email already taken."

    if response.status_code == 200:
        assert response.json().get("message") == "OTP sent to email."

    print("=================== Sign up test passed ==================")


# verify endpoint
def test_verify(api_client):
    # already loggedin user can't access verify
    headers = {
        "Authorization": f"{AUTH_PREFIX} thisisavalidtokenfortesting"
    }
    response = api_client.post(f"{api_client.base_url}/users/verify/", headers=headers)
    assert response.status_code == 403, "Expected status code 403"

    # =========================================
    # without payload
    response = api_client.post(f"{api_client.base_url}/users/verify/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."
    
    # =========================================
    # empty otp
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Otp cannot be empty."

    # =========================================
    # otp != 6
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "1234568"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Otp must be at most 6 characters."

    # =========================================
    # invalid otp
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Timeout or invalid OTP."

    # =========================================
    # empty name
    payload = {
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name cannot be empty."

    # =========================================
    # minimum name
    payload = {
        "name": "as",
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name must be at least 3 characters."

    # =========================================
    # maximum name
    payload = {
        "name": "as" * 20,
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Name must be at most 20 characters."

    # =========================================
    # empty email
    payload = {
        "name": "asadf",
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email cannot be empty."

    # =========================================
    # maximum email
    payload = {
        "name": user_1["name"],
        "email": "asdf" * 200 + "@b.d",
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email must be at most 254 characters."

    # =========================================
    # invalid email format
    payload = {
        "name": user_1["name"],
        "email": "asdfdd",
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid email format."

    # =========================================
    # empty password
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password cannot be empty."

    # =========================================
    # minimum password
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "password": "123",
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password must be at least 8 characters."

    # =========================================
    # maximum password
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "password": "123" * 20,
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password must be at most 20 characters."

    # =========================================
    # invalid password format
    payload = {
        "name": user_1["name"],
        "email": user_1["test_email"],
        "password": "asdfasdf",
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid password format."

    # =========================================
    # successful verification user 1
    otp = input('Press enter if user_1 already created. else enter OTP: ')
    if otp:
        payload = {
            "name": user_1["name"],
            "email": user_1["test_email"],
            'password': user_1["test_pass"],
            'otp': otp
        }
        response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
        if response.status_code == 400:
            assert response.json().get("error") == "Timeout or invalid OTP."

        if response.status_code == 200:
            assert response.json().get("message") == "Signup successful."

    # =========================================
    # successful verification user 2
    otp = input('Press enter if user_2 already created. else enter OTP: ')
    if otp:
        payload = {
            "name": user_2["name"],
            "email": user_2["test_email"],
            'password': user_2["test_pass"],
            'otp': otp
        }
        response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
        if response.status_code == 400:
            assert response.json().get("error") == "Timeout or invalid OTP."

        if response.status_code == 200:
            assert response.json().get("message") == "Signup successful."

    # =========================================
    # wait 2m for clear redis cache
    # to test this delete database file and remove comment
    print("sleeping for 80 second for clear redis cache...")
    time.sleep(80)

    # random otp for only test redis cache clear
    payload = {
        "name": user_2["name"],
        "email": user_2["test_email"],
        'password': user_2["test_pass"],
        'otp': "123456"
    }
    response = api_client.post(f"{api_client.base_url}/users/verify/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Timeout or invalid OTP."

    print("=================== Verify test passed ==================")


# login endpoint
def test_log_in(api_client):
    # already loggedin user can't access login
    headers = {
        "Authorization": f"{AUTH_PREFIX} thisisavalidtokenfortesting"
    }
    response = api_client.post(f"{api_client.base_url}/users/log-in/", headers=headers)
    assert response.status_code == 403, "Expected status code 403"

    # ==================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/users/log-in/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # =========================================
    # empty email
    payload = {
        "password": user_1["test_pass"],
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email cannot be empty."

    # =========================================
    # maximum email
    payload = {
        "email": "asdf" * 200 + "@b.d",
        "password": user_1["test_pass"],
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email must be at most 254 characters."

    # =========================================
    # invalid email format
    payload = {
        "email": "asdfdd",
        "password": user_1["test_pass"],
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid email format."

    # =========================================
    # empty password
    payload = {
        "email": user_1["test_email"],
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password cannot be empty."

    # =========================================
    # minimum password
    payload = {
        "email": user_1["test_email"],
        "password": "123",
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password must be at least 8 characters."

    # =========================================
    # maximum password
    payload = {
        "email": user_1["test_email"],
        "password": "123" * 20,
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password must be at most 20 characters."

    # =========================================
    # invalid password
    payload = {
        "email": user_1["test_email"],
        "password": "asdfdfddf",
    }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid password format."

    # ================================
    # login credentials user 1
    payload = {
        "email": user_1["test_email"],
        'password': user_1["test_pass"],
    }
    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    token = response.json().get('token')
    user_1["token"] = token

    # ================================
    # login credentials user 2
    payload = {
        "email": user_2["test_email"],
        'password': user_2["test_pass"],
    }
    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    token = response.json().get('token')
    user_2["token"] = token

    print("=================== Login test passed ==================")


# test reset password route
def test_reset_password(api_client):
    # ================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/users/reset-password/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # =========================================
    # empty email
    payload = { "password": user_1["test_pass"] }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email cannot be empty."

    # =========================================
    # maximum email
    payload = { "email": "asdf" * 200 + "@b.d" }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email must be at most 254 characters."

    # =========================================
    # invalid email format
    payload = { "email": "asdfdd" }

    response = api_client.post(f"{api_client.base_url}/users/log-in/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid email format."

    # ===============================================
    # valid credentials
    payload = {"email": user_1["test_email"]}
    response = api_client.post(f"{api_client.base_url}/users/reset-password/", json=payload)
    assert response.status_code == 200, "Expected status code 200"
    assert response.json().get("message") == "OTP sent to email."

    print("=================== Reset password test passed ==================")


# test reset otp verify
def test_verify_reset_otp(api_client):
    # ====================================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # =========================================
    # empty email
    payload = {"otp": 111111}

    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email cannot be empty."

    # =========================================
    # maximum email
    payload = { "email": "asdf" * 200 + "@b.d", "otp": 111111 }

    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email must be at most 254 characters."

    # =========================================
    # invalid email format
    payload = { "email": "asdfdd", "otp": 111111 }

    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid email format."


    # =========================================
    # empty otp
    payload = { "email": user_1["test_email"] }

    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Otp cannot be empty."

    # =========================================
    # otp != 6
    payload = {
        "email": user_1["test_email"],
        "otp": "1234568"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Otp must be at most 6 characters."

    # =========================================
    # invalid otp
    payload = {
        "email": user_1["test_email"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Timeout or invalid OTP."

    # ===========================================================
    # valid request
    otp = input('Enter otp user_1 to test verify_reset_otp. else enter to pass user_1: ')
    if otp:
        payload = {"email": user_1["test_email"], "otp": otp}
        response = api_client.post(f"{api_client.base_url}/users/verify-reset-otp/", json=payload)
        assert response.status_code == 200, "Expected status code 200"
        assert response.json().get("message") == "Otp matched."

    print("=================== Verify reset otp test passed ==================")


# test set new password
def test_new_pass(api_client):
    # =========================================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/users/new-password/", json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # =========================================
    # empty otp
    payload = {
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Otp cannot be empty."

    # =========================================
    # otp != 6
    payload = {
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "1234568"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Otp must be at most 6 characters."

    # =========================================
    # invalid otp
    payload = {
        "email": user_1["test_email"],
        "password": user_1["test_pass"],
        "otp": "123446"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Timeout or invalid OTP."

    # =========================================
    # empty email
    payload = {
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email cannot be empty."

    # =========================================
    # maximum email
    payload = {
        "email": "asdf" * 200 + "@b.d",
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Email must be at most 254 characters."

    # =========================================
    # invalid email format
    payload = {
        "email": "asdfdd",
        "password": user_1["test_pass"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid email format."

    # =========================================
    # empty password
    payload = {
        "email": user_1["test_email"],
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password cannot be empty."

    # =========================================
    # minimum password
    payload = {
        "email": user_1["test_email"],
        "password": "123",
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password must be at least 8 characters."

    # =========================================
    # maximum password
    payload = {
        "email": user_1["test_email"],
        "password": "123" * 20,
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Password must be at most 20 characters."

    # =========================================
    # invalid password format
    payload = {
        "email": user_1["test_email"],
        "password": "asdfasdf",
        "otp": "123456"
    }

    response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Invalid password format."


    # ===========================================================
    # change password
    otp = input('Enter same otp to change password. else enter to pass user_1: ')
    if otp:
        payload = {
            "email": user_1["test_email"],
            "otp": otp,
            "password": user_1["test_pass"]
        }
        response = api_client.post(f"{api_client.base_url}/users/new-password/", json=payload)
        assert response.status_code == 200, "Expected status code 200"
        assert response.json().get("message") == "Password changed."
    
    print("=================== New password test passed ==================")


# account endpoint
def test_account(api_client):
    # =========================================
    # without authorization header
    response = api_client.get(f"{api_client.base_url}/users/account/")
    assert response.status_code == 401, "Expected status code 401"

    # =========================================
    # wrong secret
    headers = {
        "Authorization": f"unknown asdf"
    }
    response = api_client.get(f"{api_client.base_url}/users/account/", headers=headers)
    assert response.status_code == 401, "Expected status code 401"

    # =========================================
    # without prefix secret
    headers = {
        "Authorization": user_1["token"]
    }
    response = api_client.get(f"{api_client.base_url}/users/account/", headers=headers)
    assert response.status_code == 401, "Expected status code 401"

    # =========================================
    # invalid jwt
    headers = {
        "Authorization": f"{AUTH_PREFIX} thisisainvalidtoken"
    }
    response = api_client.get(f"{api_client.base_url}/users/account/", headers=headers)
    assert response.status_code == 401, "Expected status code 401"

    # =========================================
    # success request
    headers = {
        "Authorization":
        f"{AUTH_PREFIX} {user_1['token']}"
    }
    response = api_client.get(f"{api_client.base_url}/users/account/", headers=headers)
    assert response.status_code == 200, "Expected status code 200"

    # update user_1 name
    user_1['name'] = response.json().get("name")


    print("=================== Account test passed ==================")
    

# ====================================================================================
# ====================================================================================
# notes blueprint
# ====================================================================================
# ====================================================================================

# test current user note list
def test_note_list(api_client):
    # success request
    headers = {
        "Authorization":
        f"{AUTH_PREFIX} {user_1['token']}"
    }
    response = api_client.get(f"{api_client.base_url}/notes/", headers=headers)
    assert response.status_code == 200, "Expected status code 200"
    
    print("=================== Get notes passed ==================")


# test create new note
def test_new_note(api_client):
    # success request
    headers = {
        "Authorization":
        f"{AUTH_PREFIX} {user_1['token']}"
    }

    # ================================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/notes/new-note/", headers=headers, json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # ===============================================
    # empty text
    payload = {"title": "asdf"}
    response = api_client.post(f"{api_client.base_url}/notes/new-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Text cannot be empty."

    # ==================================================
    # empty title
    payload = {"text": "text 1"}
    response = api_client.post(f"{api_client.base_url}/notes/new-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Title cannot be empty."

    # ==================================================
    # maximum title
    payload = {"title": "asd" * 100, "text": "text 1"}
    response = api_client.post(f"{api_client.base_url}/notes/new-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Title must be at most 100 characters."

    # ==================================================
    # minimum text
    payload = {"title": "title 1", "text": "  "}
    response = api_client.post(f"{api_client.base_url}/notes/new-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Text cannot be empty."

    # ==================================================
    # maximum text
    payload = {"title": "title 1", "text": "asd" * 10000}
    response = api_client.post(f"{api_client.base_url}/notes/new-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Text must be at most 20000 characters."

    # ==================================================
    # minimum length pin
    payload = {"title": "title 1", "text": "text 1", "pin": "12"}
    response = api_client.post(f"{api_client.base_url}/notes/new-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Pin must be at least 3 characters."
    
    # ==================================================
    # maximum pin
    payload = {"title": "title 1", "text": "text 1", "pin": "123456789"}
    response = api_client.post(f"{api_client.base_url}/notes/new-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Pin must be at most 8 characters."
    
    # ==================================================
    # 1 note, create a new note user 1
    payload = {"title": "title 1", "text": "text 1", "pin": "123"}
    response = api_client.post(f"{api_client.base_url}/notes/new-note/", headers=headers, json=payload)
    assert response.status_code == 200, "Expected status code 200"

    # ==================================================
    # 2 note, create a new note user 1
    payload = {"title": "title 2", "text": "text 2", "pin": "123"}
    response = api_client.post(f"{api_client.base_url}/notes/new-note/", headers=headers, json=payload)
    assert response.status_code == 200, "Expected status code 200"

    # ==================================================
    # create a new note user 2
    headers = {
        "Authorization":
        f"{AUTH_PREFIX} {user_2['token']}"
    }

    payload = {"title": "title 2", "text": "text 2", "pin": "123"}
    response = api_client.post(f"{api_client.base_url}/notes/new-note/", headers=headers, json=payload)
    assert response.status_code == 200, "Expected status code 200"

    print("=================== Create new note passed ==================")


# delete note
def test_delete_note(api_client):
    # ===========================================
    # user 1
    headers_user_1 = {
        "Authorization":
        f"{AUTH_PREFIX} {user_1['token']}"
    }

    # ===========================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/notes/delete-note/", headers=headers_user_1, json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # ================================
    # id with space
    response = api_client.post(f"{api_client.base_url}/notes/delete-note/", headers=headers_user_1, json={"note_id": "  "})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Note_id cannot be empty."

    # ================================
    # invalid id
    response = api_client.post(f"{api_client.base_url}/notes/delete-note/", headers=headers_user_1, json={"note_id": 55555})
    assert response.status_code == 404, "Expected status code 404"
    assert response.json().get("error") == "Note not found!"

    # ================================
    # big id
    response = api_client.post(f"{api_client.base_url}/notes/delete-note/", headers=headers_user_1, json={"note_id": "555" * 55})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Note_id must be at most 7 characters."

    # ======================================
    # get a note id from logged in user
    # delete note
    response = api_client.get(f"{api_client.base_url}/notes/", headers=headers_user_1)
    note_id_user_1 = response.json().get("notes")[0].get("id")
    response = api_client.post(f"{api_client.base_url}/notes/delete-note/", headers=headers_user_1, json={"note_id": note_id_user_1})
    assert response.status_code == 200, "Expected status code 200"
    assert response.json().get("id") == str(note_id_user_1)

    # ======================================
    # user 1 try to delete user 2 note

    # get user 2 note
    headers_user_2 = {
        "Authorization":
        f"{AUTH_PREFIX} {user_2['token']}"
    }
    response = api_client.get(f"{api_client.base_url}/notes/", headers=headers_user_2)
    note_id_user_2 = response.json().get("notes")[0].get("id")

    # user 1 try to delete
    response = api_client.post(f"{api_client.base_url}/notes/delete-note/", headers=headers_user_1, json={"note_id": note_id_user_2})
    assert response.status_code == 403, "Expected status code 403"
    assert response.json().get("error") == "Delete not allowed!"
    
    print("=================== Delete note passed ==================")


# test update note
def test_update_note(api_client):
    # user 1
    headers = {
        "Authorization":
        f"{AUTH_PREFIX} {user_1['token']}"
    }

    # ================================================
    # get a note id from logged in user 1
    response = api_client.get(f"{api_client.base_url}/notes/", headers=headers)
    note_id_user_1 = response.json().get("notes")[0].get("id")

    # ================================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # ===============================================
    # empty id
    payload = {"title": "asdf", "text": "text 1"}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Note_id cannot be empty."

    # ===============================================
    # id with space
    payload = {"note_id": "    ","title": "asdf", "text": "text 1"}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Note_id cannot be empty."

    # ===============================================
    # big note id
    payload = {"note_id": "555" * 55, "title": "asdf", "text": "text 1"}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Note_id must be at most 7 characters."

    # ===============================================
    # invalid id
    payload = {"note_id": 555555, "title": "title 1", "text": "text 1", "pin": "16789"}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    assert response.status_code == 404, "Expected status code 404"
    assert response.json().get("error") == "Note not found!"

    # ===============================================
    # only id and title
    payload = {"note_id": note_id_user_1, "title": "asdf"}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Text cannot be empty."

    # ===============================================
    # only id and text
    payload = {"note_id": note_id_user_1, "text": "text 1"}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Title cannot be empty."

    # ===============================================
    # maximum title
    payload = {"note_id": note_id_user_1, "title": "asd" * 100, "text": "text 1"}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Title must be at most 100 characters."

    # ===============================================
    # minimum text
    payload = {"note_id": note_id_user_1, "title": "title 1", "text": " "}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Text cannot be empty."

    # ===============================================
    # maximum text
    payload = {"note_id": note_id_user_1, "title": "title 1", "text": "asd" * 10000}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Text must be at most 20000 characters."

    # ===============================================
    # minimum length pin
    payload = {"note_id": note_id_user_1, "title": "title 1", "text": "text 1", "pin": "12"}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Pin must be at least 3 characters."
    
    # ===============================================
    # maximum pin
    payload = {"note_id": note_id_user_1, "title": "title 1", "text": "text 1", "pin": "123456789"}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Pin must be at most 8 characters."

    # ===============================================
    # update note user 1
    title = "This is updated title."
    text = "This is updated text."
    pin  = "asd"
    payload = {"note_id": note_id_user_1, "title": title, "text": text, "pin": pin}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    
    updated_title = response.json().get("title")
    updated_text = response.json().get("text")
    updated_pin = response.json().get("pin")

    assert response.status_code == 200, "Expected status code 200"
    assert title == updated_title and text == updated_text and pin == updated_pin

    # user 2 try to update user 1 note
    headers = {
        "Authorization":
        f"{AUTH_PREFIX} {user_2['token']}"
    }

    payload = {"note_id": note_id_user_1, "title": title, "text": text, "pin": pin}
    response = api_client.post(f"{api_client.base_url}/notes/update-note/", headers=headers, json=payload)
    assert response.status_code == 403, "Expected status code 403"
    assert response.json().get("error") == "Update not allowed!"

    print("=================== Update note passed ==================")


# ====================================================================================
# ====================================================================================
# main blueprint
# ====================================================================================
# ====================================================================================

# get single note
def test_single_note(api_client):
    # get user 2 note
    headers_user_2 = {
        "Authorization":
        f"{AUTH_PREFIX} {user_2['token']}"
    }
    response = api_client.get(f"{api_client.base_url}/notes/", headers=headers_user_2)
    note_id_user_2 = response.json().get("notes")[0].get("id")

    # =================================
    # empty payload
    response = api_client.post(f"{api_client.base_url}/main/single-note/", headers=headers_user_2, json={})
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Request must be JSON."

    # =================================
    # empty username
    response = api_client.post(f"{api_client.base_url}/main/single-note/", headers=headers_user_2, json={ "note_id": 500 })
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Username cannot be empty."

    # =================================
    # invalid note id
    payload = { "note_id": 500, "username": user_2['name'].replace(" ", "-").lower() }
    response = api_client.post(f"{api_client.base_url}/main/single-note/", headers=headers_user_2, json=payload)
    assert response.status_code == 404, "Expected status code 404"
    assert response.json().get("error") == "Note not found!"
 
    # =================================
    # invalid username
    payload = { "note_id": note_id_user_2, "username": "invalid" }
    response = api_client.post(f"{api_client.base_url}/main/single-note/", headers=headers_user_2, json=payload)
    assert response.status_code == 404, "Expected status code 404"
    assert response.json().get("error") == "Note not found!"

    # =================================
    # pin protected message
    payload = { "note_id": note_id_user_2, "username": user_2['name'].replace(" ", "-").lower() }
    response = api_client.post(f"{api_client.base_url}/main/single-note/", headers=headers_user_2, json=payload)
    assert response.status_code == 200, "Expected status code 200"
    assert response.json().get("message") == "Pin required!"

    # =================================
    # with pin, invalid note id
    payload = { "note_id": 500, "username": user_2['name'].replace(" ", "-").lower(), "pin": "123" }
    response = api_client.post(f"{api_client.base_url}/main/single-note/", headers=headers_user_2, json=payload)
    assert response.status_code == 404, "Expected status code 404"
    assert response.json().get("error") == "Note not found!"

    # =================================
    # with pin, invalid username
    payload = { "note_id": 500, "username": "invalid", "pin": "123" }
    response = api_client.post(f"{api_client.base_url}/main/single-note/", headers=headers_user_2, json=payload)
    assert response.status_code == 404, "Expected status code 404"
    assert response.json().get("error") == "Note not found!"

    # =================================
    # invalid pin
    payload = { "note_id": note_id_user_2, "username": user_2['name'].replace(" ", "-").lower(), "pin": "1212" }
    response = api_client.post(f"{api_client.base_url}/main/single-note/", headers=headers_user_2, json=payload)
    assert response.status_code == 403, "Expected status code 403"
    assert response.json().get("error") == "Invalid pin."

    # =================================
    # success request
    payload = { "note_id": note_id_user_2, "username": user_2['name'].replace(" ", "-").lower(), "pin": "123" }
    response = api_client.post(f"{api_client.base_url}/main/single-note/", headers=headers_user_2, json=payload)
    assert response.status_code == 200, "Expected status code 200"
    assert response.json().get("username") == user_2['name'].replace(" ", "-").lower()

    print("=================== Get single note passed ==================")


# get user profile
def test_user_profile(api_client):
    # =================================================
    # minimum username
    url = f"{api_client.base_url}/main/user-profile/as/"
    response = api_client.get(url)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Username must be between 3 and 20 characters."

    # =================================================
    # maximum username
    url = f"{api_client.base_url}/main/user-profile/{'asd' * 20}/"
    response = api_client.get(url)
    assert response.status_code == 400, "Expected status code 400"
    assert response.json().get("error") == "Username must be between 3 and 20 characters."

    # =================================================
    # invalid username
    url = f"{api_client.base_url}/main/user-profile/adff/"
    response = api_client.get(url)
    assert response.status_code == 404, "Expected status code 404"
    assert response.json().get("error") == "User not found!"

    # ====================================
    # success
    name = user_1["name"]
    url = f"{api_client.base_url}/main/user-profile/{name}/"
    response = api_client.get(url)
    assert response.status_code == 200, "Expected status code 200"
    
    print("=================== Get user profile passed ==================")