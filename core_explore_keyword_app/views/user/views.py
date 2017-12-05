"""Core Explore Keyword App views
"""
import json

from django.core.urlresolvers import reverse_lazy

import core_explore_keyword_app.permissions.rights as rights
import core_main_app.utils.decorators as decorators
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query
from core_explore_example_app.settings import INSTALLED_APPS
from core_explore_keyword_app.forms import KeywordForm
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.template import api as template_api
from core_main_app.utils.databases.pymongo_database import get_full_text_query
from core_main_app.utils.rendering import render
import core_main_app.components.version_manager.api as version_manager_api


@decorators.permission_required(content_type=rights.explore_keyword_content_type,
                                permission=rights.explore_keyword_access, login_url=reverse_lazy("core_main_app_login"))
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
            },
            {
                "path": 'core_explore_keyword_app/libs/tag-it/2.0/js/tag-it.js',
                "is_raw": True
            },
            {
                "path": 'core_explore_keyword_app/user/js/search/search.js',
                "is_raw": True
            }
        ],
        "css": ["core_explore_example_app/user/css/query_result.css",
                "core_main_app/common/css/XMLTree.css",
                "core_explore_common_app/user/css/results.css",
                "core_explore_keyword_app/libs/tag-it/2.0/css/jquery.tagit.css",
                'core_explore_keyword_app/user/css/search/search.css'],
    }

    modals = [
        "core_main_app/common/modals/error_page_modal.html"
    ]

    error = None

    if request.method == 'POST':
        search_form = KeywordForm(data=request.POST)
        # validate form
        if search_form.is_valid():
            try:
                # get form values
                query_id = search_form.cleaned_data.get('query_id', None)
                keywords = search_form.cleaned_data.get('keywords', None)
                global_templates = search_form.cleaned_data.get('global_templates', [])
                user_templates = search_form.cleaned_data.get('user_templates', [])
                # get all template version manager ids
                template_version_manager_ids = global_templates + user_templates
                # from ids, get all version manager
                version_manager_list = version_manager_api.get_by_id_list(template_version_manager_ids)
                # from all version manager, build a list of all version (template)
                template_ids = []
                map(lambda x: template_ids.extend(x.versions), version_manager_list)
                if query_id is None or keywords is None:
                    error = "Expected parameters are not provided"
                else:
                    # get query
                    query = query_api.get_by_id(query_id)
                    if len(query.data_sources) == 0:
                        error = "Please select at least 1 data source."
                    else:
                        # update query
                        query.templates = template_api.get_all_by_id_list(template_ids)
                        query.content = json.dumps(get_full_text_query(keywords))
                        query_api.upsert(query)
            except DoesNotExist:
                error = "An unexpected error occurred while retrieving the query."
            except Exception, e:
                error = "An unexpected error occurred: {}.".format(e.message)
        else:
            error = "An unexpected error occurred: the form is not valid."
    else:
        # create query
        query = Query(user_id=str(request.user.id), templates=[])
        query_api.upsert(query)
        # create keyword form
        search_form = KeywordForm(data={'query_id': str(query.id), 'user_id': str(request.user.id)})

    context = {
        'search_form': search_form,
        'query_id': search_form.data['query_id'],
        'error': error,
        'local_query_url': 'core_explore_common_local_query',
        'data_sources_selector_template': 'core_explore_common_app/user/selector/data_sources_selector.html',
    }

    if 'core_exporters_app' in INSTALLED_APPS:
        # add all assets needed
        assets['js'].extend([{
            "path": 'core_exporters_app/user/js/exporters/list/modals/list_exporters_selector.js',
            "is_raw": False
        }])
        # add the modal
        modals.extend([
            "core_exporters_app/user/exporters/list/modals/list_exporters_selector.html"
        ])

        context['exporter_app'] = True

    return render(request,
                  'core_explore_keyword_app/user/index.html',
                  assets=assets,
                  modals=modals,
                  context=context)
