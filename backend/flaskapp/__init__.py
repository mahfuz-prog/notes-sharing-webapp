from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flaskapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flaskapp.logging import configure_logging, LogLevels

load_dotenv()
configure_logging(LogLevels.info)


mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_class: Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    from flaskapp.users.routes import users_bp
    from flaskapp.main.routes import main_bp
    from flaskapp.notes.routes import notes_bp
    from flaskapp.utils import register_error_handlers

    app.register_blueprint(users_bp, url_prefix="/api-v1/users/")
    app.register_blueprint(main_bp, url_prefix="/api-v1/main/")
    app.register_blueprint(notes_bp, url_prefix="/api-v1/notes/")
    register_error_handlers(app)

    # Cross-Origin Resource Sharing
    # CORS(app, origins=[os.getenv("ORIGIN", "*")], methods=["GET", "POST"])
    CORS(app)

    return app
