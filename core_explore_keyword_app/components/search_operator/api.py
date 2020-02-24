""" Search Operator API
"""
from mongoengine import errors as mongoengine_errors
from pymongo import errors as pymongo_errors

from core_explore_keyword_app.components.search_operator.models import SearchOperator
from core_main_app.commons.exceptions import ApiError
from core_main_app.utils.xml import xpath_to_dot_notation


def get_all():
    """ Return all the Search Operator.

    Returns:
    """
    return SearchOperator.get_all()


def get_by_id(operator_id):
    """ Return the Search Operator with the given id.

    Args:
        operator_id:

    Returns:
    """
    try:
        return SearchOperator.get_by_id(operator_id)
    except mongoengine_errors.ValidationError:
        raise ApiError("Invalid operator ID")
    except mongoengine_errors.DoesNotExist:
        raise ApiError("Operator does not exist")


def get_by_name(operator_name):
    """ Return the Search Operator with the given name.

    Args:
        operator_name:

    Returns:
    """
    try:
        return SearchOperator.get_by_name(operator_name)
    except mongoengine_errors.DoesNotExist:
        raise ApiError("Operator does not exist")


def get_by_dot_notation_list(dot_notation_list):
    """ Return the Search Operator with the given dot_notation list.

    Args:
        dot_notation_list:

    Returns:
    """
    try:
        return SearchOperator.get_by_dot_notation_list(dot_notation_list)
    except mongoengine_errors.DoesNotExist:
        raise ApiError("Operator does not exist")


def upsert(operator):
    """ Save or update a Search Operator.

    Args:
        operator:

    Returns:

    """
    try:
        # Create the dot notation list automatically from the XPath list
        operator.dot_notation_list = [
            xpath_to_dot_notation(xpath)
            for xpath in operator.xpath_list
        ]

        return operator.save()
    except pymongo_errors.DuplicateKeyError:
        raise ApiError("Operator named %s already exists" % operator.name)


def delete(operator):
    """ Delete a Search Operator.

    Args:
        operator:

    Returns:

    """
    return operator.delete()
