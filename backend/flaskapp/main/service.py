import logging
from pydantic import ValidationError
from flask import request
from sqlalchemy import func
from flaskapp import db
from flaskapp import redis_client
from flaskapp.db_models import User, Notes
from flaskapp.main import model
from flaskapp.exceptions import (
    InternalServerError,
    UsernameError,
    UserNotFoundError,
    RequestJsonError,
    NoteNotFound,
    NotePinMismatchError,
    NotePinRequiredError,
)


def homepage_stats() -> dict:
    try:
        total_user = User.query.count()
        total_notes = Notes.query.count()

        total_char_cached = redis_client.get("total_char")
        if total_char_cached:
            total_char_value = int(total_char_cached)
        else:
            char_sum = (
                db.session.query(
                    func.sum(func.length(Notes.title) + func.length(Notes.text))
                ).scalar()
            ) or 0

            redis_client.setex("total_char", 600, str(char_sum))  # cache for 10 minutes
            total_char_value = char_sum

        return {
            "totalUser": total_user,
            "totalNotes": total_notes,
            "totalChar": total_char_value,
        }
    except Exception as e:
        logging.error(f"Failed to load homepage stats. Error: {str(e)}")
        raise InternalServerError()


# query a user by username
def get_user(username: str) -> User:
    try:
        user = User.query.filter_by(username=username).first()
        if user is None:
            logging.warning(f"User not found for username={username}")
            raise UserNotFoundError()
        return user
    except UserNotFoundError:
        raise
    except Exception as e:
        logging.error(f"Failed to get user. Error: {str(e)}")
        raise InternalServerError()


def get_user_note_list(username: str) -> list:
    # Validate username
    try:
        validated_username = model.UsernameValidator(username=username)
        username = validated_username.username
    except ValidationError as e:
        logging.error(f"Failed to validate username. Error: {str(e)}")
        raise UsernameError()

    user = get_user(username)

    notes_data = []
    if user.notes:
        for note in user.notes:
            notes_data.append(
                {
                    "id": note.id,
                    "title": note.title,
                    "dateCreated": note.date_created,
                    "isLocked": bool(note.pin),
                }
            )

    return notes_data


# get a single not by id
def get_note(note_id: int) -> Notes:
    try:
        note = Notes.query.get(note_id)
        if note is None:
            logging.warning(f"Note not found for note_id={note_id}")
            raise NoteNotFound()
        return note
    except NoteNotFound:
        raise
    except Exception as e:
        logging.error(f"Failed to get note. Error: {str(e)}")
        raise InternalServerError()


def get_single_note() -> dict:
    try:
        validated = model.SingleNoteRequest(**request.get_json())
    except ValidationError as e:
        logging.error(f"Invalid request body. Error: {str(e)}")
        raise RequestJsonError()

    note = get_note(int(validated.note_id))

    # if note has a pin
    if note.pin:
        # the request dose not contain a pin
        if not validated.pin:
            logging.warning(f"Pin required for note_id: {note.id}")
            raise NotePinRequiredError()

        if note.pin != validated.pin:
            logging.warning(
                f"Pin mismatch for note_id={note.id}: provided={validated.pin}"
            )
            raise NotePinMismatchError()

    return {
        "username": note.author.username,
        "title": note.title,
        "text": note.text,
        "date": note.date_created,
    }
