""" Test units
"""

from unittest import TestCase
from unittest.mock import patch, Mock

from core_main_app.commons.exceptions import ApiError
from core_explore_keyword_app.components.search_operator import (
    api as search_operator_api,
)
from core_explore_keyword_app.components.search_operator.models import SearchOperator
from core_explore_keyword_app.utils.search_operators import (
    build_search_operator_query,
    get_keywords_from_search_operator_query,
)


class TestBuildSearchOperatorQuery(TestCase):
    """Test Build Search Operator Query"""

    @patch.object(search_operator_api, "get_by_name")
    def test_single_dot_notation_returns_valid_query(self, mock_get_by_name):
        """test_single_dot_notation_returns_valid_query"""

        mock_dot_notation = "mock.dot.notation"
        mock_value = "mock_value"
        mock_search_operator = Mock(spec=SearchOperator)
        mock_search_operator.dot_notation_list = [mock_dot_notation]
        mock_get_by_name.return_value = mock_search_operator

        expected_dict = {
            "$or": [
                {mock_dot_notation: mock_value},
                {"%s.#text" % mock_dot_notation: mock_value},
            ]
        }

        returned_dict = build_search_operator_query("mock_name", mock_value)

        self.assertDictEqual(returned_dict, expected_dict)

    @patch.object(search_operator_api, "get_by_name")
    def test_multi_dot_notation_returns_valid_query(self, mock_get_by_name):
        """test_multi_dot_notation_returns_valid_query"""

        mock_dot_notation_list = ["mock.dot.notation.1", "mock.dot.notation.2"]
        mock_value = "mock_value"
        mock_search_operator = Mock(spec=SearchOperator)
        mock_search_operator.dot_notation_list = mock_dot_notation_list
        mock_get_by_name.return_value = mock_search_operator

        mock_dot_notation_values = [
            {mock_dot_notation: mock_value}
            for mock_dot_notation in mock_dot_notation_list
        ]
        mock_dot_notation_values += [
            {"%s.#text" % mock_dot_notation: mock_value}
            for mock_dot_notation in mock_dot_notation_list
        ]

        expected_dict = {"$or": mock_dot_notation_values}

        returned_dict = build_search_operator_query("mock_name", mock_value)

        self.assertDictEqual(returned_dict, expected_dict)


class TestGetKeywordsFromSearchOperatorQuery(TestCase):
    """Test Get Keywords From Search Operator Query"""

    def test_query_without_or_returns_none(self):
        """test_query_without_or_returns_none"""

        self.assertEqual(get_keywords_from_search_operator_query({}), None)

    @patch.object(search_operator_api, "get_by_dot_notation_list")
    def test_returns_valid_keyword(self, mock_get_by_dot_notation_list):
        """test_returns_valid_keyword"""

        mock_keyword = "mock_keyword"
        mock_search_operator = Mock(spec=SearchOperator)
        mock_search_operator.name = mock_keyword
        mock_get_by_dot_notation_list.return_value = mock_search_operator
        mock_value = "mock_value"
        mock_query = {
            "$or": [
                {"mock.dot.notation.1": mock_value},
                {"mock.dot.notation.1.#text": mock_value},
                {"mock.dot.notation.2": mock_value},
                {"mock.dot.notation.2.#text": mock_value},
            ]
        }

        expected_string = "%s:%s" % (mock_keyword, mock_value)
        returned_string = get_keywords_from_search_operator_query(mock_query)

        self.assertEqual(returned_string, expected_string)

    @patch.object(search_operator_api, "get_by_dot_notation_list")
    def test_api_error_returns_none(self, mock_get_by_dot_notation_list):
        """test_api_error_returns_none"""

        mock_get_by_dot_notation_list.side_effect = ApiError("mock_error")
        mock_value = "mock_value"
        mock_query = {
            "$or": [
                {"mock.dot.notation.1": mock_value},
                {"mock.dot.notation.1.#text": mock_value},
                {"mock.dot.notation.2": mock_value},
                {"mock.dot.notation.2.#text": mock_value},
            ]
        }

        self.assertIsNone(get_keywords_from_search_operator_query(mock_query))
