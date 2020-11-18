""" Unit Test Persistent Query Keyword
"""

from mock import patch

from tests.components.persistent_query_keyword.fixtures.fixtures import (
    PersistentQueryKeywordFixtures,
)
from django.contrib.auth.models import AnonymousUser
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)

import core_explore_keyword_app.components.persistent_query_keyword.api as persistent_query_keyword_api
from core_explore_keyword_app.components.persistent_query_keyword.models import (
    PersistentQueryKeyword,
)
from core_main_app.access_control.exceptions import AccessControlError

from core_explore_common_app.settings import CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT

fixture_persistent_query_keyword = PersistentQueryKeywordFixtures()


class TestPersistentQueryKeywordGetById(MongoIntegrationBaseTestCase):
    fixture = fixture_persistent_query_keyword

    def test_get_by_id_as_superuser_returns_persistent_query_keyword(self):

        # Arrange
        persistent_query_keyword_id = self.fixture.persistent_query_keyword_1.id
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)

        # Act
        persistent_query_keyword = persistent_query_keyword_api.get_by_id(
            persistent_query_keyword_id, mock_user
        )

        # Assert
        self.assertTrue(isinstance(persistent_query_keyword, PersistentQueryKeyword))

    def test_get_by_id_as_owner_returns_persistent_query_keyword(self):

        # Arrange
        persistent_query_keyword_id = self.fixture.persistent_query_keyword_1.id
        mock_user = create_mock_user("1")

        # Act
        persistent_query_keyword = persistent_query_keyword_api.get_by_id(
            persistent_query_keyword_id, mock_user
        )

        # Assert
        self.assertTrue(isinstance(persistent_query_keyword, PersistentQueryKeyword))

    def test_get_by_id_as_anonymous_user(self):
        # Arrange
        persistent_query_keyword_id = self.fixture.persistent_query_keyword_1.id

        # Act # Assert
        if CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            self.assertTrue(
                isinstance(
                    persistent_query_keyword_api.get_by_id(
                        persistent_query_keyword_id, AnonymousUser()
                    ),
                    PersistentQueryKeyword,
                )
            )

        else:
            with self.assertRaises(AccessControlError):
                persistent_query_keyword_api.get_by_id(
                    persistent_query_keyword_id, AnonymousUser()
                )

    def test_get_by_id_as_user_not_owner(self):
        # Arrange
        persistent_query_keyword_id = self.fixture.persistent_query_keyword_1.id
        mock_user = create_mock_user("0")

        # Act # Assert

        self.assertTrue(
            isinstance(
                persistent_query_keyword_api.get_by_id(
                    persistent_query_keyword_id, mock_user
                ),
                PersistentQueryKeyword,
            )
        )


class TestPersistentQueryKeywordGetByName(MongoIntegrationBaseTestCase):
    fixture = fixture_persistent_query_keyword

    def test_get_by_name_as_superuser_returns_persistent_query_keyword(self):

        # Arrange
        persistent_query_keyword_name = self.fixture.persistent_query_keyword_1.name
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)

        # Act
        persistent_query_keyword = persistent_query_keyword_api.get_by_name(
            persistent_query_keyword_name, mock_user
        )

        # Assert
        self.assertTrue(isinstance(persistent_query_keyword, PersistentQueryKeyword))

    def test_get_by_name_as_owner_returns_persistent_query_keyword(self):

        # Arrange
        persistent_query_keyword_name = self.fixture.persistent_query_keyword_1.name
        mock_user = create_mock_user("1")

        # Act
        persistent_query_keyword = persistent_query_keyword_api.get_by_name(
            persistent_query_keyword_name, mock_user
        )

        # Assert
        self.assertTrue(isinstance(persistent_query_keyword, PersistentQueryKeyword))

    def test_get_by_name_as_user_not_owner(self):
        # Arrange
        persistent_query_keyword_name = self.fixture.persistent_query_keyword_1.name
        mock_user = create_mock_user("0")

        # Act # Assert
        self.assertTrue(
            isinstance(
                persistent_query_keyword_api.get_by_name(
                    persistent_query_keyword_name, mock_user
                ),
                PersistentQueryKeyword,
            )
        )

    def test_get_by_name_as_anonymous_user(self):
        # Arrange
        persistent_query_keyword_name = self.fixture.persistent_query_keyword_1.name

        # Act # Assert
        if CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            self.assertTrue(
                isinstance(
                    persistent_query_keyword_api.get_by_name(
                        persistent_query_keyword_name, AnonymousUser()
                    ),
                    PersistentQueryKeyword,
                )
            )

        else:
            with self.assertRaises(AccessControlError):
                persistent_query_keyword_api.get_by_name(
                    persistent_query_keyword_name, AnonymousUser()
                )


