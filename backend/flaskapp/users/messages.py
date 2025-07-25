from flaskapp import mail
from flask_mail import Message

def send_otp(otp, email):
	msg = Message('Verify Your OTP', sender='noreply@demo.com', recipients=[email])
	msg.body = f'''To confirm your email, Use the OTP. After 2 minutes otp will be invalid.
OTP: {otp}
If you did not make this request then simply ignore this email and no changes will be made.
'''
	try:
		mail.send(msg)
		return True
	except:
		return False