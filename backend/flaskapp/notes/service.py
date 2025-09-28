import logging
from typing import Union, Tuple
from flask import request, jsonify, Response
from flaskapp import db
from flaskapp.caching import redis_client, RedisKeys
from flaskapp.db_models import Notes
from flaskapp.notes import model
from flaskapp.utils import response_body_validator
from flaskapp.exceptions import (
    NoteNotFound,
    NoteDeleteForbiddenError,
    InternalServerError,
)


def current_user_note_list(current_user):
    page = request.args.get("page", 1, type=int)
    note_list = (
        Notes.query.filter_by(user_id=current_user.id)
        .order_by(Notes.date_created.desc())
        .paginate(page=page, per_page=6)
    )

    pagination = {
        "currentPage": note_list.page,
        "hasPrev": note_list.has_prev,
        "hasNext": note_list.has_next,
        "pageList": list(
            note_list.iter_pages(
                left_edge=1, right_edge=1, left_current=1, right_current=0
            )
        ),
    }

    notes = []
    for note in note_list.items:
        notes.append(
            {
                "id": note.id,
                "info": {
                    "title": note.title,
                    "dateCreated": note.date_created,
                    "text": note.text,
                    "pin": note.pin,
                },
            }
        )

    return jsonify({"pagination": pagination, "notes": notes}), 200


# get a single note by id
def get_note_by_id(note_id) -> Notes:
    note = db.session.get(Notes, note_id)
    if not note:
        logging.warning(f"Note not found for id={note_id}")
        raise NoteNotFound()

    return note


# delete note
def delete_note_by_id(current_user, note_id) -> Union[Response, Tuple[Response, int]]:
    validated = model.DeleteNoteRequest(note_id=note_id)

    note = get_note_by_id(validated.note_id)
    if note.author != current_user:
        logging.error(f"{note.author} is not current_user")
        raise NoteDeleteForbiddenError()

    try:
        title = note.title
        db.session.delete(note)
        db.session.commit()
    except Exception as e:
        logging.error(f"Failed to delete note id={validated.note_id}. Error: {str(e)}")
        raise InternalServerError()

    # after delete a note if the note is cached then delete the cache
    # main blueprint -> get_user_note_list service
    cache_key = RedisKeys.user_notes(current_user.username)
    cached_notes = redis_client.get(cache_key)
    if cached_notes:
        redis_client.delete(cache_key)

    # if only the deleted note stored on cache
    # main blueprint -> get_single_note
    cache_key = RedisKeys.single_note(validated.note_id)
    cached_notes = redis_client.get(cache_key)
    if cached_notes:
        redis_client.delete(cache_key)

    return jsonify({"title": title, "id": validated.note_id}), 200


# create a new note
def create_note(current_user) -> Union[Response, Tuple[Response, int]]:
    validated = response_body_validator(model.CreateNewNoteRequest)

    try:
        note = Notes(
            pin=validated.pin,
            title=validated.title,
            text=validated.text,
            author=current_user,
        )
        db.session.add(note)
        db.session.commit()

        # after create a new note if the notes are cached for this user
        # main blueprint -> get_user_note_list service
        cache_key = RedisKeys.user_notes(current_user.username)
        cached_notes = redis_client.get(cache_key)
        if cached_notes:
            redis_client.delete(cache_key)
    except Exception as e:
        logging.error(f"Failed to create new note. Error {str(e)}")
        raise InternalServerError()

    data = {
        "id": note.id,
        "info": {
            "title": note.title,
            "dateCreated": note.date_created,
            "text": note.text,
            "pin": note.pin,
        },
    }

    return jsonify(data), 201


# update a user note
def edit_user_note(current_user) -> Union[Response, Tuple[Response, int]]:
    validated = response_body_validator(model.UpdateNoteRequest)

    note = get_note_by_id(validated.note_id)
    if note.author != current_user:
        logging.error(f"{note.author} is not current_user")
        raise NoteDeleteForbiddenError()

    try:
        # changes in database
        note.title = validated.title
        note.text = validated.text
        note.pin = validated.pin
        db.session.commit()
    except Exception as e:
        logging.error(f"Failed to edit note id={validated.note_id}. Error: {str(e)}")
        raise InternalServerError()

    # after edit a note if the notes are cached for this user
    # main blueprint -> get_user_note_list service
    cache_key = RedisKeys.user_notes(current_user.username)
    cached_notes = redis_client.get(cache_key)
    if cached_notes:
        redis_client.delete(cache_key)

    # if only the edited note stored on cache
    # main blueprint -> get_single_note
    cache_key = RedisKeys.single_note(validated.note_id)
    cached_notes = redis_client.get(cache_key)
    if cached_notes:
        redis_client.delete(cache_key)

    return jsonify(
        {"id": note.id, "title": note.title, "text": note.text, "pin": note.pin}
    ), 200
