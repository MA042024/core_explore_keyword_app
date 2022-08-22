"""Template tag to include the search bar
"""

from django import template

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.settings import DATA_SORTING_FIELDS
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query
from core_explore_common_app.views.user.ajax import add_local_data_source
from core_explore_keyword_app.forms import KeywordForm


register = template.Library()


@register.inclusion_tag(
    "core_explore_keyword_app/user/embedded_search_bar.html", takes_context=True
)
def show_search_bar(context):
    """Include the search bar in a template.

    Args:
        context: Context

    Returns:

    """
    request = context["request"]
    try:
        # create Query
        query = Query(user_id=str(request.user.id))

        # add local data source to the query
        add_local_data_source(request, query)

        # set visibility
        query_api.set_visibility_to_query(query, request.user)

        # upsert the query
        query_api.upsert(query, request.user)

        # create keyword form
        data_form = {
            "query_id": str(query.id),
            "user_id": query.user_id,
            "order_by_field": ",".join(DATA_SORTING_FIELDS),
        }
        search_form = KeywordForm(data=data_form, request=request)

        context = {
            "data": {
                "search_form": search_form,
                "query_id": search_form.data["query_id"],
            }
        }
    except AccessControlError as ace:
        context = {"data": {"error": str(ace)}}
    except:
        context = {"data": {"error": "An unexpected error occurred"}}

    return template.RequestContext(request, context)
