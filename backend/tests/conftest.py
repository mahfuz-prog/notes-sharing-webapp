import pytest
from flaskapp import create_app, db


@pytest.fixture(scope="function")
def app():
    """Create a Flask app instance configured for tests."""
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="function")
def db_session():
    """Provide a transactional database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    # Bind a new session to the transaction
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    # Override the global session
    db.session = session

    yield session

    session.remove()
    transaction.rollback()
    connection.close()
