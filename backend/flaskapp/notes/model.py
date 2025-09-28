from pydantic import BaseModel, constr
from flaskapp.config import Config

title_validator = constr(
    strip_whitespace=True,
    min_length=Config.MIN_TITLE_LENGTH,
    max_length=Config.MAX_TITLE_LENGTH,
)

text_validator = constr(
    strip_whitespace=True,
    min_length=Config.MIN_TEXT_LENGTH,
    max_length=Config.MAX_TEXT_LENGTH,
)

pin_validator = constr(
    min_length=0,
    max_length=Config.MAX_PIN_LENGTH,
    strip_whitespace=True,
)


class DeleteNoteRequest(BaseModel):
    note_id: int


class CreateNewNoteRequest(BaseModel):
    title: title_validator
    text: text_validator
    pin: pin_validator


class UpdateNoteRequest(BaseModel):
    note_id: int
    title: title_validator
    text: text_validator
    pin: pin_validator
