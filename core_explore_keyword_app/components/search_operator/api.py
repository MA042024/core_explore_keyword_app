""" Search Operator API
"""
from core_main_app.commons import exceptions
from core_main_app.utils.xml import xpath_to_dot_notation
from core_explore_keyword_app.components.search_operator.models import (
    SearchOperator,
)


def get_all():
    """Return all the Search Operator.

    Returns:
    """
    return SearchOperator.get_all()


def get_by_id(operator_id):
    """Return the Search Operator with the given id.

    Args:
        operator_id:

    Returns:
    """
    try:
        return SearchOperator.get_by_id(operator_id)
    except exceptions.ModelError:
        raise exceptions.ApiError("Invalid operator ID")
    except exceptions.DoesNotExist:
        raise exceptions.ApiError("Operator does not exist")


def get_by_name(operator_name):
    """Return the Search Operator with the given name.

    Args:
        operator_name:

    Returns:
    """
    try:
        return SearchOperator.get_by_name(operator_name)
    except exceptions.DoesNotExist:
        raise exceptions.ApiError("Operator does not exist")


def get_by_dot_notation_list(dot_notation_list):
    """Return the Search Operator with the given dot_notation list.

    Args:
        dot_notation_list:

    Returns:
    """
    try:
        return SearchOperator.get_by_dot_notation_list(dot_notation_list)
    except exceptions.DoesNotExist:
        raise exceptions.ApiError("Operator does not exist")


def get_all_xpath_except_xpath(operator):
    """Return the Search Operator with the given dot_notation list.

    Args:

    Returns:
    """
    return SearchOperator.get_all_xpath_list_except_xpath(operator.id)


def upsert(operator):
    """Save or update a Search Operator.

    Args:
        operator:

    Returns:

    """

    try:
        # Create the dot notation list automatically from the XPath list
        operator.dot_notation_list = [
            xpath_to_dot_notation(xpath) for xpath in operator.xpath_list
        ]

        operator.save_object()
        return operator
    except exceptions.NotUniqueError:
        raise exceptions.ApiError("Operator name or xpath already exists")
    except exceptions.ModelError as model_error:
        raise exceptions.ApiError("Model save failed: %s" % str(model_error))


def delete(operator):
    """Delete a Search Operator.

    Args:
        operator:

    Returns:

    """
    return operator.delete()
