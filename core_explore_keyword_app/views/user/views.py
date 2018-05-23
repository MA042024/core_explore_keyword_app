"""Core Explore Keyword App views
"""
import json

from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

import core_explore_keyword_app.permissions.rights as rights
import core_main_app.components.version_manager.api as version_manager_api
import core_explore_keyword_app.components.persistent_query_keyword.api as persistent_query_keyword_api
import core_main_app.utils.decorators as decorators
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query
from core_explore_keyword_app.settings import INSTALLED_APPS
from core_explore_common_app.views.user.views import ResultQueryRedirectView
from core_explore_keyword_app.forms import KeywordForm
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.template import api as template_api
from core_main_app.utils.databases.pymongo_database import get_full_text_query
from core_main_app.utils.rendering import render


class KeywordSearchView(View):

    @method_decorator(decorators.
                      permission_required(content_type=rights.explore_keyword_content_type,
                                          permission=rights.explore_keyword_access,
                                          login_url=reverse_lazy("core_main_app_login")))
    def get(self, request, *args, **kwargs):
        error = None
        data_form = None
        display_persistent_query_button = False
        if 'query_id' not in kwargs:
            # create query
            query = Query(user_id=str(request.user.id), templates=[])
            query_api.upsert(query)
            # create keyword form
            # create all data for select values in forms
            data_form = {
                'query_id': str(query.id),
                'user_id': query.user_id,
            }
        else:
            try:
                # get the query id
                query = query_api.get_by_id(str(kwargs['query_id']))
                user_id = query.user_id
                # get all keywords back
                query_json = json.loads(query.content)
                keywords = None
                if '$text' in query_json:
                    keywords = query_json['$text']['$search'].replace(" ", ",").replace('"', '')
                # get all version managers
                version_managers = []
                for template in query.templates:
                    version_managers.append(str(version_manager_api.get_from_version(template).id))
                # create all data for select values in forms
                data_form = {
                    'query_id': str(query.id),
                    'user_id': user_id,
                    'keywords': keywords,
                    'global_templates': version_managers,
                    'user_templates': version_managers
                }
                display_persistent_query_button = True
            except Exception, e:
                error = "An unexpected error occurred while loading the query: {}.".format(e.message)

        # re-init the form
        search_form = KeywordForm(data=data_form)
        assets = self._load_assets()
        modals = self._load_modals()

        context = self._load_context(search_form, error, display_persistent_query_button)

        return render(request,
                      'core_explore_keyword_app/user/index.html',
                      assets=assets,
                      modals=modals,
                      context=context)

    @method_decorator(decorators.
                      permission_required(content_type=rights.explore_keyword_content_type,
                                          permission=rights.explore_keyword_access,
                                          login_url=reverse_lazy("core_main_app_login")))
    def post(self, request, *args, **kwargs):
        error = None
        search_form = KeywordForm(data=request.POST)
        display_persistent_query_button = False
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
                        display_persistent_query_button = True
            except DoesNotExist:
                error = "An unexpected error occurred while retrieving the query."
            except Exception, e:
                error = "An unexpected error occurred: {}.".format(e.message)
        else:
            error = "An unexpected error occurred: the form is not valid."

        assets = self._load_assets()
        modals = self._load_modals()
        context = self._load_context(search_form, error, display_persistent_query_button)

        return render(request,
                      'core_explore_keyword_app/user/index.html',
                      assets=assets,
                      modals=modals,
                      context=context)

    @staticmethod
    def _load_assets():
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
                        },
                        {
                            "path": 'core_explore_common_app/user/js/button_persistent_query.js',
                            "is_raw": False
                        },
                    ],
                    "css": ["core_explore_common_app/user/css/query_result.css",
                            "core_main_app/common/css/XMLTree.css",
                            "core_explore_common_app/user/css/results.css",
                            "core_explore_keyword_app/libs/tag-it/2.0/css/jquery.tagit.css",
                            'core_explore_keyword_app/user/css/search/search.css'],
                }

        if 'core_exporters_app' in INSTALLED_APPS:
            # add all assets needed
            assets['js'].extend([{
                "path": 'core_exporters_app/user/js/exporters/list/modals/list_exporters_selector.js',
                "is_raw": False
            }])

        return assets

    @staticmethod
    def _load_modals():
        modals = [
                    "core_main_app/common/modals/error_page_modal.html",
                    "core_explore_common_app/user/persistent_query/modals/persistent_query_modal.html"
               ]

        if 'core_exporters_app' in INSTALLED_APPS:
            # add the modal
            modals.extend([
                "core_exporters_app/user/exporters/list/modals/list_exporters_selector.html"
            ])

        return modals

    @staticmethod
    def _load_context(search_form, error, display_persistent_query_button):
        context = {
            'search_form': search_form,
            'query_id': search_form.data['query_id'],
            'error': error,
            'data_sources_selector_template': 'core_explore_common_app/user/selector/data_sources_selector.html',
            'get_shareable_link_url': reverse("core_explore_keyword_get_persistent_query_url"),
            'display_persistent_query_button': display_persistent_query_button
        }

        if 'core_exporters_app' in INSTALLED_APPS:
            context['exporter_app'] = True

        return context


class ResultQueryRedirectKeywordView(ResultQueryRedirectView):

    @staticmethod
    def _get_persistent_query(persistent_query_id):
        return persistent_query_keyword_api.get_by_id(persistent_query_id)

    @staticmethod
    def _get_reversed_url(query):
        return reverse("core_explore_keyword_app_search", kwargs={'query_id': query.id})

    @staticmethod
    def _get_reversed_url_if_failed():
        return reverse("core_explore_keyword_app_search")
