from flaskapp import db
from datetime import datetime

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(254), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	notes = db.relationship('Notes', backref='author', lazy=True)

	# username check while creating account
	@staticmethod
	def check_name(name):
		name = name.strip().replace(' ', '-').lower()
		user = User.query.filter_by(username=name).first()
		return True if user else False

	# email check while creating account
	@staticmethod
	def check_email(email):
		user = User.query.filter_by(email=email).first()
		return True if user else False

	def __repr__(self):
		return f'username: {self.username} | email: {self.email}'


# one to many relationship, user -> notes
class Notes(db.Model):
	__tablename__ = 'notes'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), unique=False, nullable=False)
	text = db.Column(db.String(20000), unique=False, nullable=False)
	pin = db.Column(db.String(8), nullable=True)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f'id: {self.id} | Title: {self.title} | Author: {self.user_id}'