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
