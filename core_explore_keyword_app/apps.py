""" Apps file for setting core package when app is ready
"""
from django.apps import AppConfig
from core_main_app.utils.databases.pymongo_database import init_text_index


class ExploreKeywordAppConfig(AppConfig):
    """ Core application settings
    """
    name = 'core_explore_keyword_app'

    def ready(self):
        """ Run when the app is ready.

        Returns:

        """
        init_text_index('data')
