""" Unit Test Persistent Query Keyword
"""

from django.contrib.auth.models import AnonymousUser

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_explore_common_app.settings import (
    CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT,
)
import core_explore_keyword_app.components.persistent_query_keyword.api as persistent_query_keyword_api

from core_explore_keyword_app.components.persistent_query_keyword.models import (
    PersistentQueryKeyword,
)
from tests.components.persistent_query_keyword.fixtures.fixtures import (
    PersistentQueryKeywordFixtures,
)

fixture_persistent_query_keyword = PersistentQueryKeywordFixtures()


class TestPersistentQueryKeywordGetById(IntegrationBaseTestCase):
    """Test Persistent Query Keyword Get By Id"""

    fixture = fixture_persistent_query_keyword

    def test_get_by_id_as_superuser_returns_persistent_query_keyword(self):
        """test_get_by_id_as_superuser_returns_persistent_query_keyword"""

        # Arrange
        persistent_query_keyword_id = (
            self.fixture.persistent_query_keyword_1.id
        )
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)

        # Act
        persistent_query_keyword = persistent_query_keyword_api.get_by_id(
            persistent_query_keyword_id, mock_user
        )

        # Assert
        self.assertTrue(
            isinstance(persistent_query_keyword, PersistentQueryKeyword)
        )

    def test_get_by_id_as_owner_returns_persistent_query_keyword(self):
        """test_get_by_id_as_owner_returns_persistent_query_keyword"""

        # Arrange
        persistent_query_keyword_id = (
            self.fixture.persistent_query_keyword_1.id
        )
        mock_user = create_mock_user("1")

        # Act
        persistent_query_keyword = persistent_query_keyword_api.get_by_id(
            persistent_query_keyword_id, mock_user
        )

        # Assert
        self.assertTrue(
            isinstance(persistent_query_keyword, PersistentQueryKeyword)
        )

    def test_get_by_id_as_anonymous_user(self):
        """test_get_by_id_as_anonymous_user"""

        # Arrange
        persistent_query_keyword_id = (
            self.fixture.persistent_query_keyword_1.id
        )

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
        """test_get_by_id_as_user_not_owner"""

        # Arrange
        persistent_query_keyword_id = (
            self.fixture.persistent_query_keyword_1.id
        )
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


class TestPersistentQueryKeywordGetByName(IntegrationBaseTestCase):
    """Test Persistent Query Keyword Get By Name"""

    fixture = fixture_persistent_query_keyword

    def test_get_by_name_as_superuser_returns_persistent_query_keyword(self):
        """test_get_by_name_as_superuser_returns_persistent_query_keyword"""

        # Arrange
        persistent_query_keyword_name = (
            self.fixture.persistent_query_keyword_1.name
        )
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)

        # Act
        persistent_query_keyword = persistent_query_keyword_api.get_by_name(
            persistent_query_keyword_name, mock_user
        )

        # Assert
        self.assertTrue(
            isinstance(persistent_query_keyword, PersistentQueryKeyword)
        )

    def test_get_by_name_as_owner_returns_persistent_query_keyword(self):
        """test_get_by_name_as_owner_returns_persistent_query_keyword"""

        # Arrange
        persistent_query_keyword_name = (
            self.fixture.persistent_query_keyword_1.name
        )
        mock_user = create_mock_user("1")

        # Act
        persistent_query_keyword = persistent_query_keyword_api.get_by_name(
            persistent_query_keyword_name, mock_user
        )

        # Assert
        self.assertTrue(
            isinstance(persistent_query_keyword, PersistentQueryKeyword)
        )

    def test_get_by_name_as_user_not_owner(self):
        """test_get_by_name_as_user_not_owner"""

        # Arrange
        persistent_query_keyword_name = (
            self.fixture.persistent_query_keyword_1.name
        )
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
        """test_get_by_name_as_anonymous_user"""

        # Arrange
        persistent_query_keyword_name = (
            self.fixture.persistent_query_keyword_1.name
        )

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


class TestPersistentQueryKeywordDelete(IntegrationBaseTestCase):
    """Test Persistent Query Keyword Delete"""

    fixture = fixture_persistent_query_keyword

    def test_delete_others_persistent_query_keyword_as_superuser_deletes_persistent_query_keyword(
        self,
    ):
        """test_delete_others_persistent_query_keyword_as_superuser_deletes_persistent_query_keyword"""

        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)

        # Act
        persistent_query_keyword_api.delete(
            persistent_query_keyword, mock_user
        )

    def test_delete_own_persistent_query_keyword_deletes_persistent_query_keyword(
        self,
    ):
        """test_delete_own_persistent_query_keyword_deletes_persistent_query_keyword"""

        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1
        mock_user = create_mock_user("1")

        # Act
        persistent_query_keyword_api.delete(
            persistent_query_keyword, mock_user
        )

    def test_delete_others_persistent_query_keyword_raises_error(self):
        """test_delete_others_persistent_query_keyword_raises_error"""

        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1
        mock_user = create_mock_user("0")

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.delete(
                persistent_query_keyword, mock_user
            )

    def test_delete_others_user_persistent_query_keyword_as_anonymous_raises_error(
        self,
    ):
        """test_delete_others_user_persistent_query_keyword_as_anonymous_raises_error"""

        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.delete(
                persistent_query_keyword, AnonymousUser()
            )


