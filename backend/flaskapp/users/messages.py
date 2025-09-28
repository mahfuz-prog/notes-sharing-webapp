import logging
from flaskapp import mail
from flask_mail import Message
from flaskapp.exceptions import InternalServerError


def send_otp(otp: str, email: str) -> None:
    msg = Message("Verify Your OTP", sender="noreply@demo.com", recipients=[email])
    msg.body = f"""To confirm your email, Use the OTP. After 2 minutes otp will be invalid.
OTP: {otp}
If you did not make this request then simply ignore this email and no changes will be made.
"""
    try:
        mail.send(msg)
    except Exception as e:
        logging.error(f"Failed to send Verify OTP email. Error: {str(e)}")
        raise InternalServerError()
