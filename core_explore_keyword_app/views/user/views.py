"""Core Explore Keyword App views
"""
import json

from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query
from core_explore_keyword_app.forms import KeywordForm
from core_main_app.utils.databases.pymongo_database import get_full_text_query
from core_main_app.utils.rendering import render


def keyword_search(request):
    """ Explore by keyword search view

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": 'core_explore_common_app/user/js/results.js',
                "is_raw": False
            },
            {
                "path": 'core_explore_common_app/user/js/results.raw.js',
                "is_raw": True
            },
            {
                "path": 'core_main_app/common/js/XMLTree.js',
                "is_raw": False
            },
            {
                "path": 'core_main_app/common/js/modals/error_page_modal.js',
                "is_raw": True
            }
        ],
        "css": ["core_explore_example_app/user/css/query_result.css",
                "core_main_app/common/css/XMLTree.css",
                "core_explore_common_app/user/css/results.css"],
    }

    modals = [
        "core_main_app/common/modals/error_page_modal.html"
    ]

    if request.method == 'POST':
        search_form = KeywordForm(request.POST)
        if search_form.is_valid():
            # get form values
            query_id = request.POST['query_id']
            keywords = request.POST['keywords']
            # update query
            query = query_api.get_by_id(query_id)
            query.content = json.dumps(get_full_text_query(keywords))
            query_api.upsert(query)
    else:
        # create query
        query = Query(user_id=str(request.user.id), templates=[])
        query_api.upsert(query)
        # create form
        search_form = KeywordForm({'query_id': str(query.id)})

    context = {
        'search_form': search_form,
        'query_id': search_form.data['query_id'],
        'local_query_url': 'core_explore_common_local_query',
        'data_sources_selector_template': 'core_explore_common_app/user/selector/data_sources_selector.html'
    }

    return render(request,
                  'core_explore_keyword_app/user/index.html',
                  assets=assets,
                  modals=modals,
                  context=context)
