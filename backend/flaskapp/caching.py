import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
)


class RedisKeys:
    SIGN_UP = "signup:{email}:otp"
    RESET_PASSWORD = "reset_pass:{email}:otp"
    USER_NOTES = "user:{username}:notes"
    SINGLE_NOTE = "note:{note_id}"
    TOTAL_USER = "total_user"
    TOTAL_NOTE = "total_note"
    TOTAL_CHAR = "total_char"

    @staticmethod
    def sign_up(email: str) -> str:
        return RedisKeys.SIGN_UP.format(email=email)

    @staticmethod
    def reset_password(email: str) -> str:
        return RedisKeys.RESET_PASSWORD.format(email=email)

    @staticmethod
    def user_notes(username: str) -> str:
        return RedisKeys.USER_NOTES.format(username=username)

    @staticmethod
    def single_note(note_id: str) -> str:
        return RedisKeys.SINGLE_NOTE.format(note_id=note_id)
