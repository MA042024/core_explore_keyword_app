""" Url router for the explore keyword application
"""
from django.urls import re_path, include

from core_explore_keyword_app.views.user import (
    views as user_views,
    ajax as user_ajax,
)
from core_explore_keyword_app.views.admin import ajax as admin_ajax

urlpatterns = [
    re_path(
        r"^$",
        user_views.KeywordSearchView.as_view(),
        name="core_explore_keyword_app_search",
    ),
    re_path(
        r"^suggestions$",
        user_ajax.SuggestionsKeywordSearchView.as_view(),
        name="core_explore_keyword_suggestions",
    ),
    re_path(
        r"^get-persistent-query-url$",
        user_ajax.CreatePersistentQueryUrlKeywordView.as_view(),
        name="core_explore_keyword_get_persistent_query_url",
    ),
    re_path(
        r"^results-redirect",
        user_views.ResultQueryRedirectKeywordView.as_view(),
        name="core_explore_keyword_results_redirect",
    ),
    re_path(
        r"^(?P<query_id>\w+)$",
        user_views.KeywordSearchView.as_view(),
        name="core_explore_keyword_app_search",
    ),
    re_path(
        r"^operators/delete$",
        admin_ajax.SearchOperatorDeleteModalView.as_view(),
        name="core_explore_keyword_app_search_operator_delete",
    ),
    re_path(
        r"^operators/edit$",
        admin_ajax.SearchOperatorConfigModalView.as_view(),
        name="core_explore_keyword_app_search_operator_edit",
    ),
    re_path(r"^rest/", include("core_explore_keyword_app.rest.urls")),
]
