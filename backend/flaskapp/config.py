import json

# with open('/etc/backend_config.json', 'r') as config_file:
with open('../backend_config.json', 'r') as config_file:
	conf = json.load(config_file)

class Config():
	SECRET_KEY = conf.get('SECRET_KEY')
	AUTH_PREFIX = conf.get('AUTH_PREFIX')
	SQLALCHEMY_DATABASE_URI = conf.get('SQLALCHEMY_DATABASE_URI')

	# MAIL_SERVER configuration
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USERNAME = conf.get('EMAIL_USER') 	#email
	MAIL_PASSWORD = conf.get('EMAIL_PASS')	#app password
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True

	# jwt
	JWT_TIMEOUT = conf.get('JWT_TIMEOUT')