""" Url router for the REST API
"""
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from core_explore_keyword_app.rest.persistent_query_keyword import (
    views as persistent_query_keyword_views,
)
from core_explore_keyword_app.rest.search_operators import (
    views as search_operator_views,
)

urlpatterns = [
    re_path(
        r"^search_operators/$",
        search_operator_views.SearchOperatorList.as_view(),
        name="core_explore_keyword_app_rest_search_operator_list",
    ),
    re_path(
        r"^search_operator/(?P<pk>\w+)/$",
        search_operator_views.SearchOperatorDetail.as_view(),
        name="core_explore_keyword_app_rest_search_operator",
    ),
    re_path(
        r"^admin/persistent_query_keyword/$",
        persistent_query_keyword_views.AdminPersistentQueryKeywordList.as_view(),
        name="core_explore_keyword_app_rest_persistent_query_keyword_admin_list",
    ),
    re_path(
        r"^persistent_query_keyword/$",
        persistent_query_keyword_views.PersistentQueryKeywordList.as_view(),
        name="core_explore_keyword_app_rest_persistent_query_keyword_list",
    ),
    re_path(
        r"^persistent_query_keyword/(?P<pk>\w+)/$",
        persistent_query_keyword_views.PersistentQueryKeywordDetail.as_view(),
        name="core_explore_keyword_app_rest_persistent_query_keyword_detail",
    ),
    re_path(
        r"^persistent_query_keyword/name/(?P<name>\w+)/$",
        persistent_query_keyword_views.PersistentQueryKeywordByName.as_view(),
        name="core_explore_keyword_app_rest_persistent_query_keyword_name",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
