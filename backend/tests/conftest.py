import os
import pytest
from dotenv import load_dotenv
from flaskapp import bcrypt
from flaskapp.db_models import User
from flaskapp import create_app, db
from flaskapp.db_models import Notes
from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv()


class TestConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    AUTH_PREFIX = os.getenv("AUTH_PREFIX")

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    MAIL_SUPPRESS_SEND = True

    # jwt
    JWT_TIMEOUT_MINUTES = int(os.getenv("JWT_TIMEOUT_MINUTES"))

    # user
    MAX_NAME_LENGTH = 20
    MIN_NAME_LENGTH = 3
    OTP_LENGTH = 6
    MIN_PASS_LENGTH = 8
    MAX_PASS_LENGTH = 20
    PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,20}$"

    # note
    MAX_NOTE_ID_LENGTH = 7
    MIN_TITLE_LENGTH = 1
    MAX_TITLE_LENGTH = 100
    MIN_TEXT_LENGTH = 1
    MAX_TEXT_LENGTH = 20000
    MIN_PIN_LENGTH = 3
    MAX_PIN_LENGTH = 8


@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for each test session."""
    flask_app = create_app(TestConfig)

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()


@pytest.fixture(scope="function")
def db_session(app):
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

        Session = scoped_session(sessionmaker(bind=connection))
        db.session = Session

        yield Session

        Session.remove()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def redis_clean():
    from flaskapp.caching import redis_client

    redis_client.flushdb()
    yield redis_client
    redis_client.flushdb()


@pytest.fixture()
def client(app, db_session, redis_clean):
    return app.test_client()


@pytest.fixture(scope="function")
def test_user_1():
    hashed_pass = bcrypt.generate_password_hash("string", rounds=13).decode("utf-8")
    return User(
        email="test1@example.com",
        username="test1",
        password=hashed_pass,
    )


@pytest.fixture(scope="function")
def auth_headers_1(client, db_session, test_user_1):
    db_session.add(test_user_1)
    db_session.commit()

    payload = {"email": test_user_1.email, "password": "string"}
    response = client.post("/api-v1/users/log-in/", json=payload)
    assert response.status_code == 200
    token = response.get_json()["token"]
    return {"Authorization": f"basic {token}"}


@pytest.fixture(scope="function")
def test_user_2():
    hashed_pass = bcrypt.generate_password_hash("string", rounds=13).decode("utf-8")
    return User(
        email="test2@example.com",
        username="test2",
        password=hashed_pass,
    )


@pytest.fixture(scope="function")
def auth_headers_2(client, db_session, test_user_2):
    db_session.add(test_user_2)
    db_session.commit()

    payload = {"email": test_user_2.email, "password": "string"}
    response = client.post("/api-v1/users/log-in/", json=payload)
    assert response.status_code == 200
    token = response.get_json()["token"]
    return {"Authorization": f"basic {token}"}


@pytest.fixture(scope="function")
def test_note_1(db_session, test_user_1):
    db_session.add(test_user_1)
    db_session.commit()

    return Notes(
        title="Test note title",
        text="test note text",
        pin="pin",
        user_id=test_user_1.id,
    )
