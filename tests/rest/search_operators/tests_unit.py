""" Unit tests for search operators REST API.
"""
from collections import OrderedDict
from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError

from core_main_app.commons.exceptions import DoesNotExist, ModelError, NotUniqueError
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

from core_explore_keyword_app.components.search_operator import (
    api as search_operator_api,
)
from core_explore_keyword_app.components.search_operator.models import SearchOperator
from core_explore_keyword_app.rest.search_operators import (
    views as search_operator_views,
)
from core_explore_keyword_app.rest.search_operators.serializers import (
    SearchOperatorSerializer,
)


class TestSearchOperatorListGet(SimpleTestCase):
    """TestSearchOperatorListGet"""

    def setUp(self) -> None:
        self.mock_user = create_mock_user("1", is_staff=True)
        self.mock_search_operators = [
            SearchOperator(name="mock01", xpath_list=["x/path/a"]),
            SearchOperator(name="mock02", xpath_list=["x/path/b"]),
        ]

    @patch.object(search_operator_api, "get_all")
    def test_get_all_returns_200(self, mock_get_all):
        """test_get_all_returns_200"""

        mock_get_all.return_value = self.mock_search_operators
        response = RequestMock.do_request_get(
            search_operator_views.SearchOperatorList.as_view(), self.mock_user
        )

        self.assertTrue(response.status_code, status.HTTP_200_OK)

    @patch.object(search_operator_api, "get_all")
    def test_get_all_returns_search_operator_list(self, mock_get_all):
        """test_get_all_returns_search_operator_list"""

        mock_get_all.return_value = self.mock_search_operators
        response = RequestMock.do_request_get(
            search_operator_views.SearchOperatorList.as_view(), self.mock_user
        )

        self.assertEqual(
            response.data,
            [
                OrderedDict({"id": None, "name": "mock01", "xpath_list": ["x/path/a"]}),
                OrderedDict({"id": None, "name": "mock02", "xpath_list": ["x/path/b"]}),
            ],
        )

    @patch.object(search_operator_api, "get_all")
    def test_empty_list_returns_200(self, mock_get_all):
        """test_empty_list_returns_200"""

        mock_get_all.return_value = []
        response = RequestMock.do_request_get(
            search_operator_views.SearchOperatorList.as_view(), self.mock_user
        )

        self.assertTrue(response.status_code, status.HTTP_200_OK)

    @patch.object(search_operator_api, "get_all")
    @patch.object(SearchOperatorSerializer, "data")
    def test_exception_returns_500(self, mock_serializer_data, mock_get_all):
        """test_exception_returns_500"""

        mock_get_all.side_effect = Exception
        response = RequestMock.do_request_get(
            search_operator_views.SearchOperatorList.as_view(), self.mock_user
        )

        self.assertTrue(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestSearchOperatorListPost(SimpleTestCase):
    """Test Search Operator List Post"""

    def setUp(self) -> None:
        self.mock_user = create_mock_user("1", is_staff=True)

    @patch.object(SearchOperatorSerializer, "is_valid")
    @patch.object(SearchOperatorSerializer, "save")
    @patch.object(SearchOperatorSerializer, "data")
    def test_valid_search_operator_returns_201(
        self, mock_serializer_data, mock_serializer_save, mock_serializer_is_valid
    ):
        """test_valid_search_operator_returns_201"""

        mock_serializer_is_valid.return_value = True
        mock_serializer_save.return_value = None
        mock_serializer_data.return_value = None
        response = RequestMock.do_request_post(
            search_operator_views.SearchOperatorList.as_view(),
            self.mock_user,
            data={
                "name": "mockname",
                "xpath_list": ["/x/path/one", "/x/path/two"],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(SearchOperatorSerializer, "is_valid")
    def test_invalid_search_operator_returns_400(self, mock_serializer_is_valid):
        """test_invalid_search_operator_returns_400"""

        mock_serializer_is_valid.side_effect = ValidationError

        response = RequestMock.do_request_post(
            search_operator_views.SearchOperatorList.as_view(),
            self.mock_user,
            data={
                "name": "mock_name",
                "xpath_list": ["/x/path.one*1..1", "/x/path/two"],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(SearchOperatorSerializer, "is_valid")
    @patch.object(SearchOperatorSerializer, "save")
    def test_model_error_returns_400(
        self, mock_serializer_save, mock_serializer_is_valid
    ):
        """test_model_error_returns_400"""

        mock_serializer_is_valid.return_value = True
        mock_serializer_save.side_effect = ModelError(message="mock error")

        response = RequestMock.do_request_post(
            search_operator_views.SearchOperatorList.as_view(),
            self.mock_user,
            data={
                "name": "mock_name",
                "xpath_list": ["/x/path.one*1..1", "/x/path/two"],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(SearchOperatorSerializer, "is_valid")
    @patch.object(SearchOperatorSerializer, "save")
    def test_duplicate_returns_400(
        self, mock_serializer_save, mock_serializer_is_valid
    ):
        """test_duplicate_returns_400"""

        mock_serializer_is_valid.return_value = True
        mock_serializer_save.side_effect = NotUniqueError(message="mock error")
        response = RequestMock.do_request_post(
            search_operator_views.SearchOperatorList.as_view(),
            self.mock_user,
            data={
                "name": "mock_name",
                "xpath_list": ["/x/path.one*1..1", "/x/path/two"],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(SearchOperatorSerializer, "__init__")
    def test_key_error_returns_400(self, mock_serializer):
        """test_key_error_returns_400"""

        mock_serializer.side_effect = KeyError
        response = RequestMock.do_request_post(
            search_operator_views.SearchOperatorList.as_view(),
            self.mock_user,
            data={
                "name": "mock_name",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(SearchOperatorSerializer, "__init__")
    def test_exception_returns_500(self, mock_serializer):
        """test_exception_returns_500"""

        mock_serializer.side_effect = Exception
        response = RequestMock.do_request_post(
            search_operator_views.SearchOperatorList.as_view(),
            self.mock_user,
            data={
                "name": "mock_name",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestSearchOperatorDetailGet(SimpleTestCase):
    """Test Search Operator Detail Get"""

    def setUp(self) -> None:
        self.mock_user = create_mock_user("1", is_staff=True)

    @patch.object(search_operator_api, "get_by_id")
    def test_default_returns_200(self, mock_get_by_id):
        """test_default_returns_200"""

        mock_get_by_id.return_value = {
            "name": "mock_operator",
            "xpath_list": ["/x/path/a", "/x/path/b"],
        }
        response = RequestMock.do_request_get(
            search_operator_views.SearchOperatorDetail.as_view(),
            self.mock_user,
            param={"pk": 1},
        )

        self.assertTrue(response.status_code, status.HTTP_200_OK)

    @patch.object(search_operator_api, "get_by_id")
    def test_default_returns_search_operator_data(self, mock_get_by_id):
        """test_default_returns_search_operator_data"""

        search_operator = {
            "name": "mock_operator",
            "xpath_list": ["/x/path/a", "/x/path/b"],
        }
        mock_get_by_id.return_value = search_operator
        response = RequestMock.do_request_get(
            search_operator_views.SearchOperatorDetail.as_view(),
            self.mock_user,
            param={"pk": 1},
        )

        self.assertEqual(response.data, search_operator)

    @patch.object(search_operator_api, "get_by_id")
    def test_nonexistent_returns_404(self, mock_get_by_id):
        """test_nonexistent_returns_404"""

        mock_get_by_id.side_effect = DoesNotExist(message="mock error")
        response = RequestMock.do_request_get(
            search_operator_views.SearchOperatorDetail.as_view(),
            self.mock_user,
            param={"pk": 1},
        )

        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(search_operator_api, "get_by_id")
    def test_exception_returns_500(self, mock_get_by_id):
        """test_exception_returns_500"""

        mock_get_by_id.side_effect = Exception
        response = RequestMock.do_request_get(
            search_operator_views.SearchOperatorDetail.as_view(),
            self.mock_user,
            param={"pk": 1},
        )

        self.assertTrue(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestSearchOperatorDetailPatch(SimpleTestCase):
    """Test Search Operator Detail Patch"""

    def setUp(self) -> None:
        self.mock_user = create_mock_user("1", is_staff=True)

    @patch.object(search_operator_api, "get_by_id")
    def test_valid_operator_returns_200(self, mock_get_by_id):
        """test_valid_operator_returns_200"""

        mock_get_by_id.return_value = {
            "name": "mock_operator",
            "xpath_list": ["/x/path/a", "/x/path/b"],
        }
        response = RequestMock.do_request_patch(
            search_operator_views.SearchOperatorDetail.as_view(),
            self.mock_user,
            param={"pk": 1},
        )

        self.assertTrue(response.status_code, status.HTTP_200_OK)

    @patch.object(search_operator_api, "get_by_id")
    def test_valid_operator_returns_operator(self, mock_get_by_id):
        """test_valid_operator_returns_operator"""

        mock_operator = {
            "name": "mock_operator",
            "xpath_list": ["/x/path/a", "/x/path/b"],
        }
        mock_get_by_id.return_value = mock_operator
        response = RequestMock.do_request_patch(
            search_operator_views.SearchOperatorDetail.as_view(),
            self.mock_user,
            param={"pk": 1},
        )

        self.assertTrue(response.data, mock_operator)

    @patch.object(SearchOperatorSerializer, "is_valid")
    def test_invalid_operator_returns_400(self, mock_serializer_is_valid):
        """test_invalid_operator_returns_400"""

        mock_serializer_is_valid.side_effect = ValidationError
        response = RequestMock.do_request_patch(
            search_operator_views.SearchOperatorDetail.as_view(),
            self.mock_user,
            param={"pk": 1},
        )

        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(search_operator_api, "get_by_id")
    def test_nonexistent_operator_returns_404(self, mock_get_by_id):
        """test_nonexistent_operator_returns_404"""

        mock_get_by_id.side_effect = DoesNotExist
        response = RequestMock.do_request_patch(
            search_operator_views.SearchOperatorDetail.as_view(),
            self.mock_user,
            param={"pk": 1},
        )

        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(SearchOperatorSerializer, "save")
    def test_exception_returns_500(self, mock_serializer_save):
        """test_exception_returns_500"""

        mock_serializer_save.side_effect = Exception
        response = RequestMock.do_request_patch(
            search_operator_views.SearchOperatorDetail.as_view(),
            self.mock_user,
            param={"pk": 1},
        )

        self.assertTrue(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestSearchOperatorDetailDelete(SimpleTestCase):
    """Test Search Operator Detail Delete"""

    def setUp(self) -> None:
        self.mock_user = create_mock_user("1", is_staff=True)

    @patch.object(search_operator_api, "get_by_id")
    @patch.object(search_operator_api, "delete")
    def test_valid_returns_204(self, mock_delete, mock_get_by_id):
        """test_valid_returns_204"""

        mock_delete.return_value = None
        mock_get_by_id.return_value = {}
        response = RequestMock.do_request_delete(
            search_operator_views.SearchOperatorDetail.as_view(),
            self.mock_user,
            param={"pk": 1},
        )

        self.assertTrue(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(search_operator_api, "get_by_id")
    def test_nonexistent_returns_404(self, mock_get_by_id):
        """test_nonexistent_returns_404"""

        mock_get_by_id.side_effect = DoesNotExist
        response = RequestMock.do_request_delete(
            search_operator_views.SearchOperatorDetail.as_view(),
            self.mock_user,
            param={"pk": 1},
        )

        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(search_operator_api, "get_by_id")
    @patch.object(search_operator_api, "delete")
    def test_exception_returns_500(self, mock_delete, mock_get_by_id):
        """test_exception_returns_500"""

        mock_get_by_id.return_value = {}
        mock_delete.side_effect = Exception
        response = RequestMock.do_request_delete(
            search_operator_views.SearchOperatorDetail.as_view(),
            self.mock_user,
            param={"pk": 1},
        )

        self.assertTrue(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
