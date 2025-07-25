from flask import Blueprint, jsonify, request
from flaskapp.db_models import Notes
from flaskapp import db
from flaskapp.utils import (
	login_required,
	validate_request_json,
	MAX_NOTE_ID_LENGTH,
	MAX_TITLE_LENGTH, MIN_TITLE_LENGTH,
	MAX_TEXT_LENGTH, MIN_TEXT_LENGTH,
	MAX_PIN_LENGTH, MIN_PIN_LENGTH
)


# notes blueprint
notes_bp = Blueprint("notes", __name__)


# =========================================
# load notes
@notes_bp.route("/")
@login_required
def note_list(current_user):
	page = request.args.get('page', 1, type=int)
	note_list = Notes.query.filter_by(user_id=current_user.id).order_by(Notes.date_created.desc()).paginate(page=page, per_page=6)

	pagination = {
		"currentPage": note_list.page,
		"hasPrev": note_list.has_prev,
		"hasNext": note_list.has_next,
		"pageList": list(note_list.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=0))
	}

	notes = []
	for note in note_list.items:
		notes.append({
			'id': note.id, 
			'info': {
				'title':note.title, 
				'dateCreated':note.date_created, 
				'text': note.text, 
				'pin': note.pin
				}
			})

	data = { "pagination": pagination, "notes": notes}
	
	return jsonify(data), 200


# ==============================================
# delete note
@notes_bp.route("/delete-note/", methods=["POST"])
@login_required
@validate_request_json({
	'note_id': {'required': True, 'max_len': MAX_NOTE_ID_LENGTH}
})
def delete_note(current_user, note_id_stripped):
	# load note
	note = Notes.query.get(note_id_stripped)
	if not note:
		return jsonify({'error': 'Note not found!'}), 404

	if note.author != current_user:
		return jsonify({'error': 'Delete not allowed!'}), 403

	# delete note
	title = note.title
	db.session.delete(note)
	db.session.commit()
	
	data = {"title": title, "id": note_id_stripped}

	return jsonify(data), 200


# ========================================================
# create new note
@notes_bp.route("/new-note/", methods=["POST"])
@login_required
@validate_request_json({
	'title': {'required': True, 'min_len': MIN_TITLE_LENGTH, 'max_len': MAX_TITLE_LENGTH},
	'text': {'required': True, 'min_len': MIN_TEXT_LENGTH, 'max_len': MAX_TEXT_LENGTH},
	'pin': {'required': False, 'min_len': MIN_PIN_LENGTH, 'max_len': MAX_PIN_LENGTH}
})
def new_note(current_user, title_stripped, text_stripped, pin_stripped):
	# create new note
	note = Notes(pin=pin_stripped, title=title_stripped, text=text_stripped, author=current_user)
	db.session.add(note)
	db.session.commit()

	data = {'id': note.id, 'info': {'title': note.title, 'dateCreated': note.date_created, 'text': note.text, 'pin': note.pin}}

	return jsonify(data), 200


# ==============================================
# update note
@notes_bp.route("/update-note/", methods=["POST"])
@login_required
@validate_request_json({
	'note_id': {'required': True, 'max_len': MAX_NOTE_ID_LENGTH},
	'title': {'required': True, 'min_len': MIN_TITLE_LENGTH, 'max_len': MAX_TITLE_LENGTH},
	'text': {'required': True, 'min_len': MIN_TEXT_LENGTH, 'max_len': MAX_TEXT_LENGTH},
	'pin': {'required': False, 'min_len': MIN_PIN_LENGTH, 'max_len': MAX_PIN_LENGTH}
})
def update_note(current_user, note_id_stripped, title_stripped, text_stripped, pin_stripped):
	# load note
	note = Notes.query.get(note_id_stripped)
	if not note:
		return jsonify({'error': 'Note not found!'}), 404

	# check note belong from current user
	if note.author != current_user:
		return jsonify({'error': 'Update not allowed!'}), 403

	# changes in database
	note.title = title_stripped
	note.text = text_stripped
	note.pin = pin_stripped
	db.session.commit()

	data = { "id": note.id, "title": note.title, "text": note.text, "pin": note.pin }

	return jsonify(data), 200