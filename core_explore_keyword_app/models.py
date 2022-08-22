"""Explore Keyword models
"""

from django.db import models

from core_main_app.permissions.utils import get_formatted_name
from core_explore_keyword_app.permissions import rights


class ExploreKeyword(models.Model):
    """Explore Keyword"""

    class Meta:
        """Meta"""

        verbose_name = "core_explore_keyword_app"
        default_permissions = ()
        permissions = (
            (
                rights.EXPLORE_KEYWORD_ACCESS,
                get_formatted_name(rights.EXPLORE_KEYWORD_ACCESS),
            ),
        )
