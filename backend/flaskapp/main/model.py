from pydantic import BaseModel, constr
from flaskapp.config import Config


class UsernameValidator(BaseModel):
    username: constr(
        strip_whitespace=True,
        min_length=Config.MIN_NAME_LENGTH,
        max_length=Config.MAX_NAME_LENGTH,
    )

    def __init__(self, **data):
        if "username" in data:
            data["username"] = data["username"].replace(" ", "-").lower()
        super().__init__(**data)


class SingleNoteRequest(BaseModel):
    username: constr(
        min_length=Config.MIN_NAME_LENGTH,
        max_length=Config.MAX_NAME_LENGTH,
        strip_whitespace=True,
    )
    note_id: constr(max_length=Config.MAX_NOTE_ID_LENGTH, strip_whitespace=True)
    pin: (
        constr(
            min_length=Config.MIN_PIN_LENGTH,
            max_length=Config.MAX_PIN_LENGTH,
            strip_whitespace=True,
        )
        | None
    ) = ""
