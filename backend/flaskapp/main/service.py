import json
import logging
from typing import Union, Tuple
from flask import jsonify, Response
from sqlalchemy import func
from flaskapp import db
from flaskapp.caching import redis_client, RedisKeys
from flaskapp.db_models import User, Notes
from flaskapp.main import model
from flaskapp.utils import response_body_validator
from flaskapp.exceptions import (
    InternalServerError,
    UserNotFoundError,
    NoteNotFound,
    NotePinMismatchError,
    NotePinRequiredError,
)


# total user cout
def user_count() -> int:
    cache_key = RedisKeys.TOTAL_USER
    total_user = redis_client.get(cache_key)
    if total_user:
        return int(total_user)

    total_user = User.query.count()
    redis_client.setex(cache_key, 60 * 60, str(total_user))
    return total_user


# total note count
def note_count() -> int:
    cache_key = RedisKeys.TOTAL_NOTE
    total_note = redis_client.get(cache_key)
    if total_note:
        return int(total_note)

    total_note = Notes.query.count()
    redis_client.setex(cache_key, 60 * 60, str(total_note))
    return total_note


# total char in all notes
def total_char() -> int:
    cache_key = RedisKeys.TOTAL_CHAR
    total_char = redis_client.get(cache_key)
    if total_char:
        return int(total_char)

    char_sum = (
        db.session.query(
            func.sum(func.length(Notes.title) + func.length(Notes.text))
        ).scalar()
    ) or 0
    redis_client.setex(cache_key, 60 * 60, str(char_sum))
    return char_sum


def homepage_stats() -> Union[Response, Tuple[Response, int]]:
    try:
        return jsonify(
            {
                "totalUser": user_count(),
                "totalNotes": note_count(),
                "totalChar": total_char(),
            }
        ), 200
    except Exception as e:
        logging.error(f"Failed to load homepage stats. Error: {str(e)}")
        raise InternalServerError()


# query a user by username
def get_user_by_username(username: str) -> User:
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


def get_user_note_list(username: str) -> Union[Response, Tuple[Response, int]]:
    validated = model.PublicProfileRequest(username=username)
    user = get_user_by_username(validated.username)

    cache_key = RedisKeys.user_notes(validated.username)
    # cache hit return notes
    cached_notes = redis_client.get(cache_key)
    if cached_notes:
        return jsonify(json.loads(cached_notes)), 200

    notes_data = []
    if user.notes:
        for note in user.notes:
            notes_data.append(
                {
                    "id": note.id,
                    "title": note.title,
                    "dateCreated": note.date_created.isoformat(),
                    "isLocked": bool(note.pin),
                }
            )

    # cache miss save notes in redis
    redis_client.set(cache_key, json.dumps(notes_data))

    return jsonify(notes_data), 200


# get a single not by id
def get_note_by_id(note_id: int) -> Notes:
    try:
        note = db.session.get(Notes, note_id)
        if note is None:
            logging.warning(f"Note not found for note_id={note_id}")
            raise NoteNotFound()
        return note
    except NoteNotFound:
        raise
    except Exception as e:
        logging.error(f"Failed to get note. Error: {str(e)}")
        raise InternalServerError()


def get_single_note() -> Union[Response, Tuple[Response, int]]:
    validated = response_body_validator(model.SingleNoteRequest)

    cache_key = RedisKeys.single_note(validated.note_id)
    # cache hit return note
    cached_note = redis_client.get(cache_key)
    if cached_note:
        note_data = json.loads(cached_note)

        # Validate PIN for cached notes
        if note_data.get("isLocked"):
            if not validated.pin:
                logging.warning(f"Pin required for note_id: {note_data['id']}")
                raise NotePinRequiredError()
            if note_data["pin"] != validated.pin:
                logging.warning(
                    f"Pin mismatch for note_id={note_data['id']}: provided={validated.pin}"
                )
                raise NotePinMismatchError()

        # remove pin and return note
        note_data.pop("pin", None)
        return jsonify(note_data), 200

    # cache miss
    note = get_note_by_id(int(validated.note_id))

    # if note has a pin
    if note.pin:
        # the request dose not contain a pin
        if not validated.pin:
            logging.warning(f"Pin required for note_id: {note.id}")
            raise NotePinRequiredError()

        # pin dosen't match
        if note.pin != validated.pin:
            logging.warning(
                f"Pin mismatch for note_id={note.id}: provided={validated.pin}"
            )
            raise NotePinMismatchError()

    note_data = {
        "username": note.author.username,
        "title": note.title,
        "text": note.text,
        "date": note.date_created.isoformat(),
        "isLocked": bool(note.pin),
        "pin": note.pin,
    }

    # cache note
    redis_client.set(cache_key, json.dumps(note_data))

    # Return without pin and locked status
    note_data.pop("pin", None)
    note_data.pop("isLocked", None)

    return jsonify(note_data), 200
