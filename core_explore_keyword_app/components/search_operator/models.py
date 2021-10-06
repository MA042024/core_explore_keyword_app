""" Search Operator model
"""
import re

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import ModelError
from core_main_app.utils.xml import validate_xpath


def validate_xpath_list(xpath_list):
    item_position = 0

    for xpath in xpath_list:
        try:
            validate_xpath(xpath)
            item_position += 1
        except exceptions.XMLError as e:
            raise ValidationError(
                "XPath syntax error (item #%d): %s" % (item_position, str(e))
            )


def validate_name(name):
    if re.match(r"^[a-zA-Z][a-zA-Z0-9]+$", name) is None:
        raise ValidationError("Name should only contains alpha-numerical characters.")


class SearchOperator(models.Model):
    """Search Operator model"""

    name = models.CharField(
        blank=False, unique=True, validators=[validate_name], max_length=200
    )
    xpath_list = models.JSONField(
        blank=False, unique=True, validators=[validate_xpath_list]
    )
    dot_notation_list = models.JSONField(blank=False, unique=True)

    @staticmethod
    def get_all():
        """Retrieve all search operators.

        Returns:
        """
        return SearchOperator.objects.all()

    @staticmethod
    def get_by_id(operator_id):
        """Retrieve a search operator with a given id.

        Args:
            operator_id:

        Returns:
        """
        try:
            return SearchOperator.objects.get(pk=operator_id)
        except ModelError as validation_error:
            raise exceptions.ModelError(str(validation_error))
        except ObjectDoesNotExist as does_not_exist:
            raise exceptions.DoesNotExist(str(does_not_exist))

    @staticmethod
    def get_by_name(operator_name):
        """Retrieve all search operators with a given name.

        Args:
            operator_name:

        Returns:
        """
        try:
            return SearchOperator.objects.get(name=operator_name)
        except ObjectDoesNotExist as does_not_exist:
            raise exceptions.DoesNotExist(str(does_not_exist))

    @staticmethod
    def get_by_dot_notation_list(operator_dot_notation_list):
        """Retrieve all search operators with a given dot_notation list.

        Args:
            operator_dot_notation_list:

        Returns:
        """
        try:
            return SearchOperator.objects.get(
                dot_notation_list=operator_dot_notation_list
            )
        except ObjectDoesNotExist as does_not_exist:
            raise exceptions.DoesNotExist(str(does_not_exist))

    def save_object(self):
        """Upsert a search operator and handle possible issues.

        Returns:
            SearchOperator
        """
        try:
            return self.save()
        except IntegrityError as not_unique_error:
            raise exceptions.NotUniqueError(str(not_unique_error))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    def __str__(self):
        """Search Operator object as string

        Returns:

        """
        return self.name
