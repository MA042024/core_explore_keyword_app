""" Discover rules for core explore keyword app.
"""
import logging

from core_explore_keyword_app.permissions import rights as explore_keyword_rights
from core_main_app.permissions import rights as main_rights

logger = logging.getLogger(__name__)


def init_permissions(apps):
    """Initialization of groups and permissions.

    Args:
        apps (Apps): List of applications to init
    """
    try:
        group = apps.get_model("auth", "Group")
        permission = apps.get_model("auth", "Permission")

        # Get or Create the default group
        default_group, created = group.objects.get_or_create(
            name=main_rights.default_group
        )

        # Get explore keyword permissions
        explore_access_perm = permission.objects.get(
            codename=explore_keyword_rights.explore_keyword_access
        )

        # Add permissions to default group
        default_group.permissions.add(explore_access_perm)
    except Exception as e:
        logger.error("Impossible to init explore_keyword permissions: %s" % str(e))
