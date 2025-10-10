import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URI = os.getenv("REDIS_URI")

redis_client = redis.Redis.from_url(REDIS_URI, decode_responses=True)


class RedisKeys:
    SIGN_UP = "signup:{email}:otp"
    RESET_PASSWORD = "reset_pass:{email}:otp"
    USER_NOTES = "user:{username}:notes"
    SINGLE_NOTE = "note:{note_id}"
    TOTAL_USER = "total_user"
    TOTAL_NOTE = "total_note"
    TOTAL_CHAR = "total_char"

    @classmethod
    def sign_up(cls, email: str) -> str:
        return cls.SIGN_UP.format(email=email)

    @classmethod
    def reset_password(cls, email: str) -> str:
        return cls.RESET_PASSWORD.format(email=email)

    @classmethod
    def user_notes(cls, username: str) -> str:
        return cls.USER_NOTES.format(username=username)

    @classmethod
    def single_note(cls, note_id: str) -> str:
        return cls.SINGLE_NOTE.format(note_id=note_id)
