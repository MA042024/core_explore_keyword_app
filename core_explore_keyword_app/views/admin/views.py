""" Admin views for explore by keyword
"""
from django.views.generic import View

from core_main_app.utils.rendering import admin_render
from core_explore_keyword_app.components.search_operator import (
    api as search_operator_api,
)
from core_explore_keyword_app.views.admin.forms import SearchOperatorForm


class ListSearchOperatorsView(View):
    """List Search Operators View"""

    def get(self, request):
        """View to assign search operators to template

        Args:
            request:

        Returns:

        """
        context = {
            "title": "Search Operator Manager",
            "subtitle": "Operator List",
        }

        assets = {
            "js": [
                {
                    "path": "core_explore_keyword_app/admin/js/search_operators.js",
                    "is_raw": False,
                },
                {
                    "path": "core_explore_keyword_app/admin/js/search_ops_manager.js",
                    "is_raw": False,
                },
                {
                    "path": "core_explore_keyword_app/admin/js/search_ops_manager_delete.js",
                    "is_raw": False,
                },
            ],
            "css": [
                "core_explore_keyword_app/admin/css/search_ops_manager.css"
            ],
        }

        modals = [
            "core_explore_keyword_app/admin/search_ops_manager/modal/config/modal.html",
            "core_explore_keyword_app/admin/search_ops_manager/modal/delete/modal.html",
        ]

        try:
            context.update(
                {
                    "operators": search_operator_api.get_all(),
                    "operator_form": SearchOperatorForm(),
                }
            )

            return admin_render(
                request,
                "core_explore_keyword_app/admin/search_ops_manager.html",
                modals=modals,
                assets=assets,
                context=context,
            )
        except Exception as exception:
            context.update(
                {
                    "error": "Unable to load the page: %s."
                    % str(exception).lower()
                }
            )

            return admin_render(
                request,
                "core_main_app/admin/commons/errors/errors_wrapper.html",
                context=context,
            )
