""" Unit tests for PersistentQueryKeyword.
"""
from unittest import TestCase, mock
from mock import patch
from core_explore_keyword_app.components.persistent_query_keyword import (
    api as persistent_query_keyword_api,
)
from core_explore_keyword_app.components.persistent_query_keyword.models import (
    PersistentQueryKeyword,
)
from core_main_app.commons import exceptions
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.access_control.exceptions import AccessControlError


class TestPersistentQueryKeywordGetById(TestCase):
    @patch.object(PersistentQueryKeyword, "get_by_id")
    def test_persistent_query_keyword_get_by_id_return_data_if_found(
        self, mock_get_by_id
    ):

        # Arrange
        expected_result = PersistentQueryKeyword(user_id="1")
        mock_get_by_id.return_value = expected_result
        mock_user = create_mock_user("1")

        # Act # Assert
        self.assertEqual(
            persistent_query_keyword_api.get_by_id("mock_id", mock_user),
            expected_result,
        )

    def test_persistent_query_keyword_get_by_id_raises_model_error_if_not_found(self):

        # Arrange
        mock_user = create_mock_user("1")

        # Act # Assert
        with self.assertRaises(exceptions.ModelError):
            persistent_query_keyword_api.get_by_id("mock_id", mock_user)

    @patch.object(PersistentQueryKeyword, "get_by_id")
    def test_persistent_query_keyword_get_by_id_raises_does_not_exist_error_if_not_found(
        self, mock_get_by_id
    ):

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist(message="mock error")
        mock_user = create_mock_user("1")

        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            persistent_query_keyword_api.get_by_id("mock_id", mock_user)


class TestsPersistentQueryKeywordGetByName(TestCase):
    @mock.patch.object(PersistentQueryKeyword, "get_by_name")
    def test_persistent_query_keyword_get_by_name_return_data_if_found(
        self, mock_get_by_name
    ):
        # Arrange
        expected_result = PersistentQueryKeyword(user_id="1")
        mock_get_by_name.return_value = expected_result
        mock_user = create_mock_user("1")

        # Act # Assert
        self.assertEqual(
            persistent_query_keyword_api.get_by_name("mock_name", mock_user),
            expected_result,
        )

    @patch.object(PersistentQueryKeyword, "get_by_name")
    def test_persistent_query_keyword_get_by_name_raises_does_not_exist_error_if_not_found(
        self, mock_get_by_name
    ):

        # Arrange
        mock_get_by_name.side_effect = exceptions.DoesNotExist(message="mock error")
        mock_user = create_mock_user("1")

        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            persistent_query_keyword_api.get_by_name("mock_id", mock_user)


class TestsPersistentQueryKeywordUpsert(TestCase):
    def setUp(self) -> None:
        self.mock_persistent_query_keyword = PersistentQueryKeyword(
            user_id="1",
            name="mock_keyword",
            content={"content_test"},
            templates=["5ea99316d26ebc48e475c60a"],
            data_sources=[],
        )

    @patch.object(PersistentQueryKeyword, "save")
    def test_persistent_query_keyword_upsert_return_data(self, mock_save):

        # Arrange
        mock_save.return_value = self.mock_persistent_query_keyword
        mock_user = create_mock_user("1")

        # Act
        result = persistent_query_keyword_api.upsert(
            self.mock_persistent_query_keyword, mock_user
        )

        # Assert
        self.assertIsInstance(result, PersistentQueryKeyword)


class TestsPersistentQueryKeywordDelete(TestCase):
    @patch.object(PersistentQueryKeyword, "delete")
    def test_returns_no_error(self, mock_delete):

        # Arrange
        mock_delete.return_value = None
        mock_user = create_mock_user("1")

        # Act # Assert
        self.assertEqual(
            persistent_query_keyword_api.delete(
                PersistentQueryKeyword(user_id="1"), mock_user
            ),
            None,
        )


class TestsPersistentQueryKeywordGetAll(TestCase):
    @patch.object(PersistentQueryKeyword, "get_all")
    def test_returns_no_error(self, mock_get_all):

        # Arrange
        expected_result = {
            PersistentQueryKeyword(user_id="1"),
            PersistentQueryKeyword(user_id="2"),
        }
        mock_get_all.return_value = expected_result

        mock_user = create_mock_user("1", is_superuser=True, is_staff=True)

        # Act # Assert
        self.assertEqual(
            persistent_query_keyword_api.get_all(mock_user), expected_result
        )

    @patch.object(PersistentQueryKeyword, "get_all")
    def test_persistent_query_keyword_get_all_raises_does_not_access_control_error_if_not_admin(
        self, mock_get_all
    ):

        # Arrange
        mock_get_all.side_effect = AccessControlError
        mock_user = create_mock_user("1")

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.get_all(mock_user)


class TestsPersistentQueryKeywordGetAllByUser(TestCase):
    @patch.object(PersistentQueryKeyword, "get_all_by_user")
    def test_returns_no_error(self, mock_get_all_by_user):

        # Arrange
        expected_result = {
            PersistentQueryKeyword(user_id="1"),
            PersistentQueryKeyword(user_id="1"),
        }
        mock_get_all_by_user.return_value = expected_result

        mock_user = create_mock_user("1")

        # Act # Assert
        self.assertEqual(
            persistent_query_keyword_api.get_all_by_user(mock_user), expected_result
        )
