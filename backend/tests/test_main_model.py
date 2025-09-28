import pytest
from flaskapp.main import model
from flask import current_app
from pydantic import ValidationError


class TestModel:
    # PublicProfileRequest
    def test_PublicProfileRequest_valid(self):
        validated = model.PublicProfileRequest(username="test_user")
        assert validated.username == "test_user"

    def test_PublicProfileRequest_username_too_short(self):
        MIN_NAME_LENGTH = current_app.config["MIN_NAME_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.PublicProfileRequest(username="t" * (MIN_NAME_LENGTH - 1))
        assert f"String should have at least {MIN_NAME_LENGTH} characters" in str(
            exc_info.value
        )

    def test_PublicProfileRequest_username_too_long(self):
        MAX_NAME_LENGTH = current_app.config["MAX_NAME_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.PublicProfileRequest(username="t" * (MAX_NAME_LENGTH + 1))
        assert f"String should have at most {MAX_NAME_LENGTH} characters" in str(
            exc_info.value
        )

    def test_PublicProfileRequest_invalid_type(self):
        with pytest.raises(ValidationError) as exc_info:
            model.PublicProfileRequest(username=123)
        assert "Input should be a valid string" in str(exc_info.value)

    # SingleNoteRequest
    def test_SingleNoteRequest_valid(self):
        validated = model.SingleNoteRequest(
            username="validuser", note_id="note123", pin="1234"
        )
        assert validated.username == "validuser"
        assert validated.note_id == "note123"
        assert validated.pin == "1234"

    def test_SingleNoteRequest_username_too_short(self):
        MIN_NAME_LENGTH = current_app.config["MIN_NAME_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.SingleNoteRequest(
                username="t" * (MIN_NAME_LENGTH - 1),
                note_id="note123",
                pin="1234",
            )
        assert f"String should have at least {MIN_NAME_LENGTH} characters" in str(
            exc_info.value
        )

    def test_SingleNoteRequest_username_too_long(self):
        MAX_NAME_LENGTH = current_app.config["MAX_NAME_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.SingleNoteRequest(
                username="t" * (MAX_NAME_LENGTH + 1),
                note_id="note123",
                pin="1234",
            )
        assert f"String should have at most {MAX_NAME_LENGTH} characters" in str(
            exc_info.value
        )

    def test_SingleNoteRequest_note_id_too_long(self):
        MAX_NOTE_ID_LENGTH = current_app.config["MAX_NOTE_ID_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.SingleNoteRequest(
                username="validuser",
                note_id="t" * (MAX_NOTE_ID_LENGTH + 1),
                pin="1234",
            )
        assert f"String should have at most {MAX_NOTE_ID_LENGTH} characters" in str(
            exc_info.value
        )

    def test_SingleNoteRequest_pin_too_short(self):
        MIN_PIN_LENGTH = current_app.config["MIN_PIN_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.SingleNoteRequest(
                username="validuser",
                note_id="note123",
                pin="t" * (MIN_PIN_LENGTH - 1),
            )
        assert f"String should have at least {MIN_PIN_LENGTH} characters" in str(
            exc_info.value
        )
