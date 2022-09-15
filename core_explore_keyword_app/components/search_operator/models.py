""" Search Operator model
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import ModelError
from core_main_app.utils.validation.regex_validation import validate_alphanum
from core_main_app.utils.validation.xpath_validation import validate_xpath_list


class SearchOperator(models.Model):
    """Search Operator model"""

    name = models.CharField(
        blank=False, unique=True, validators=[validate_alphanum], max_length=200
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

    @staticmethod
    def get_all_xpath_list_except_xpath(operator_id):
        """Retrieve all xpath

        Args:

        Returns:
        """
        return (
            SearchOperator.objects.exclude(id=operator_id)
            .all()
            .values_list("xpath_list", flat=True)
        )

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
