""" Search operators utilities
"""
from core_explore_keyword_app.components.search_operator import api as \
    search_operator_api


def build_search_operator_query(search_operator_name, value):
    search_operator = search_operator_api.get_by_name(search_operator_name)
    search_operator_list = [{
        search_operator_dot_notation: value
    } for search_operator_dot_notation in search_operator.dot_notation_list]

    if len(search_operator_list) == 1:
        return search_operator_list[0]
    else:
        return {"$or": search_operator_list}


def get_keywords_from_search_operator_query(query):
    if "$or" in query:
        dot_notation_list = [list(query_item.keys())[0] for query_item in query["$or"]]
        value = list(query["$or"][0].values())[0]
    else:
        dot_notation_list = list(query.keys())
        value = list(query.values())[0]

    return "%s:%s" % (
        search_operator_api.get_by_dot_notation_list(dot_notation_list).name, value
    )
