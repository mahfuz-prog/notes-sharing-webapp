import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    AUTH_PREFIX = os.getenv("AUTH_PREFIX")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    # MAIL_SERVER configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv("EMAIL_USER")  # email
    MAIL_PASSWORD = os.getenv("EMAIL_PASS")  # app password
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # jwt
    JWT_TIMEOUT_MINUTES = int(os.getenv("JWT_TIMEOUT_MINUTES"))

    MAX_NAME_LENGTH = 20
    MIN_NAME_LENGTH = 3
    MAX_EMAIL_LENGTH = 254
    MIN_EMAIL_LENGTH = 5
    EMAIL_REGEX = ""
    OTP_LENGTH = 6
    MIN_PASS_LENGTH = 8
    MAX_PASS_LENGTH = 20
    PASSWORD_REGEX = ""

    MAX_NOTE_ID_LENGTH = 7
    MIN_TITLE_LENGTH = 1
    MAX_TITLE_LENGTH = 100
    MIN_TEXT_LENGTH = 1
    MAX_TEXT_LENGTH = 20000
    MIN_PIN_LENGTH = 3
    MAX_PIN_LENGTH = 8
