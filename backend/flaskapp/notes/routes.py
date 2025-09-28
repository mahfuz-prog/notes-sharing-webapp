from flask import Blueprint
from flaskapp.utils import login_required
from flaskapp.notes import service

# notes blueprint
notes_bp = Blueprint("notes", __name__)


# load notes
@notes_bp.route("/")
@login_required
def note_list(current_user):
    return service.current_user_note_list(current_user)


# delete note
@notes_bp.route("/delete-note/<int:note_id>/", methods=["DELETE"])
@login_required
def delete_note(current_user, note_id):
    return service.delete_note_by_id(current_user, note_id)


# create new note
@notes_bp.route("/new-note/", methods=["POST"])
@login_required
def new_note(current_user):
    return service.create_note(current_user)


# update note
@notes_bp.route("/update-note/", methods=["PUT"])
@login_required
def update_note(current_user):
    return service.edit_user_note(current_user)
