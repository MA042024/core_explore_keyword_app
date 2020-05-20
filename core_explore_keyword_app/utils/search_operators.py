""" Search operators utilities
"""
import logging

from core_explore_keyword_app.components.search_operator import (
    api as search_operator_api,
)
from core_main_app.commons.exceptions import ApiError

LOGGER = logging.getLogger(__name__)


def build_search_operator_query(search_operator_name, value):
    search_operator = search_operator_api.get_by_name(search_operator_name)
    search_operator_list = [
        {search_operator_dot_notation: value}
        for search_operator_dot_notation in search_operator.dot_notation_list
    ]

    # Add `#text` field in case it is defined
    search_operator_list += [
        {"%s.#text" % search_operator_dot_notation: value}
        for search_operator_dot_notation in search_operator.dot_notation_list
    ]

    return {"$or": search_operator_list}


def get_keywords_from_search_operator_query(query):
    dot_notation_list = [list(query_item.keys())[0] for query_item in query["$or"]]
    dot_notation_list = [
        dot_notation_item
        for dot_notation_item in dot_notation_list
        if not dot_notation_item.endswith("#text")
    ]
    value = list(query["$or"][0].values())[0]

    try:
        return "%s:%s" % (
            search_operator_api.get_by_dot_notation_list(dot_notation_list).name,
            value,
        )
    except ApiError as api_error:
        LOGGER.info("API error for query: %s (%s)" % (str(query), str(api_error)))
        return None