class TestPersistentQueryKeywordUpdate(IntegrationBaseTestCase):
    """Test Persistent Query Keyword Update"""

    fixture = fixture_persistent_query_keyword

    def test_update_others_persistent_query_keyword_as_superuser_updates_persistent_query_keyword(
        self,
    ):
        """test_update_others_persistent_query_keyword_as_superuser_updates_persistent_query_keyword"""

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

    def test_update_own_persistent_query_keyword_updates_persistent_query_keyword(
        self,
    ):
        """test_update_own_persistent_query_keyword_updates_persistent_query_keyword"""

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
        """test_update_others_persistent_query_keyword_raises_error"""

        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1
        persistent_query_keyword.name = "new_name_persistent_query_keyword_1"
        mock_user = create_mock_user("0")

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.upsert(
                persistent_query_keyword, mock_user
            )

    def test_update_others_user_persistent_query_keyword_as_anonymous_raises_error(
        self,
    ):
        """test_update_others_user_persistent_query_keyword_as_anonymous_raises_error"""

        # Arrange
        persistent_query_keyword = self.fixture.persistent_query_keyword_1

        # Act # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.upsert(
                persistent_query_keyword, AnonymousUser()
            )


class TestPersistentQueryKeywordCreate(IntegrationBaseTestCase):
    """Test Persistent Query Keyword Create"""

    fixture = fixture_persistent_query_keyword

    def test_create_others_persistent_query_keyword_as_superuser_creates_persistent_query_keyword(
        self,
    ):
        """test_create_others_persistent_query_keyword_as_superuser_creates_persistent_query_keyword"""

        # Arrange
        persistent_query_keyword = PersistentQueryKeyword(
            name="new_persistent_query_keyword", user_id="0"
        )
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)
        # Act
        result = persistent_query_keyword_api.upsert(
            persistent_query_keyword, mock_user
        )
        # Assert
        self.assertTrue(isinstance(result, PersistentQueryKeyword))
        self.assertTrue(result.name, "new_persistent_query_keyword")

    def test_create_persistent_query_keyword_as_user_creates_persistent_query_keyword(
        self,
    ):
        """test_create_persistent_query_keyword_as_user_creates_persistent_query_keyword"""

        # Arrange
        persistent_query_keyword = PersistentQueryKeyword(
            name="new_persistent_query_keyword", user_id="1"
        )
        mock_user = create_mock_user("1")

        # Act
        result = persistent_query_keyword_api.upsert(
            persistent_query_keyword, mock_user
        )
        # Assert
        self.assertTrue(isinstance(result, PersistentQueryKeyword))
        self.assertTrue(result.name, "new_persistent_query_keyword")

    def test_create_persistent_query_keyword_as_anonymous_user(self):
        """test_create_persistent_query_keyword_as_anonymous_user"""

        # Arrange
        persistent_query_keyword = PersistentQueryKeyword(
            name="new_persistent_query_keyword", user_id="None"
        )

        # Act
        if CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT:
            result = persistent_query_keyword_api.upsert(
                persistent_query_keyword, AnonymousUser()
            )
            # Assert
            self.assertTrue(isinstance(result, PersistentQueryKeyword))
            self.assertTrue(result.name, "new_persistent_query_keyword")

        else:
            with self.assertRaises(AccessControlError):
                persistent_query_keyword_api.upsert(
                    persistent_query_keyword, AnonymousUser()
                )


class TestPersistentQueryKeywordGetAll(IntegrationBaseTestCase):
    """Test Persistent Query Keyword Get All"""

    fixture = fixture_persistent_query_keyword

    def test_get_all_as_superuser_returns_all_persistent_query_keyword(self):
        """test_get_all_as_superuser_returns_all_persistent_query_keyword"""

        # Arrange
        mock_user = create_mock_user("0", is_staff=True, is_superuser=True)

        # Act
        result = persistent_query_keyword_api.get_all(mock_user)

        # Assert
        self.assertTrue(len(result), 3)

    def test_get_all_as_user_raises_error(self):
        """test_get_all_as_user_raises_error"""

        # Arrange
        mock_user = create_mock_user("1")

        # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.get_all(mock_user)

    def test_get_all_as_anonymous_user_raises_error(self):
        """test_get_all_as_anonymous_user_raises_error"""

        # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.get_all(AnonymousUser())


class TestPersistentQueryKeywordGetAllByUser(IntegrationBaseTestCase):
    """Test Persistent Query Keyword Get All By User"""

    fixture = fixture_persistent_query_keyword

    def test_get_all_by_user_as_superuser_returns_all_user_persistent_query_keyword(
        self,
    ):
        """test_get_all_by_user_as_superuser_returns_all_user_persistent_query_keyword"""

        # Arrange
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        # Act
        result = persistent_query_keyword_api.get_all_by_user(mock_user)

        # Assert
        self.assertTrue(len(result), 1)

    def test_get_all_by_user_returns_all_user_persistent_query_keyword(self):
        """test_get_all_by_user_returns_all_user_persistent_query_keyword"""

        # Arrange
        mock_user = create_mock_user("1")

        # Act
        result = persistent_query_keyword_api.get_all_by_user(mock_user)

        # Assert
        self.assertTrue(len(result), 1)

    def test_get_all_as_anonymous_user_raises_error(self):
        """test_get_all_as_anonymous_user_raises_error"""

        # Assert
        with self.assertRaises(AccessControlError):
            persistent_query_keyword_api.get_all_by_user(AnonymousUser())