class TestPersistentQueryKeywordDelete(MongoIntegrationBaseTestCase):
    fixture = fixture_persistent_query_keyword

    def test_delete_others_persistent_query_keyword_as_superuser_deletes_persistent_query_keyword(
        self,
    ):
        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)

        # Act
        persistent_query_keyword_api.delete(persistent_query_keyword, mock_user)

    def test_delete_own_persistent_query_keyword_deletes_persistent_query_keyword(self):
        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1
        mock_user = create_mock_user("1")

        # Act
        persistent_query_keyword_api.delete(persistent_query_keyword, mock_user)

    def test_delete_others_persistent_query_keyword_raises_error(self):
        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1
        mock_user = create_mock_user("0")

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.delete(persistent_query_keyword, mock_user)

    def test_delete_others_user_persistent_query_keyword_as_anonymous_raises_error(
        self,
    ):
        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.delete(
                persistent_query_keyword, AnonymousUser()
            )


class TestPersistentQueryKeywordUpdate(MongoIntegrationBaseTestCase):
    fixture = fixture_persistent_query_keyword

    def test_update_others_persistent_query_keyword_as_superuser_updates_data_structure(
        self,
    ):
        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1
        persistent_query_keyword.name = "new_name_persistent_query_keyword_1"
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)
        # Act
        result = persistent_query_keyword_api.upsert(
            persistent_query_keyword, mock_user
        )
        # Assert
        self.assertTrue(isinstance(result, PersistentQueryKeyword))
        self.assertTrue(result.name, "new_name_persistent_query_keyword_1")

    def test_update_own_persistent_query_keyword_updates_persistent_query_keyword(self):
        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1
        mock_user = create_mock_user("1")
        persistent_query_keyword.name = "new_name_persistent_query_keyword_1"
        # Act
        result = persistent_query_keyword_api.upsert(
            persistent_query_keyword, mock_user
        )
        # Assert
        self.assertTrue(isinstance(result, PersistentQueryKeyword))
        self.assertTrue(result.name, "new_name_persistent_query_keyword_1")

    def test_update_others_persistent_query_keyword_raises_error(self):
        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1
        persistent_query_keyword.name = "new_name_persistent_query_keyword_1"
        mock_user = create_mock_user("0")

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.upsert(persistent_query_keyword, mock_user)

    def test_update_others_user_persistent_query_keyword_as_anonymous_raises_error(
        self,
    ):
        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.upsert(
                persistent_query_keyword, AnonymousUser()
            )


class TestPersistentQueryKeywordGetAll(MongoIntegrationBaseTestCase):
    fixture = fixture_persistent_query_keyword

    def test_get_all_as_superuser_returns_all_persistent_query_keyword(self):
        # Arrange
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)

        # Act
        result = persistent_query_keyword_api.get_all(mock_user)

        # Assert
        self.assertTrue(len(result), 3)

    def test_get_all_as_user_raises_error(self):
        # Arrange
        mock_user = create_mock_user("1")

        # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.get_all(mock_user)

    def test_get_all_as_anonymous_user_raises_error(self):
        # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.get_all(AnonymousUser())


class TestPersistentQueryExampleGetAllByUser(MongoIntegrationBaseTestCase):
    fixture = fixture_persistent_query_keyword

    def test_get_all_by_user_as_superuser_returns_all_user_persistent_query_keyword(
        self,
    ):
        # Arrange
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        # Act
        result = persistent_query_keyword_api.get_all_by_user(mock_user)

        # Assert
        self.assertTrue(len(result), 1)

    def test_get_all_by_user_returns_all_user_persistent_query_keyword(self):
        # Arrange
        mock_user = create_mock_user("1")

        # Act
        result = persistent_query_keyword_api.get_all_by_user(mock_user)

        # Assert
        self.assertTrue(len(result), 1)

    def test_get_all_as_anonymous_user_raises_error(self):
        # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.get_all_by_user(AnonymousUser())
