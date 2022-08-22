"""Explore keyword app Ajax views
"""
import json
import logging
import re

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View

from core_main_app.components.template import api as template_api
from core_main_app.utils.databases.mongo.pymongo_database import get_full_text_query
import core_main_app.components.template_version_manager.api as template_version_manager_api
from core_main_app.utils import decorators

from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.constants import LOCAL_QUERY_NAME
from core_explore_common_app.utils.query.query import send, create_local_data_source
from core_explore_common_app.views.user.ajax import CreatePersistentQueryUrlView
from core_explore_keyword_app.permissions import rights
from core_explore_keyword_app.components.persistent_query_keyword.models import (
    PersistentQueryKeyword,
)
from core_explore_keyword_app.forms import KeywordForm


logger = logging.getLogger("core_explore_keyword_app.views.user.ajax")


def _is_local_in_data_source(query):
    """Check if there is a data source that is local.

    Args:
        query:

    Returns:
    """
    # If we find a data source that is local
    for data_source in query.data_sources:
        # find local data source
        if data_source["name"] == LOCAL_QUERY_NAME:
            return True
    return False


def check_data_source(query):
    """Check the data sources. We will not provide suggestions if there are data sources selected but none of them is local.

    Args:
        query:

    Returns:
    """

    return len(query.data_sources) == 0 or _is_local_in_data_source(query)


class SuggestionsKeywordSearchView(View):
    """Suggestions Keyword Search View"""

    @method_decorator(
        decorators.permission_required(
            content_type=rights.EXPLORE_KEYWORD_CONTENT_TYPE,
            permission=rights.EXPLORE_KEYWORD_ACCESS,
            login_url=reverse_lazy("core_main_app_login"),
        )
    )
    def post(self, request, *args, **kwargs):
        """POST

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        suggestions = []
        search_form = KeywordForm(data=request.POST, request=request)
        keywords = request.POST.get("term")

        if search_form.is_valid():
            try:
                # get form values
                query_id = search_form.cleaned_data.get("query_id", None)
                global_templates = search_form.cleaned_data.get("global_templates", [])
                user_templates = search_form.cleaned_data.get("user_templates", [])

                # get all template version manager ids
                template_version_manager_ids = global_templates + user_templates

                # from ids, get all version manager
                version_manager_list = template_version_manager_api.get_by_id_list(
                    template_version_manager_ids, request=request
                )

                # from all version manager, build a list of all version (template)
                template_ids = []
                list([template_ids.extend(x.versions) for x in version_manager_list])

                if query_id is not None and keywords is not None:
                    # get query
                    query = query_api.get_by_id(query_id, request.user)

                    # Check the selected data sources
                    if check_data_source(query):

                        # Prepare query
                        query = self._get_query_prepared(
                            keywords, query, request, template_ids
                        )

                        # Send query
                        dict_results = send(
                            request, query, len(query.data_sources) - 1, 1
                        )

                        if dict_results["count"] > 0:
                            self._extract_suggestion_from_results(
                                dict_results, keywords, suggestions
                            )

            except Exception as exception:
                logger.error(
                    "Exception while generating suggestions: " + str(exception)
                )

        return HttpResponse(
            json.dumps({"suggestions": suggestions}),
            content_type="application/javascript",
        )

    def _get_query_prepared(self, keywords, query, request, template_ids):
        """Prepare the query for suggestions.

        Args:
            keywords:
            query:
            request:
            template_ids:
        Returns:
        """

        # update query
        query.templates.set(
            template_api.get_all_accessible_by_id_list(template_ids, request=request)
        )
        # TODO: improve query to get better results
        query.content = json.dumps(get_full_text_query(keywords))
        # Data source is local
        query.data_sources = [create_local_data_source(request)]
        return query

    def _extract_suggestion_from_results(self, dict_results, keywords, suggestions):
        """Extract suggestion from

        Args:
            dict_results:
            keywords:
            suggestions:

        Returns:
        """
        results = dict_results["results"]
        # Prepare keywords
        wordList = re.sub("[^\w]", " ", keywords).split()
        wordList = [x + "|" + x + "\w+" for x in wordList]
        wordList = "|".join(wordList)
        for result in results:
            # Extract suggestions from data
            listWholeKeywords = re.findall(
                "\\b(" + wordList + ")\\b", result["xml_content"], flags=re.IGNORECASE
            )
            labels = list(set(listWholeKeywords))

            for label in labels:
                label = label.lower()
                result_json = {}
                result_json["label"] = label
                result_json["value"] = label
                if not result_json in suggestions:
                    suggestions.append(result_json)


class CreatePersistentQueryUrlKeywordView(CreatePersistentQueryUrlView):
    """Create the persistent url from a Query"""

    view_to_reverse = "core_explore_keyword_results_redirect"

    @staticmethod
    def _create_persistent_query(query):
        # create the persistent query
        return PersistentQueryKeyword(
            user_id=query.user_id,
            content=query.content,
            data_sources=query.data_sources,
        )
