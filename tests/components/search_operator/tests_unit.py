""" Unit tests for SearchOperator API calls.
"""
from unittest import TestCase, mock

from core_main_app.commons import exceptions
from core_explore_keyword_app.components.search_operator import (
    api as search_operator_api,
)
from core_explore_keyword_app.components.search_operator.models import (
    SearchOperator,
)


class TestsApiGetAll(TestCase):
    """Tests Api Get All"""

    @mock.patch.object(SearchOperator, "get_all")
    def test_returns_no_error(self, mock_get_all):
        """test_returns_no_error"""

        expected_result = ["search_operator_1", "search_operator_2"]
        mock_get_all.return_value = expected_result

        self.assertListEqual(search_operator_api.get_all(), expected_result)


class TestsApiGetById(TestCase):
    """Tests Api Get By Id"""

    @mock.patch.object(SearchOperator, "get_by_id")
    def test_returns_no_error(self, mock_get_by_id):
        """test_returns_no_error"""

        expected_result = "search_operator"
        mock_get_by_id.return_value = expected_result

        self.assertEqual(
            search_operator_api.get_by_id("mock_id"), expected_result
        )

    @mock.patch.object(SearchOperator, "get_by_id")
    def test_incorrect_id_raises_api_error(self, mock_get_by_id):
        """test_incorrect_id_raises_api_error"""

        mock_get_by_id.side_effect = exceptions.ModelError(
            message="mock error"
        )

        with self.assertRaises(exceptions.ApiError):
            search_operator_api.get_by_id("mock_id")

    @mock.patch.object(SearchOperator, "get_by_id")
    def test_nonexistant_raises_api_error(self, mock_get_by_id):
        """test_nonexistant_raises_api_error"""

        mock_get_by_id.side_effect = exceptions.DoesNotExist(
            message="mock error"
        )

        with self.assertRaises(exceptions.ApiError):
            search_operator_api.get_by_id("mock_id")


class TestsApiGetByName(TestCase):
    """Tests Api Get By Name"""

    @mock.patch.object(SearchOperator, "get_by_name")
    def test_returns_no_error(self, mock_get_by_name):
        """test_returns_no_error"""

        expected_result = "search_operator"
        mock_get_by_name.return_value = expected_result

        self.assertEqual(
            search_operator_api.get_by_name("mock_name"), expected_result
        )

    @mock.patch.object(SearchOperator, "get_by_name")
    def test_nonexistant_raises_api_error(self, mock_get_by_name):
        """test_nonexistant_raises_api_error"""

        mock_get_by_name.side_effect = exceptions.DoesNotExist(
            message="mock error"
        )

        with self.assertRaises(exceptions.ApiError):
            search_operator_api.get_by_name("mock_name")


class TestsApiGetByDotNotationList(TestCase):
    """Tests Api Get By Dot Notation List"""

    @mock.patch.object(SearchOperator, "get_by_dot_notation_list")
    def test_returns_no_error(self, mock_get_by_dot_notation_list):
        """test_returns_no_error"""

        expected_result = "search_operator"
        mock_get_by_dot_notation_list.return_value = expected_result

        self.assertEqual(
            search_operator_api.get_by_dot_notation_list(
                ["dot_not_1", "dot_not_2"]
            ),
            expected_result,
        )

    @mock.patch.object(SearchOperator, "get_by_dot_notation_list")
    def test_nonexistant_raises_api_error(self, mock_get_by_dot_notation_list):
        """test_nonexistant_raises_api_error"""

        mock_get_by_dot_notation_list.side_effect = exceptions.DoesNotExist(
            message="mock error"
        )

        with self.assertRaises(exceptions.ApiError):
            search_operator_api.get_by_dot_notation_list(
                ["dot_not_1", "dot_not_2"]
            )


class TestsApiUpsert(TestCase):
    """Tests Api Upsert"""

    def setUp(self) -> None:
        self.mock_search_operator = SearchOperator(
            name="mock_operator", xpath_list=["/x/path/a", "/x/path/b"]
        )

    @mock.patch.object(SearchOperator, "save")
    def test_returns_no_error(self, mock_save):
        """test_returns_no_error"""

        mock_save.return_value = None

        search_operator_api.upsert(self.mock_search_operator)

    @mock.patch.object(SearchOperator, "save")
    def test_dot_notation_list_is_correct(self, mock_save):
        """test_dot_notation_list_is_correct"""

        expected_dot_notation_list = ["x.path.a", "x.path.b"]
        mock_save.return_value = self.mock_search_operator

        self.assertListEqual(
            search_operator_api.upsert(
                self.mock_search_operator
            ).dot_notation_list,
            expected_dot_notation_list,
        )

    @mock.patch.object(SearchOperator, "save")
    def test_duplicate_raises_api_error(self, mock_save):
        """test_duplicate_raises_api_error"""

        mock_save.side_effect = exceptions.NotUniqueError(message="mock error")

        with self.assertRaises(exceptions.ApiError):
            search_operator_api.upsert(self.mock_search_operator)


class TestsApiDelete(TestCase):
    """Tests Api Delete"""

    @mock.patch.object(SearchOperator, "delete")
    def test_returns_no_error(self, mock_delete):
        """test_returns_no_error"""

        mock_delete.return_value = None

        self.assertEqual(search_operator_api.delete(SearchOperator()), None)
