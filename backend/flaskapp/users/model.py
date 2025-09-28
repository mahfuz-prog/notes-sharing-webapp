import re
from pydantic import BaseModel, EmailStr, field_validator, constr
from flaskapp.config import Config


username_validator = constr(
    strip_whitespace=True,
    min_length=Config.MIN_NAME_LENGTH,
    max_length=Config.MAX_NAME_LENGTH,
)

password_validator = constr(
    strip_whitespace=True,
    min_length=Config.MIN_PASS_LENGTH,
    max_length=Config.MAX_PASS_LENGTH,
)

otp_validator = constr(
    strip_whitespace=True,
    min_length=Config.OTP_LENGTH,
    max_length=Config.OTP_LENGTH,
)


class SignUpRequest(BaseModel):
    username: username_validator
    email: EmailStr


class VerifyRequest(BaseModel):
    username: username_validator
    email: EmailStr
    password: password_validator
    otp: otp_validator

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        pattern = re.compile(Config.PASSWORD_REGEX)
        if not pattern.match(v):
            raise ValueError(
                "Password must be 8–64 characters long, contain at least one uppercase, one lowercase, one digit."
            )
        return v


class LogInRequest(BaseModel):
    email: EmailStr
    password: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class VerifyResetOtpRequest(BaseModel):
    email: EmailStr
    otp: otp_validator


class ChangePasswordRequest(BaseModel):
    email: EmailStr
    password: password_validator
    otp: otp_validator

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        pattern = re.compile(Config.PASSWORD_REGEX)
        if not pattern.match(v):
            raise ValueError(
                "Password must be 8–64 characters long, contain at least one uppercase, one lowercase, one digit."
            )
        return v
