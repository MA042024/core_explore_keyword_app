""" Persistent Query Example API
"""
from core_explore_keyword_app.components.persistent_query_keyword.models import (
    PersistentQueryKeyword,
)
from core_main_app.access_control.decorators import access_control
from core_explore_common_app.access_control.api import can_read_persistent_query


@access_control(can_read_persistent_query)
def get_by_id(persistent_query_keyword_id, user):
    """Return the Persistent Query Keyword with the given id

    Args:
        persistent_query_keyword_id:
        user:
    Returns:

    """
    return PersistentQueryKeyword.get_by_id(persistent_query_keyword_id)


@access_control(can_read_persistent_query)
def get_by_name(persistent_query_keyword_name, user):
    """Return the Persistent Query Keyword with the given name

    Args:
        persistent_query_keyword_name:
        user:
    Returns:

    """
    return PersistentQueryKeyword.get_by_name(persistent_query_keyword_name)
