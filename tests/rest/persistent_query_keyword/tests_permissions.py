""" Authentication tests for PersistentQueryKeyword REST API.
"""
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase
from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
import core_explore_keyword_app.components.persistent_query_keyword.api as persistent_query_keyword_api
from core_explore_keyword_app.components.persistent_query_keyword.models import (
    PersistentQueryKeyword,
)
from core_explore_keyword_app.rest.persistent_query_keyword import (
    views as persistent_query_keyword_views,
)
from core_explore_keyword_app.rest.persistent_query_keyword.serializers import (
    PersistentQueryKeywordSerializer,
    PersistentQueryKeywordAdminSerializer,
)


class TestAdminPersistentQueryKeywordListGet(SimpleTestCase):
    """Test Admin Persistent Query Keyword List Get"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_get(
            persistent_query_keyword_views.AdminPersistentQueryKeywordList.as_view(),
            AnonymousUser(),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            persistent_query_keyword_views.AdminPersistentQueryKeywordList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(PersistentQueryKeyword, "get_all")
    def test_superuser_returns_http_200(self, get_all):
        """test_superuser_returns_http_200"""

        get_all.return_value = {}
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_get(
            persistent_query_keyword_views.AdminPersistentQueryKeywordList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPersistentQueryKeywordListGet(SimpleTestCase):
    """Test Persistent Query Keyword List Get"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_get(
            persistent_query_keyword_views.PersistentQueryKeywordList.as_view(),
            AnonymousUser(),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(PersistentQueryKeyword, "get_all_by_user")
    def test_authenticated_returns_http_200(self, get_all):
        """test_authenticated_returns_http_200"""

        get_all.return_value = {}
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            persistent_query_keyword_views.PersistentQueryKeywordList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(PersistentQueryKeyword, "get_all_by_user")
    def test_superuser_returns_http_200(self, get_all):
        """test_superuser_returns_http_200"""

        get_all.return_value = {}
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_get(
            persistent_query_keyword_views.PersistentQueryKeywordList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPersistentQueryKeywordListPost(SimpleTestCase):
    """Test Persistent Query Keyword List Post"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_post(
            persistent_query_keyword_views.AdminPersistentQueryKeywordList.as_view(),
            AnonymousUser(),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(PersistentQueryKeywordSerializer, "is_valid")
    @patch.object(PersistentQueryKeywordSerializer, "save")
    @patch.object(PersistentQueryKeywordSerializer, "data")
    def test_authenticated_returns_http_201(
        self,
        persistent_query_keyword_serializer_data,
        persistent_query_keyword_serializer_save,
        persistent_query_keyword_serializer_is_valid,
    ):
        """test_authenticated_returns_http_201"""

        persistent_query_keyword_serializer_is_valid.return_value = True
        persistent_query_keyword_serializer_save.return_value = None
        persistent_query_keyword_serializer_data.return_value = {}
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            persistent_query_keyword_views.PersistentQueryKeywordList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(PersistentQueryKeywordAdminSerializer, "is_valid")
    @patch.object(PersistentQueryKeywordAdminSerializer, "save")
    @patch.object(PersistentQueryKeywordAdminSerializer, "data")
    def test_superuser_returns_http_201(
        self,
        persistent_query_keyword_serializer_data,
        persistent_query_keyword_serializer_save,
        persistent_query_keyword_serializer_is_valid,
    ):
        """test_superuser_returns_http_201"""

        persistent_query_keyword_serializer_is_valid.return_value = True
        persistent_query_keyword_serializer_save.return_value = None
        persistent_query_keyword_serializer_data.return_value = {}

        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_post(
            persistent_query_keyword_views.AdminPersistentQueryKeywordList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestAdminPersistentQueryKeywordListPost(SimpleTestCase):
    """Test Admin Persistent Query Keyword List Post"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_post(
            persistent_query_keyword_views.AdminPersistentQueryKeywordList.as_view(),
            AnonymousUser(),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            persistent_query_keyword_views.AdminPersistentQueryKeywordList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(PersistentQueryKeywordAdminSerializer, "is_valid")
    @patch.object(PersistentQueryKeywordAdminSerializer, "save")
    @patch.object(PersistentQueryKeywordAdminSerializer, "data")
    def test_superuser_returns_http_201(
        self,
        persistent_query_keyword_serializer_data,
        persistent_query_keyword_serializer_save,
        persistent_query_keyword_serializer_is_valid,
    ):
        """test_superuser_returns_http_201"""

        persistent_query_keyword_serializer_is_valid.return_value = True
        persistent_query_keyword_serializer_save.return_value = None
        persistent_query_keyword_serializer_data.return_value = {}

        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_post(
            persistent_query_keyword_views.AdminPersistentQueryKeywordList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestPersistentQueryKeywordDetailGet(SimpleTestCase):
    """Test Persistent Query Keyword Detail Get"""

    @patch.object(persistent_query_keyword_api, "get_by_id")
    @patch.object(PersistentQueryKeywordSerializer, "data")
    def test_anonymous_returns_http_403(
        self,
        mock_persistent_query_keyword_serializer_data,
        mock_persistent_query_keyword_api_get_by_id,
    ):
        """test_anonymous_returns_http_403"""

        mock_persistent_query_keyword_serializer_data.return_value = {}
        mock_persistent_query_keyword_api_get_by_id.return_value = None
        response = RequestMock.do_request_get(
            persistent_query_keyword_views.PersistentQueryKeywordDetail.as_view(),
            AnonymousUser(),
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(persistent_query_keyword_api, "get_by_id")
    @patch.object(PersistentQueryKeywordSerializer, "data")
    def test_authenticated_returns_http_200(
        self,
        mock_persistent_query_keyword_serializer_data,
        mock_persistent_query_keyword_api_get_by_id,
    ):
        """test_authenticated_returns_http_200"""

        mock_persistent_query_keyword_serializer_data.return_value = {}
        mock_persistent_query_keyword_api_get_by_id.return_value = None
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            persistent_query_keyword_views.PersistentQueryKeywordDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(persistent_query_keyword_api, "get_by_id")
    @patch.object(PersistentQueryKeywordSerializer, "data")
    def test_superuser_returns_http_200(
        self,
        mock_persistent_query_keyword_serializer_data,
        mock_persistent_query_keyword_api_get_by_id,
    ):
        """test_superuser_returns_http_200"""

        mock_persistent_query_keyword_serializer_data.return_value = {}
        mock_persistent_query_keyword_api_get_by_id.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            persistent_query_keyword_views.PersistentQueryKeywordDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPersistentQueryKeywordDetailPatch(SimpleTestCase):
    """Test Persistent Query Keyword Detail Patch"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_patch(
            persistent_query_keyword_views.PersistentQueryKeywordDetail.as_view(),
            AnonymousUser(),
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(persistent_query_keyword_api, "get_by_id")
    @patch.object(PersistentQueryKeywordSerializer, "is_valid")
    @patch.object(PersistentQueryKeywordSerializer, "save")
    @patch.object(PersistentQueryKeywordSerializer, "data")
    def test_authenticated_returns_http_200(
        self,
        mock_persistent_query_keyword_data,
        mock_persistent_query_keyword_save,
        mock_persistent_query_keyword_is_valid,
        mock_persistent_query_keyword_api_get_by_id,
    ):
        """test_authenticated_returns_http_200"""

        mock_persistent_query_keyword_data.return_value = {}
        mock_persistent_query_keyword_save.return_value = None
        mock_persistent_query_keyword_is_valid.return_value = True
        mock_persistent_query_keyword_api_get_by_id.return_value = None
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            persistent_query_keyword_views.PersistentQueryKeywordDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(persistent_query_keyword_api, "get_by_id")
    @patch.object(PersistentQueryKeywordSerializer, "is_valid")
    @patch.object(PersistentQueryKeywordSerializer, "save")
    @patch.object(PersistentQueryKeywordSerializer, "data")
    def test_superuser_returns_http_200(
        self,
        mock_persistent_query_keyword_data,
        mock_persistent_query_keyword_save,
        mock_persistent_query_keyword_is_valid,
        mock_persistent_query_keyword_api_get_by_id,
    ):
        """test_superuser_returns_http_200"""

        mock_persistent_query_keyword_data.return_value = {}
        mock_persistent_query_keyword_save.return_value = None
        mock_persistent_query_keyword_is_valid.return_value = True
        mock_persistent_query_keyword_api_get_by_id.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            persistent_query_keyword_views.PersistentQueryKeywordDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPersistentQueryKeywordDetailDelete(SimpleTestCase):
    """Test Persistent Query Keyword Detail Delete"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_delete(
            persistent_query_keyword_views.PersistentQueryKeywordDetail.as_view(),
            AnonymousUser(),
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(persistent_query_keyword_api, "get_by_id")
    @patch.object(persistent_query_keyword_api, "delete")
    def test_authenticated_returns_http_200(
        self, persistent_query_keyword_api_delete, persistent_query_keyword_get_by_id
    ):
        """test_authenticated_returns_http_200"""

        persistent_query_keyword_api_delete.return_value = None
        persistent_query_keyword_get_by_id.return_value = None
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            persistent_query_keyword_views.PersistentQueryKeywordDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(persistent_query_keyword_api, "get_by_id")
    @patch.object(persistent_query_keyword_api, "delete")
    def test_superuser_returns_http_200(
        self, persistent_query_keyword_api_delete, persistent_query_keyword_get_by_id
    ):
        """test_superuser_returns_http_200"""

        persistent_query_keyword_api_delete.return_value = None
        persistent_query_keyword_get_by_id.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_delete(
            persistent_query_keyword_views.PersistentQueryKeywordDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestPersistentQueryKeywordByNameGet(SimpleTestCase):
    """Test Persistent Query Keyword By Name Get"""

    @patch.object(persistent_query_keyword_api, "get_by_name")
    @patch.object(PersistentQueryKeywordSerializer, "data")
    def test_anonymous_returns_http_403(
        self,
        mock_persistent_query_keyword_serializer_data,
        mock_persistent_query_keyword_api_get_by_name,
    ):
        """test_anonymous_returns_http_403"""

        mock_persistent_query_keyword_serializer_data.return_value = {}
        mock_persistent_query_keyword_api_get_by_name.return_value = None
        response = RequestMock.do_request_get(
            persistent_query_keyword_views.PersistentQueryKeywordByName.as_view(),
            AnonymousUser(),
            param={"name": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(persistent_query_keyword_api, "get_by_name")
    @patch.object(PersistentQueryKeywordSerializer, "data")
    def test_authenticated_returns_http_200(
        self,
        mock_persistent_query_keyword_serializer_data,
        mock_persistent_query_keyword_api_get_by_name,
    ):
        """test_authenticated_returns_http_200"""

        mock_persistent_query_keyword_serializer_data.return_value = {}
        mock_persistent_query_keyword_api_get_by_name.return_value = None
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            persistent_query_keyword_views.PersistentQueryKeywordByName.as_view(),
            mock_user,
            param={"name": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(persistent_query_keyword_api, "get_by_name")
    @patch.object(PersistentQueryKeywordSerializer, "data")
    def test_superuser_returns_http_200(
        self,
        mock_persistent_query_keyword_serializer_data,
        mock_persistent_query_keyword_api_get_by_name,
    ):
        """test_superuser_returns_http_200"""

        mock_persistent_query_keyword_serializer_data.return_value = {}
        mock_persistent_query_keyword_api_get_by_name.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            persistent_query_keyword_views.PersistentQueryKeywordByName.as_view(),
            mock_user,
            param={"name": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
