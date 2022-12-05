""" Unit tests for user-side AJAX calls
"""
import json
from unittest import TestCase
from unittest.mock import MagicMock, patch

from django.test import RequestFactory
from rest_framework import status

from core_explore_keyword_app.views.user.ajax import (
    SuggestionsKeywordSearchView,
)
from core_main_app.commons.exceptions import QueryError, DoesNotExist
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestSuggestionsKeywordSearchViewPost(TestCase):
    """Test SuggestionsKeywordSearchView post method"""

    @classmethod
    def setUpClass(cls) -> None:
        """setUpClass"""
        cls.data = {
            "keywords": "mock_keyword",
            "query_id": 1,
            "user_id": 1,
            "term": "mock_term",
        }

        cls.user = create_mock_user(user_id=1)
        cls.view = "core_explore_keyword_suggestions"

        cls.factory = RequestFactory()

    def setUp(self) -> None:
        """setUp"""
        self.user.has_perm = MagicMock()
        self.user.has_perm.return_value = True

    def _send_post_request(self):
        """_send_post_request"""
        request = self.factory.post(self.view, data=self.data)
        request.user = self.user

        return SuggestionsKeywordSearchView().post(request)

    @patch("core_explore_keyword_app.views.user.ajax.KeywordForm.is_valid")
    def test_invalid_form_returns_400(self, mock_keyword_form_is_valid):
        """test_invalid_form_returns_400"""
        mock_keyword_form_is_valid.return_value = False

        response = self._send_post_request()

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("core_explore_keyword_app.views.user.ajax.sanitize_value")
    @patch("core_explore_keyword_app.views.user.ajax.KeywordForm")
    def test_invalid_term_returns_400(
        self, mock_keyword_form, mock_sanitize_value
    ):
        """test_invalid_term_returns_400"""
        mock_keyword_form.return_value = MagicMock()
        mock_sanitize_value.side_effect = QueryError("mock_error")

        response = self._send_post_request()

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(
        "core_explore_keyword_app.views.user.ajax.template_version_manager_api.get_by_id_list"
    )
    @patch("core_explore_keyword_app.views.user.ajax.sanitize_value")
    @patch("core_explore_keyword_app.views.user.ajax.KeywordForm")
    def test_template_not_found_returns_400(
        self, mock_keyword_form, mock_sanitize_value, mock_template_get_by_id
    ):
        """test_template_not_found_returns_400"""
        mock_keyword_form.return_value = MagicMock()
        mock_sanitize_value.return_value = None
        mock_template_get_by_id.side_effect = DoesNotExist(
            "mock_does_not_exist_error"
        )

        response = self._send_post_request()

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("core_explore_keyword_app.views.user.ajax.query_api.get_by_id")
    @patch(
        "core_explore_keyword_app.views.user.ajax.template_version_manager_api.get_by_id_list"
    )
    @patch("core_explore_keyword_app.views.user.ajax.sanitize_value")
    @patch("core_explore_keyword_app.views.user.ajax.KeywordForm")
    def test_query_not_found_returns_400(
        self,
        mock_keyword_form,
        mock_sanitize_value,
        mock_template_get_by_id,
        mock_query_get_by_id,
    ):
        """test_query_not_found_returns_400"""
        mock_keyword_form.return_value = MagicMock()
        mock_sanitize_value.return_value = None
        mock_template_get_by_id.return_value = []
        mock_query_get_by_id.side_effect = DoesNotExist(
            "mock_does_not_exist_error"
        )

        response = self._send_post_request()

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("core_explore_keyword_app.views.user.ajax.check_data_source")
    @patch("core_explore_keyword_app.views.user.ajax.query_api.get_by_id")
    @patch(
        "core_explore_keyword_app.views.user.ajax.template_version_manager_api.get_by_id_list"
    )
    @patch("core_explore_keyword_app.views.user.ajax.sanitize_value")
    @patch("core_explore_keyword_app.views.user.ajax.KeywordForm")
    def test_check_data_source_fails_returns_400(
        self,
        mock_keyword_form,
        mock_sanitize_value,
        mock_template_get_by_id,
        mock_query_get_by_id,
        mock_check_data_source,
    ):
        """test_check_data_source_fails_returns_400"""
        mock_keyword_form.return_value = MagicMock()
        mock_sanitize_value.return_value = None
        mock_template_get_by_id.return_value = []
        mock_query_get_by_id.return_value = MagicMock()
        mock_check_data_source.side_effect = Exception(
            "mock_check_data_source_exception"
        )

        response = self._send_post_request()

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(
        "core_explore_keyword_app.views.user.ajax.SuggestionsKeywordSearchView._get_query_prepared"
    )
    @patch("core_explore_keyword_app.views.user.ajax.check_data_source")
    @patch("core_explore_keyword_app.views.user.ajax.query_api.get_by_id")
    @patch(
        "core_explore_keyword_app.views.user.ajax.template_version_manager_api.get_by_id_list"
    )
    @patch("core_explore_keyword_app.views.user.ajax.sanitize_value")
    @patch("core_explore_keyword_app.views.user.ajax.KeywordForm")
    def test_get_query_prepared_fails_returns_400(
        self,
        mock_keyword_form,
        mock_sanitize_value,
        mock_template_get_by_id,
        mock_query_get_by_id,
        mock_check_data_source,
        mock_get_query_prepared,
    ):
        """test_get_query_prepared_fails_returns_400"""
        mock_keyword_form.return_value = MagicMock()
        mock_sanitize_value.return_value = None
        mock_template_get_by_id.return_value = []
        mock_query_get_by_id.return_value = MagicMock()
        mock_check_data_source.return_value = True
        mock_get_query_prepared.side_effect = Exception(
            "mock_get_query_prepared_exception"
        )

        response = self._send_post_request()

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("core_explore_keyword_app.views.user.ajax.send")
    @patch(
        "core_explore_keyword_app.views.user.ajax.SuggestionsKeywordSearchView._get_query_prepared"
    )
    @patch("core_explore_keyword_app.views.user.ajax.check_data_source")
    @patch("core_explore_keyword_app.views.user.ajax.query_api.get_by_id")
    @patch(
        "core_explore_keyword_app.views.user.ajax.template_version_manager_api.get_by_id_list"
    )
    @patch("core_explore_keyword_app.views.user.ajax.sanitize_value")
    @patch("core_explore_keyword_app.views.user.ajax.KeywordForm")
    def test_send_query_fails_returns_400(
        self,
        mock_keyword_form,
        mock_sanitize_value,
        mock_template_get_by_id,
        mock_query_get_by_id,
        mock_check_data_source,
        mock_get_query_prepared,
        mock_send_query,
    ):
        """test_send_query_fails_returns_400"""
        mock_keyword_form.return_value = MagicMock()
        mock_sanitize_value.return_value = None
        mock_template_get_by_id.return_value = []
        mock_query_get_by_id.return_value = MagicMock()
        mock_check_data_source.return_value = True
        mock_get_query_prepared.return_value = MagicMock()
        mock_send_query.side_effect = Exception("mock_send_query_exception")

        response = self._send_post_request()

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(
        "core_explore_keyword_app.views.user.ajax.SuggestionsKeywordSearchView._extract_suggestion_from_results"
    )
    @patch("core_explore_keyword_app.views.user.ajax.send")
    @patch(
        "core_explore_keyword_app.views.user.ajax.SuggestionsKeywordSearchView._get_query_prepared"
    )
    @patch("core_explore_keyword_app.views.user.ajax.check_data_source")
    @patch("core_explore_keyword_app.views.user.ajax.query_api.get_by_id")
    @patch(
        "core_explore_keyword_app.views.user.ajax.template_version_manager_api.get_by_id_list"
    )
    @patch("core_explore_keyword_app.views.user.ajax.sanitize_value")
    @patch("core_explore_keyword_app.views.user.ajax.KeywordForm")
    def test_extract_suggestions_fails_returns_400(
        self,
        mock_keyword_form,
        mock_sanitize_value,
        mock_template_get_by_id,
        mock_query_get_by_id,
        mock_check_data_source,
        mock_get_query_prepared,
        mock_send_query,
        mock_extract_suggestion_from_results,
    ):
        """test_extract_suggestions_fails_returns_400"""
        mock_keyword_form.return_value = MagicMock()
        mock_sanitize_value.return_value = None
        mock_template_get_by_id.return_value = []
        mock_query_get_by_id.return_value = MagicMock()
        mock_check_data_source.return_value = True
        mock_get_query_prepared.return_value = MagicMock()
        mock_send_query.return_value = {"count": 1}
        mock_extract_suggestion_from_results.side_effect = Exception(
            "mock_extract_suggestion_from_results_exception"
        )

        response = self._send_post_request()

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(
        "core_explore_keyword_app.views.user.ajax.SuggestionsKeywordSearchView._extract_suggestion_from_results"
    )
    @patch("core_explore_keyword_app.views.user.ajax.send")
    @patch(
        "core_explore_keyword_app.views.user.ajax.SuggestionsKeywordSearchView._get_query_prepared"
    )
    @patch("core_explore_keyword_app.views.user.ajax.check_data_source")
    @patch("core_explore_keyword_app.views.user.ajax.query_api.get_by_id")
    @patch(
        "core_explore_keyword_app.views.user.ajax.template_version_manager_api.get_by_id_list"
    )
    @patch("core_explore_keyword_app.views.user.ajax.sanitize_value")
    @patch("core_explore_keyword_app.views.user.ajax.KeywordForm")
    def test_empty_dict_results_returns_200(
        self,
        mock_keyword_form,
        mock_sanitize_value,
        mock_template_get_by_id,
        mock_query_get_by_id,
        mock_check_data_source,
        mock_get_query_prepared,
        mock_send_query,
        mock_extract_suggestion_from_results,
    ):
        """test_empty_dict_results_returns_200"""
        mock_keyword_form.return_value = MagicMock()
        mock_sanitize_value.return_value = None
        mock_template_get_by_id.return_value = []
        mock_query_get_by_id.return_value = MagicMock()
        mock_check_data_source.return_value = True
        mock_get_query_prepared.return_value = MagicMock()
        mock_send_query.return_value = {"count": 0}
        mock_extract_suggestion_from_results.return_value = None

        response = self._send_post_request()

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    @patch(
        "core_explore_keyword_app.views.user.ajax.SuggestionsKeywordSearchView._extract_suggestion_from_results"
    )
    @patch("core_explore_keyword_app.views.user.ajax.send")
    @patch(
        "core_explore_keyword_app.views.user.ajax.SuggestionsKeywordSearchView._get_query_prepared"
    )
    @patch("core_explore_keyword_app.views.user.ajax.check_data_source")
    @patch("core_explore_keyword_app.views.user.ajax.query_api.get_by_id")
    @patch(
        "core_explore_keyword_app.views.user.ajax.template_version_manager_api.get_by_id_list"
    )
    @patch("core_explore_keyword_app.views.user.ajax.sanitize_value")
    @patch("core_explore_keyword_app.views.user.ajax.KeywordForm")
    def test_dict_results_returns_suggestions(
        self,
        mock_keyword_form,
        mock_sanitize_value,
        mock_template_get_by_id,
        mock_query_get_by_id,
        mock_check_data_source,
        mock_get_query_prepared,
        mock_send_query,
        mock_extract_suggestion_from_results,
    ):
        """test_dict_results_returns_suggestions"""
        mock_keyword_form.return_value = MagicMock()
        mock_sanitize_value.return_value = None
        mock_template_get_by_id.return_value = []
        mock_query_get_by_id.return_value = MagicMock()
        mock_check_data_source.return_value = True
        mock_get_query_prepared.return_value = MagicMock()
        mock_send_query.return_value = {"count": 0}
        mock_extract_suggestion_from_results.return_value = None

        response = self._send_post_request()

        self.assertEquals(json.loads(response.content), {"suggestions": []})
