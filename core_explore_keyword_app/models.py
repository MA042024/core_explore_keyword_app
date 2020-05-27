"""Explore Keyword models
"""

from django.db import models

from core_explore_keyword_app.permissions import rights
from core_main_app.permissions.utils import get_formatted_name


class ExploreKeyword(models.Model):
    class Meta(object):
        verbose_name = "core_explore_keyword_app"
        default_permissions = ()
        permissions = (
            (
                rights.explore_keyword_access,
                get_formatted_name(rights.explore_keyword_access),
            ),
        )
