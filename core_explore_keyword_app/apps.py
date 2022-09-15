""" Apps file for setting core package when app is ready
"""
import sys

from django.apps import AppConfig

from core_explore_keyword_app.permissions import discover


class ExploreKeywordAppConfig(AppConfig):
    """Core application settings"""

    name = "core_explore_keyword_app"
    verbose_name = "Core Explore by Keyword App"

    def ready(self):
        """Run when the app is ready.

        Returns:

        """
        if "migrate" not in sys.argv:
            discover.init_permissions(self.apps)
