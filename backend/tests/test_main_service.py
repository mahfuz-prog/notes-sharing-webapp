import pytest
from unittest import mock
from flaskapp.config import Config
import flaskapp.main.service as main_service
from flaskapp.exceptions import InternalServerError, UserNotFoundError, UsernameError


class TestMainService:
    def test_homepage_stats(self, app):
        data = main_service.homepage_stats()
        assert data["totalUser"] == 0
        assert data["totalNotes"] == 0
        assert data["totalChar"] == 0

    def test_homepage_stats_error(self, app):
        with pytest.raises(InternalServerError) as exc_info:
            with mock.patch(
                "flaskapp.main.service.User.query", new_callable=mock.PropertyMock
            ) as mocked_query:
                mocked_query.return_value.count.side_effect = Exception
                main_service.homepage_stats()

            # Check exception details
            assert exc_info.value.code == 500
            assert exc_info.value.description == "An unexpected error occurred"

    def test_get_user(self, app):
        pass

    def test_get_user_error(self, app):
        with pytest.raises(UserNotFoundError) as exc_info:
            main_service.get_user("test user")
            assert exc_info.value.code == 404
            assert exc_info.value.description == "User not found"

        with pytest.raises(InternalServerError) as exc_info:
            with mock.patch(
                "flaskapp.main.service.User.query", new_callable=mock.PropertyMock
            ) as mocked_query:
                mocked_query.return_value.filter_by.side_effect = Exception
                main_service.get_user("test_user")

            # Check exception details
            assert exc_info.value.code == 500
            assert exc_info.value.description == "An unexpected error occurred"

    def test_get_user_note_list(self, app):
        pass

    def test_get_user_note_list_error(self, app):
        with pytest.raises(UsernameError) as exc_info:
            main_service.get_user_note_list("a")
            assert exc_info.value.code == 400
            MIN_NAME_LENGTH = Config["MIN_NAME_LENGTH"]
            MAX_NAME_LENGTH = Config["MAX_NAME_LENGTH"]
            assert (
                exc_info.value.description
                == f"Username must be between {MIN_NAME_LENGTH} and {MAX_NAME_LENGTH} characters"
            )
