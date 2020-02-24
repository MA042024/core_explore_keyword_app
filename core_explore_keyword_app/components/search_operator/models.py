""" Search Operator model
"""
from django_mongoengine import fields, Document


class SearchOperator(Document):
    """ Search Operator model
    """
    name = fields.StringField(blank=False, unique=True)
    xpath_list = fields.ListField(blank=False, unique=True)
    dot_notation_list = fields.ListField(blank=False, unique=True)

    @staticmethod
    def get_all():
        """ Retrieve all search operators.

        Returns:
        """
        return SearchOperator.objects().all()

    @staticmethod
    def get_by_id(operator_id):
        """ Retrieve a search operator with a given id.

        Args:
            operator_id:

        Returns:
        """
        return SearchOperator.objects.get(pk=operator_id)

    @staticmethod
    def get_by_name(operator_name):
        """ Retrieve all search operators with a given name.

        Args:
            operator_name:

        Returns:
        """
        return SearchOperator.objects.get(name=operator_name)

    @staticmethod
    def get_by_dot_notation_list(operator_dot_notation_list):
        """ Retrieve all search operators with a given dot_notation list.

        Args:
            operator_dot_notation_list:

        Returns:
        """
        return SearchOperator.objects.get(dot_notation_list=operator_dot_notation_list)
