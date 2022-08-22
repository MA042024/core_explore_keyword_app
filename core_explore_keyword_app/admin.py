""" Url router for administration views
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from core_main_app.admin import core_admin_site
from core_explore_keyword_app.components.persistent_query_keyword.admin_site import (
    CustomPersistentQueryKeywordAdmin,
)
from core_explore_keyword_app.components.persistent_query_keyword.models import (
    PersistentQueryKeyword,
)
from core_explore_keyword_app.components.search_operator.admin_site import (
    CustomSearchOperatorAdmin,
)
from core_explore_keyword_app.components.search_operator.models import SearchOperator
from core_explore_keyword_app.views.admin import ajax as admin_ajax
from core_explore_keyword_app.views.admin import views as admin_views

admin_urls = [
    re_path(
        r"^operators/$",
        staff_member_required(admin_views.ListSearchOperatorsView.as_view()),
        name="core_explore_keyword_app_list_search_operators",
    ),
    re_path(
        r"^operators/edit$",
        staff_member_required(admin_ajax.SearchOperatorConfigModalView.as_view()),
        name="core_explore_keyword_app_search_operator_config_modal",
    ),
    re_path(
        r"^operators/delete$",
        staff_member_required(admin_ajax.SearchOperatorDeleteModalView.as_view()),
        name="core_explore_keyword_app_search_operator_delete_modal",
    ),
]

admin.site.register(SearchOperator, CustomSearchOperatorAdmin)
admin.site.register(PersistentQueryKeyword, CustomPersistentQueryKeywordAdmin)
urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
