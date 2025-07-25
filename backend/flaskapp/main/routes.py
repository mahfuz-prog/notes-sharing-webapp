from flask import Blueprint, jsonify, request
from flaskapp.db_models import User, Notes
from flaskapp import redis_client
from flaskapp.utils import (
    validate_request_json,
    MAX_NOTE_ID_LENGTH,
    MIN_NAME_LENGTH, MAX_NAME_LENGTH,
    MIN_PIN_LENGTH, MAX_PIN_LENGTH
)


# main blueprint
main_bp = Blueprint("main", __name__)


# =====================================
# homepage
@main_bp.route("/home/")
def home():
    total_user = User.query.count()
    total_notes = Notes.query.count()

    total_char_cached = redis_client.get("total_char")
    if total_char_cached:
        total_char_value = int(total_char_cached)
    else:
        char_sum = 0
        user_notes = Notes.query.all()
        for note in user_notes:
            char_sum += len(note.title) + len(note.text)
        redis_client.setex("total_char", 600, str(char_sum)) # cache for 10 minutes
        total_char_value = char_sum
        
    data = {
        'totalUser': total_user,
        'totalNotes': total_notes,
        'totalChar': total_char_value
    }
    
    return jsonify(data), 200


# =====================================
# single note
@main_bp.route("/single-note/", methods=["POST"])
@validate_request_json({
    'username': {'required': True, 'min_len': MIN_NAME_LENGTH, 'max_len': MAX_NAME_LENGTH},
    'note_id': {'required': True, 'max_len': MAX_NOTE_ID_LENGTH},
    'pin': {'required': False, 'min_len': MIN_PIN_LENGTH, 'max_len': MAX_PIN_LENGTH}
})
def single_note(username_stripped, note_id_stripped, pin_stripped):
    # Fetch note once
    note = Notes.query.get(note_id_stripped)

    # empty note or note does not belong to username
    if not note or note.author.username != username_stripped:
        return jsonify({"error": "Note not found!"}), 404

    # if note has a pin
    if note.pin:
        # if pin not provided for a protected note
        if not pin_stripped:
            return jsonify({"message": "Pin required!"}), 200

        # big pin or invalid pin length
        if not (MIN_PIN_LENGTH <= len(pin_stripped) <= MAX_PIN_LENGTH):
            return jsonify({"error": "Something went wrong!"}), 400
        
        # invalid pin
        if note.pin != pin_stripped:
            return jsonify({"error": "Invalid pin."}), 403

    # return note data
    data = {
        "username": note.author.username,
        "title": note.title,
        "text": note.text,
        "date": note.date_created
    }

    return jsonify(data), 200


# =====================================
# user profile
@main_bp.route("/user-profile/<string:username>/")
def user_profile(username):
    username_stripped = username.strip().replace(' ', '-').lower()

    # Validate username length
    if not (MIN_NAME_LENGTH <= len(username_stripped) <= MAX_NAME_LENGTH):
        return jsonify({"error": f"Username must be between {MIN_NAME_LENGTH} and {MAX_NAME_LENGTH} characters."}), 400

    # load user
    user = User.query.filter_by(username=username_stripped).first()
    
    # if no user found
    if not user:
        return jsonify({"error": "User not found!"}), 404

    notes_data = []
    if user.notes:
        for note in user.notes:
            notes_data.append({
                'id': note.id,
                'title': note.title,
                'dateCreated': note.date_created,
                'isLocked': bool(note.pin)
            })

    return jsonify(notes_data), 200