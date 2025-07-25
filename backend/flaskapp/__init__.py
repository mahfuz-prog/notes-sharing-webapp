import redis
from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flaskapp.config import Config
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	mail.init_app(app)
	bcrypt.init_app(app)

	from flaskapp.users.routes import users_bp
	from flaskapp.main.routes import main_bp
	from flaskapp.notes.routes import notes_bp
	app.register_blueprint(users_bp, url_prefix='/api-v1/users/')
	app.register_blueprint(main_bp, url_prefix='/api-v1/main/')
	app.register_blueprint(notes_bp, url_prefix='/api-v1/notes/')
	
	# Cross-Origin Resource Sharing
	# CORS(app, origins=["http://localhost:8080"], methods=["GET", "POST"])
	CORS(app)

	return app