"""Core Explore Keyword App views
"""
import json
import re
from typing import Dict, Any, List

from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

import core_explore_keyword_app.components.persistent_query_keyword.api as \
    persistent_query_keyword_api
import core_explore_keyword_app.permissions.rights as rights
import core_main_app.components.version_manager.api as version_manager_api
import core_main_app.utils.decorators as decorators
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.settings import DEFAULT_DATE_TOGGLE_VALUE, SORTING_DISPLAY_TYPE
from core_explore_common_app.utils.query.query import create_default_query
from core_explore_common_app.views.user.views import ResultQueryRedirectView
from core_explore_keyword_app.forms import KeywordForm
from core_explore_keyword_app.settings import INSTALLED_APPS
from core_explore_keyword_app.utils.search_operators import build_search_operator_query, \
    get_keywords_from_search_operator_query
from core_main_app.commons.exceptions import DoesNotExist, ApiError
from core_main_app.components.template import api as template_api
from core_main_app.settings import DATA_SORTING_FIELDS
from core_main_app.utils.databases.pymongo_database import get_full_text_query
from core_main_app.utils.rendering import render


class KeywordSearchView(View):

    def __init__(self, **kwargs):
        self.assets = self._load_assets()
        self.modals = self._load_modals()

        super().__init__(**kwargs)

    @method_decorator(decorators.permission_required(
        content_type=rights.explore_keyword_content_type,
        permission=rights.explore_keyword_access,
        login_url=reverse_lazy("core_main_app_login"))
    )
    def get(self, request, **kwargs):
        """ GET

        Args:
            request:
            **kwargs:

        Returns:

        """
        query_id = str(kwargs["query_id"]) if "query_id" in kwargs else None

        # assets / modals / forms
        context = self._get(request, query_id)

        return render(request,
                      "core_explore_keyword_app/user/index.html",
                      assets=self.assets,
                      modals=self.modals,
                      context=context)

    @method_decorator(decorators.permission_required(
        content_type=rights.explore_keyword_content_type,
        permission=rights.explore_keyword_access,
        login_url=reverse_lazy("core_main_app_login"))
    )
    def post(self, request):
        """ POST

        Args:
            request:

        Returns:

        """

        # assets / modals / forms
        context = self._post(request)

        return render(request,
                      "core_explore_keyword_app/user/index.html",
                      assets=self.assets,
                      modals=self.modals,
                      context=context)

    @staticmethod
    def _parse_query(query_content):
        keyword_list = list()
        query_json = json.loads(query_content)
        queries = list()

        if "$and" in query_json:
            queries += query_json["$and"]

        queries += [
            {key: value} for key, value in query_json.items()
            if key != "$and" and key != "$or"
        ]

        for query in queries:
            if "$text" in query:
                keyword_list += re.sub(
                    r"['\"]", "", query["$text"]["$search"]
                ).split(" ")
            elif len(query.keys()) != 0:  # Avoid parsing empty query
                keyword = get_keywords_from_search_operator_query(query)

                if keyword is not None:
                    keyword_list.append(keyword)

        return ",".join(keyword_list)

    def _get(self, request, query_id):
        """ Prepare the GET context

        Args:
            query_id:

        Returns:

        """
        error = None
        # set the correct default ordering for the context
        default_order = ','.join(DATA_SORTING_FIELDS)
        if query_id is None:
            # create query
            query = create_default_query(request, [])
            # upsert the query
            query_api.upsert(query)
            # create keyword form
            # create all data for select values in forms
            keywords_data_form = {
                "query_id": str(query.id),
                "user_id": query.user_id,
            }
        else:  # query_id is not None
            try:
                # get the query id
                query = query_api.get_by_id(query_id)
                user_id = query.user_id

                # get all keywords back
                keywords = self._parse_query(query.content)

                # get all version managers
                version_managers = []
                for template in query.templates:
                    version_managers.append(str(version_manager_api.get_from_version(template).id))
                # create all data for select values in forms
                keywords_data_form = {
                    "query_id": str(query.id),
                    "user_id": user_id,
                    "keywords": keywords,
                    "global_templates": version_managers,
                    "order_by_field": self._build_sorting_context_array(query),
                    "user_templates": version_managers
                }
                # set the correct ordering for the context
                if keywords_data_form['order_by_field'] != 0:
                    default_order = keywords_data_form['order_by_field']
            except Exception as e:
                error = "An unexpected error occurred while loading the query: {}.".format(str(e))
                return {"error": error}

        search_form = KeywordForm(data=keywords_data_form)
        return _format_keyword_search_context(search_form, error, None, default_order)

    def _post(self, request):
        """ Prepare the POST context

        Args:
            request:

        Returns:

        """
        error = None
        warning = None
        search_form = KeywordForm(data=request.POST)
        # validate form
        if search_form.is_valid():
            try:
                # get form values
                query_id = search_form.cleaned_data.get("query_id", None)
                keywords = search_form.cleaned_data.get("keywords", None)
                global_templates = search_form.cleaned_data.get("global_templates", [])
                user_templates = search_form.cleaned_data.get("user_templates", [])
                order_by_field_array = search_form.cleaned_data.get(
                    "order_by_field", ""
                ).strip().split(";")
                # get all template version manager ids
                template_version_manager_ids = global_templates + user_templates
                # from ids, get all version manager
                version_manager_list = version_manager_api.get_by_id_list(
                    template_version_manager_ids
                )
                # from all version manager, build a list of all version (template)
                template_ids = []
                list([template_ids.extend(x.versions) for x in version_manager_list])
                if query_id is None or keywords is None:
                    error = "Expected parameters are not provided"
                else:
                    # get query
                    query = query_api.get_by_id(query_id)
                    if len(query.data_sources) == 0:
                        warning = "Please select at least 1 data source."
                    else:
                        # update query
                        query.templates = template_api.get_all_by_id_list(template_ids)
                        query.content = self._build_query(keywords.split(","))
                        # set the data-sources filter value according to the POST request field
                        for data_sources_index in range(len(query.data_sources)):
                            # update the data-source filter only if it's not a new data-source
                            # (the default filter value is already added when the data-source
                            # is created)
                            if data_sources_index in range(0, len(order_by_field_array)):
                                query.data_sources[
                                    data_sources_index
                                ].order_by_field = order_by_field_array[data_sources_index]

                        query_api.upsert(query)
            except DoesNotExist:
                error = "An unexpected error occurred while retrieving the query."
            except Exception as e:
                error = "An unexpected error occurred: {}.".format(str(e))
        else:
            error = "An unexpected error occurred: the form is not valid."

        return _format_keyword_search_context(
            search_form, error, warning, search_form.cleaned_data.get("order_by_field", "").strip()
        )

    @staticmethod
    def _build_query(initial_keyword_list):
        """ Build query content with correct keywords and search operators

        Args:
            initial_keyword_list:

        Returns:
        """
        main_query = list()
        keyword_list = list()

        for keyword in initial_keyword_list:
            if ":" in keyword:
                try:
                    split_keyword = keyword.split(":")

                    main_query.append(
                        build_search_operator_query(
                            split_keyword[0], split_keyword[1]
                        )
                    )
                except ApiError:
                    keyword_list.append(keyword)
            else:
                keyword_list.append(keyword)

        keyword_query = get_full_text_query(",".join(keyword_list))

        # Don"t add an empty query to the main query.
        if len(keyword_query.keys()) != 0:
            main_query.append(keyword_query)

        # If the query is empty, match all documents
        if len(main_query) == 0:
            return json.dumps({})
        elif len(main_query) == 1:  # If there is one query item, match one this item.
            return json.dumps(main_query[0])
        else:  # For multiple items, a "$and" query is needed.
            return json.dumps({
                "$and": main_query
            })

    @staticmethod
    def _load_assets():
        """ Return assets structure

        Returns:

        """
        assets: Dict[str, List[Any]] = {
            "js": [
                {
                    "path": "core_explore_common_app/user/js/results.js",
                    "is_raw": False
                },
                {
                    "path": "core_explore_common_app/user/js/results.raw.js",
                    "is_raw": True
                },
                {
                    "path": "core_main_app/common/js/XMLTree.js",
                    "is_raw": False
                },
                {
                    "path": "core_main_app/common/js/modals/error_page_modal.js",
                    "is_raw": True
                },
                {
                    "path": "core_explore_keyword_app/libs/tag-it/2.0/js/tag-it.js",
                    "is_raw": True
                },
                {
                    "path": "core_explore_keyword_app/libs/stretchy/stretchy.min.js",
                    "is_raw": False
                },
                {
                    "path": "core_main_app/common/js/debounce.js",
                    "is_raw": True
                },
                {
                    "path": "core_explore_keyword_app/user/js/search/search.js",
                    "is_raw": False
                },
                {
                    "path":
                        "core_explore_keyword_app/user/js/search/autocomplete_source.js",
                    "is_raw": False
                },
                {
                    "path": "core_explore_common_app/user/js/button_persistent_query.js",
                    "is_raw": False
                },
                {
                    "path": "core_explore_common_app/user/js/sorting_{0}_criteria.js".format(
                        SORTING_DISPLAY_TYPE
                    ),
                    "is_raw": False
                }
            ],
            "css": [
                "core_explore_common_app/user/css/query_result.css",
                "core_main_app/common/css/XMLTree.css",
                "core_explore_common_app/user/css/results.css",
                "core_explore_common_app/user/css/toggle.css",
                "core_explore_keyword_app/libs/tag-it/2.0/css/jquery.tagit.css",
                "core_explore_keyword_app/user/css/search/search.css"
            ],
        }

        # Add assets needed for the exporters
        if "core_exporters_app" in INSTALLED_APPS:
            assets["js"].extend([{
                "path":
                    "core_exporters_app/user/js/exporters/list/modals/list_exporters_selector.js",
                "is_raw": False
            }])

        # Add assets needed for the file preview
        if "core_file_preview_app" in INSTALLED_APPS:
            assets["js"].extend([
                {
                    "path": "core_file_preview_app/user/js/file_preview.js",
                    "is_raw": False
                }
            ])
            assets["css"].append("core_file_preview_app/user/css/file_preview.css")

        return assets

    @staticmethod
    def _build_sorting_context_array(query):
        """ Get the query data-sources dans build the context sorting array for the JS

        Returns:

        """
        context_array = []
        for data_source in query.data_sources:
            context_array.append(data_source.order_by_field)

        return ';'.join(context_array)

    @staticmethod
    def _load_modals():
        """ Return modals structure

        Returns:

        """
        modals = [
            "core_main_app/common/modals/error_page_modal.html",
            "core_explore_common_app/user/persistent_query/modals/persistent_query_modal.html"
        ]

        if "core_exporters_app" in INSTALLED_APPS:
            # add the modal
            modals.extend([
                "core_exporters_app/user/exporters/list/modals/list_exporters_selector.html"
            ])

        if "core_file_preview_app" in INSTALLED_APPS:
            modals.append("core_file_preview_app/user/file_preview_modal.html")

        return modals


def _format_keyword_search_context(search_form, error, warning, query_order=""):
    """ Format the context for the keyword research page

    Args:
        search_form:
        error:
        warning:
        query_order:

    Returns:

    """
    context = {
        "search_form": search_form,
        "query_id": search_form.data["query_id"],
        "error": error,
        "warning": warning,
        "default_date_toggle_value": DEFAULT_DATE_TOGGLE_VALUE,
        "data_sources_selector_template":
            "core_explore_common_app/user/selector/data_sources_selector.html",
        "data_sorting_fields": query_order,
        "default_data_sorting_fields": ",".join(DATA_SORTING_FIELDS),
        "get_shareable_link_url": reverse("core_explore_keyword_get_persistent_query_url")
    }

    return context


class ResultQueryRedirectKeywordView(ResultQueryRedirectView):

    @staticmethod
    def _get_persistent_query(persistent_query_id):
        return persistent_query_keyword_api.get_by_id(persistent_query_id)

    @staticmethod
    def _get_reversed_url(query):
        return reverse("core_explore_keyword_app_search", kwargs={"query_id": query.id})

    @staticmethod
    def _get_reversed_url_if_failed():
        return reverse("core_explore_keyword_app_search")
