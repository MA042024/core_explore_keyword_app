""" Persistent Query Keyword API
"""

from core_main_app.access_control.api import has_perm_administration
from core_main_app.access_control.decorators import access_control
from core_explore_common_app.access_control.api import (
    can_read_persistent_query,
    can_write_persistent_query,
)
from core_explore_keyword_app.components.persistent_query_keyword.models import (
    PersistentQueryKeyword,
)


@access_control(can_write_persistent_query)
def upsert(persistent_query_keyword, user):
    """Saves or update persistent query

    Args:
        persistent_query_keyword:
        user:

    Returns:

    """
    persistent_query_keyword.save()
    return persistent_query_keyword


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


@access_control(can_write_persistent_query)
def delete(persistent_query_keyword, user):
    """Deletes the Persistent Query Keyword

    Args:
        persistent_query_keyword:
        user:
    """
    persistent_query_keyword.delete()


@access_control(can_write_persistent_query)
def set_name(persistent_query_keyword, name, user):
    """Set name to Persistent Query Keyword

    Args:
        persistent_query_keyword:
        name:
        user:
    """
    persistent_query_keyword.name = name
    persistent_query_keyword.save()


@access_control(has_perm_administration)
def get_all(user):
    """get all Persistent Query Keyword

    Args:
        user:
    """
    return PersistentQueryKeyword.get_all()


@access_control(can_read_persistent_query)
def get_all_by_user(user):
    """get persistent Query Keyword by user

    Args:
        user:
    """
    return PersistentQueryKeyword.get_all_by_user(user.id)
