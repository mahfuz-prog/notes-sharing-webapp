import pytest
from pydantic import ValidationError
from flask import current_app
from flaskapp.users import model


class TestAuthModels:
    # SignUpRequest
    def test_SignUpRequest_valid(self):
        validated = model.SignUpRequest(username="validuser", email="test@example.com")
        assert validated.username == "validuser"
        assert validated.email == "test@example.com"

    def test_SignUpRequest_invalid_username_too_short(self):
        MIN_NAME_LENGTH = current_app.config["MIN_NAME_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.SignUpRequest(
                username="t" * (MIN_NAME_LENGTH - 1), email="test@example.com"
            )
        assert f"String should have at least {MIN_NAME_LENGTH} characters" in str(
            exc_info.value
        )

    def test_SignUpRequest_invalid_username_too_long(self):
        MAX_NAME_LENGTH = current_app.config["MAX_NAME_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.SignUpRequest(
                username="t" * (MAX_NAME_LENGTH + 1), email="test@example.com"
            )
        assert f"String should have at most {MAX_NAME_LENGTH} characters" in str(
            exc_info.value
        )

    def test_SignUpRequest_invalid_email(self):
        with pytest.raises(ValidationError) as exc_info:
            model.SignUpRequest(username="validuser", email="not-an-email")
        assert "value is not a valid email address" in str(exc_info.value)

    # VerifyRequest
    def test_VerifyRequest_valid(self):
        validated = model.VerifyRequest(
            username="validuser",
            email="test@example.com",
            password="Valid123",
            otp="123456",
        )
        assert validated.password == "Valid123"
        assert validated.otp == "123456"

    def test_VerifyRequest_invalid_password_regex(self):
        with pytest.raises(ValidationError) as exc_info:
            model.VerifyRequest(
                username="validuser",
                email="test@example.com",
                password="alllowercase123",  # missing uppercase
                otp="123456",
            )
        assert "Password must be" in str(exc_info.value)

    def test_VerifyRequest_invalid_otp_too_short(self):
        OTP_LENGTH = current_app.config["OTP_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.VerifyRequest(
                username="validuser",
                email="test@example.com",
                password="Valid123",
                otp="1" * (OTP_LENGTH - 1),
            )
        assert f"String should have at least {OTP_LENGTH} characters" in str(
            exc_info.value
        )

    def test_VerifyRequest_invalid_otp_too_long(self):
        OTP_LENGTH = current_app.config["OTP_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.VerifyRequest(
                username="validuser",
                email="test@example.com",
                password="Valid123",
                otp="1" * (OTP_LENGTH + 1),
            )
        assert f"String should have at most {OTP_LENGTH} characters" in str(
            exc_info.value
        )

    # LogInRequest
    def test_LogInRequest_valid(self):
        validated = model.LogInRequest(email="test@example.com", password="anything")
        assert validated.email == "test@example.com"

    def test_LogInRequest_invalid_email(self):
        with pytest.raises(ValidationError) as exc_info:
            model.LogInRequest(email="invalid-email", password="anything")
        assert "value is not a valid email address" in str(exc_info.value)

    # ResetPasswordRequest
    def test_ResetPasswordRequest_valid(self):
        validated = model.ResetPasswordRequest(email="test@example.com")
        assert validated.email == "test@example.com"

    def test_ResetPasswordRequest_invalid_email(self):
        with pytest.raises(ValidationError) as exc_info:
            model.ResetPasswordRequest(email="not-an-email")
        assert "value is not a valid email address" in str(exc_info.value)

    # VerifyResetOtpRequest
    def test_VerifyResetOtpRequest_valid(self):
        validated = model.VerifyResetOtpRequest(email="test@example.com", otp="123456")
        assert validated.otp == "123456"

    def test_VerifyResetOtpRequest_invalid_otp(self):
        OTP_LENGTH = current_app.config["OTP_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.VerifyResetOtpRequest(
                email="test@example.com", otp="1" * (OTP_LENGTH - 1)
            )
        assert f"String should have at least {OTP_LENGTH} characters" in str(
            exc_info.value
        )

    # ChangePasswordRequest
    def test_ChangePasswordRequest_valid(self):
        validated = model.ChangePasswordRequest(
            email="test@example.com",
            password="Valid123",
            otp="123456",
        )
        assert validated.password == "Valid123"

    def test_ChangePasswordRequest_invalid_password_regex(self):
        with pytest.raises(ValidationError) as exc_info:
            model.ChangePasswordRequest(
                email="test@example.com",
                password="NoDigits",  # missing digit
                otp="123456",
            )
        assert "Password must be" in str(exc_info.value)

    def test_ChangePasswordRequest_invalid_otp_length(self):
        OTP_LENGTH = current_app.config["OTP_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.ChangePasswordRequest(
                email="test@example.com",
                password="Valid123",
                otp="1" * (OTP_LENGTH + 1),
            )
        assert f"String should have at most {OTP_LENGTH} characters" in str(
            exc_info.value
        )
