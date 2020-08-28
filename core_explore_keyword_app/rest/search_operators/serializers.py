""" Serializers used for the search operator REST API.
"""
from rest_framework_mongoengine.serializers import DocumentSerializer

from core_explore_keyword_app.components.search_operator import (
    api as search_operator_api,
)
from core_explore_keyword_app.components.search_operator.models import SearchOperator


class SearchOperatorSerializer(DocumentSerializer):
    """Search operator serializer"""

    class Meta(object):
        model = SearchOperator
        fields = ["id", "name", "xpath_list"]
        read_only_fields = ("id",)

    def create(self, validated_data):
        """Create and return a new `SearchOperator` instance, given the validated data."""
        # Create instance from the validated data and insert it in DB
        instance = SearchOperator(
            name=validated_data["name"], xpath_list=validated_data["xpath_list"]
        )
        search_operator_api.upsert(instance)

        return instance

    def update(self, instance, validated_data):
        """Update and return an existing `SearchOperator` instance, given the validated
        data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.xpath_list = validated_data.get("xpath_list", instance.xpath_list)
        return search_operator_api.upsert(instance)
