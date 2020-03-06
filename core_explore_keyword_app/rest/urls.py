""" Url router for the REST API
"""
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from core_explore_keyword_app.rest.search_operators import views as \
    search_operator_views

urlpatterns = [
    re_path(r"^search_operators/$", search_operator_views.SearchOperatorList.as_view(),
            name="core_explore_keyword_app_rest_search_operator_list"),
    re_path(r"^search_operator/(?P<pk>\w+)/$",
            search_operator_views.SearchOperatorDetail.as_view(),
            name="core_explore_keyword_app_rest_search_operator")
]

urlpatterns = format_suffix_patterns(urlpatterns)
