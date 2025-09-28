import pytest
from pydantic import ValidationError
from flask import current_app
from flaskapp.notes import model


class TestNoteModels:
    def test_DeleteNoteRequest_valid(self):
        validated = model.DeleteNoteRequest(note_id=123)
        assert validated.note_id == 123

    def test_DeleteNoteRequest_invalid_type(self):
        with pytest.raises(ValidationError) as exc_info:
            model.DeleteNoteRequest(note_id="not-an-int")
        assert "Input should be a valid integer" in str(exc_info.value)

    def test_CreateNewNoteRequest_valid(self):
        validated = model.CreateNewNoteRequest(
            title="Valid Title", text="Some valid text here", pin="1234"
        )
        assert validated.title == "Valid Title"
        assert validated.text == "Some valid text here"
        assert validated.pin == "1234"

    def test_CreateNewNoteRequest_invalid_title_too_short(self):
        MIN_TITLE_LENGTH = current_app.config["MIN_TITLE_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.CreateNewNoteRequest(
                title="t" * (MIN_TITLE_LENGTH - 1), text="Valid text", pin="1234"
            )
        assert f"String should have at least {MIN_TITLE_LENGTH} character" in str(
            exc_info.value
        )

    def test_CreateNewNoteRequest_invalid_text_too_long(self):
        MAX_TEXT_LENGTH = current_app.config["MAX_TEXT_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.CreateNewNoteRequest(
                title="Valid Title", text="t" * (MAX_TEXT_LENGTH + 1), pin="1234"
            )
        assert f"String should have at most {MAX_TEXT_LENGTH} characters" in str(
            exc_info.value
        )

    def test_CreateNewNoteRequest_invalid_pin_too_long(self):
        MAX_PIN_LENGTH = current_app.config["MAX_PIN_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.CreateNewNoteRequest(
                title="Valid Title",
                text="Valid text",
                pin="t" * (MAX_PIN_LENGTH + 1),
            )
        assert f"String should have at most {MAX_PIN_LENGTH} characters" in str(
            exc_info.value
        )

    def test_UpdateNoteRequest_valid(self):
        validated = model.UpdateNoteRequest(
            note_id=42, title="Updated Title", text="Updated text content", pin="5678"
        )
        assert validated.note_id == 42
        assert validated.title == "Updated Title"
        assert validated.text == "Updated text content"
        assert validated.pin == "5678"

    def test_UpdateNoteRequest_invalid_note_id_type(self):
        with pytest.raises(ValidationError) as exc_info:
            model.UpdateNoteRequest(
                note_id="not-int",
                title="Valid Title",
                text="Valid text",
                pin="5678",
            )
        assert "Input should be a valid integer" in str(exc_info.value)

    def test_UpdateNoteRequest_invalid_title_too_long(self):
        MAX_TITLE_LENGTH = current_app.config["MAX_TITLE_LENGTH"]
        with pytest.raises(ValidationError) as exc_info:
            model.UpdateNoteRequest(
                note_id=1,
                title="t" * (MAX_TITLE_LENGTH + 1),
                text="Valid text",
                pin="5678",
            )
        assert f"String should have at most {MAX_TITLE_LENGTH} characters" in str(
            exc_info.value
        )
