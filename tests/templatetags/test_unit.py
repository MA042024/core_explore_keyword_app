""" Test units
"""

from unittest import TestCase
from unittest.mock import patch

from core_explore_keyword_app.templatetags.core_explore_keyword_app_search_bar import (
    show_search_bar,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request


class TestSearchBar(TestCase):
    """TestSearchBar"""

    @patch("core_explore_common_app.components.query.api.upsert")
    @patch(
        "core_explore_common_app.components.query.api.set_visibility_to_query"
    )
    @patch(
        "core_explore_common_app.components.query.api.add_local_data_source"
    )
    def test_search_bar(
        self,
        mock_add_local_data_source,
        mock_set_visibility_to_query,
        mock_upsert,
    ):
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        mock_context = {"request": mock_request}
        mock_add_local_data_source.return_value = None
        mock_set_visibility_to_query.return_value = None
        mock_upsert.return_value = None

        response = show_search_bar(context=mock_context)

        self.assertTrue("search_form" in response["data"])
        self.assertTrue(mock_add_local_data_source.called)
        self.assertTrue(mock_set_visibility_to_query.called)
        self.assertTrue(mock_upsert.called)
