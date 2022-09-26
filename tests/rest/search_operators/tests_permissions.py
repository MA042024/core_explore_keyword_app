""" Authentication tests for search operators REST API.
"""
from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
import core_explore_keyword_app.components.search_operator.api as search_operator_api
from core_explore_keyword_app.rest.search_operators import (
    views as search_operator_rest_views,
)
from core_explore_keyword_app.rest.search_operators.serializers import (
    SearchOperatorSerializer,
)


class TestSearchOperatorListGet(SimpleTestCase):
    """Test Search Operator List Get"""

    @patch.object(search_operator_api, "get_all")
    def test_anonymous_returns_http_200(
        self, mock_search_operator_api_get_all
    ):
        """test_anonymous_returns_http_200"""

        mock_search_operator_api_get_all.return_value = []
        response = RequestMock.do_request_get(
            search_operator_rest_views.SearchOperatorList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(search_operator_api, "get_all")
    def test_authenticated_returns_http_200(
        self, mock_search_operator_api_get_all
    ):
        """test_authenticated_returns_http_200"""

        mock_user = create_mock_user("1")
        mock_search_operator_api_get_all.return_value = []

        response = RequestMock.do_request_get(
            search_operator_rest_views.SearchOperatorList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(search_operator_api, "get_all")
    @patch.object(SearchOperatorSerializer, "data")
    def test_staff_returns_http_200(
        self,
        mock_search_operator_serializer_data,
        mock_search_operator_api_get_all,
    ):
        """test_staff_returns_http_200"""

        mock_search_operator_serializer_data.return_value = {}
        mock_search_operator_api_get_all.return_value = []
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            search_operator_rest_views.SearchOperatorList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSearchOperatorListPost(SimpleTestCase):
    """Test Search Operator List Post"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_post(
            search_operator_rest_views.SearchOperatorList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            search_operator_rest_views.SearchOperatorList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(SearchOperatorSerializer, "is_valid")
    @patch.object(SearchOperatorSerializer, "save")
    @patch.object(SearchOperatorSerializer, "data")
    def test_staff_returns_http_201(
        self,
        mock_search_operator_serializer_data,
        mock_search_operator_serializer_save,
        mock_search_operator_serializer_is_valid,
    ):
        """test_staff_returns_http_201"""

        mock_search_operator_serializer_data.return_value = {}
        mock_search_operator_serializer_save.return_value = None
        mock_search_operator_serializer_is_valid.return_value = True
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            search_operator_rest_views.SearchOperatorList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestSearchOperatorDetailGet(SimpleTestCase):
    """Test Search Operator Detail Get"""

    @patch.object(search_operator_api, "get_by_id")
    @patch.object(SearchOperatorSerializer, "data")
    def test_anonymous_returns_http_200(
        self,
        mock_search_operator_serializer_data,
        mock_search_operator_api_get_by_id,
    ):
        """test_anonymous_returns_http_200"""

        mock_search_operator_serializer_data.return_value = {}
        mock_search_operator_api_get_by_id.return_value = None
        response = RequestMock.do_request_get(
            search_operator_rest_views.SearchOperatorDetail.as_view(),
            None,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(search_operator_api, "get_by_id")
    @patch.object(SearchOperatorSerializer, "data")
    def test_authenticated_returns_http_200(
        self,
        mock_search_operator_serializer_data,
        mock_search_operator_api_get_by_id,
    ):
        """test_authenticated_returns_http_200"""

        mock_search_operator_serializer_data.return_value = {}
        mock_search_operator_api_get_by_id.return_value = None
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            search_operator_rest_views.SearchOperatorDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(search_operator_api, "get_by_id")
    @patch.object(SearchOperatorSerializer, "data")
    def test_staff_returns_http_200(
        self,
        mock_search_operator_serializer_data,
        mock_search_operator_api_get_by_id,
    ):
        """test_staff_returns_http_200"""

        mock_search_operator_serializer_data.return_value = {}
        mock_search_operator_api_get_by_id.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            search_operator_rest_views.SearchOperatorDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSearchOperatorDetailPatch(SimpleTestCase):
    """Test Search Operator Detail Patch"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""
        response = RequestMock.do_request_patch(
            search_operator_rest_views.SearchOperatorDetail.as_view(),
            None,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            search_operator_rest_views.SearchOperatorDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(search_operator_api, "get_by_id")
    @patch.object(SearchOperatorSerializer, "is_valid")
    @patch.object(SearchOperatorSerializer, "save")
    @patch.object(SearchOperatorSerializer, "data")
    def test_staff_returns_http_200(
        self,
        mock_search_operator_serializer_data,
        mock_search_operator_serializer_save,
        mock_search_operator_serializer_is_valid,
        mock_search_operator_api_get_by_id,
    ):
        """test_staff_returns_http_200"""

        mock_search_operator_serializer_data.return_value = {}
        mock_search_operator_serializer_save.return_value = None
        mock_search_operator_serializer_is_valid.return_value = True
        mock_search_operator_api_get_by_id.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            search_operator_rest_views.SearchOperatorDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSearchOperatorDetailDelete(SimpleTestCase):
    """Test Search Operator Detail Delete"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""
        response = RequestMock.do_request_delete(
            search_operator_rest_views.SearchOperatorDetail.as_view(),
            None,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            search_operator_rest_views.SearchOperatorDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(search_operator_api, "get_by_id")
    @patch.object(search_operator_api, "delete")
    def test_staff_returns_http_200(
        self,
        mock_search_operator_api_delete,
        mock_search_operator_api_get_by_id,
    ):
        """test_staff_returns_http_200"""

        mock_search_operator_api_delete.return_value = None
        mock_search_operator_api_get_by_id.return_value = None
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_delete(
            search_operator_rest_views.SearchOperatorDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
