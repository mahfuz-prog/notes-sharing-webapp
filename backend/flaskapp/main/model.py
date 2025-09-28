from pydantic import BaseModel, constr
from flaskapp.config import Config

username_validator = constr(
    strip_whitespace=True,
    min_length=Config.MIN_NAME_LENGTH,
    max_length=Config.MAX_NAME_LENGTH,
)


class PublicProfileRequest(BaseModel):
    username: username_validator


class SingleNoteRequest(BaseModel):
    username: username_validator
    note_id: constr(max_length=Config.MAX_NOTE_ID_LENGTH, strip_whitespace=True)
    pin: (
        constr(
            min_length=Config.MIN_PIN_LENGTH,
            max_length=Config.MAX_PIN_LENGTH,
            strip_whitespace=True,
        )
        | None
    ) = ""
