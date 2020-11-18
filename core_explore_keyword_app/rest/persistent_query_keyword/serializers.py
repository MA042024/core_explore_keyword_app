""" Serializers used for the persistent query keyword REST API.
"""
from rest_framework_mongoengine.serializers import DocumentSerializer

from core_explore_keyword_app.components.persistent_query_keyword import (
    api as persistent_query_keyword_api,
)
from core_explore_keyword_app.components.persistent_query_keyword.models import (
    PersistentQueryKeyword,
)


class PersistentQueryKeywordSerializer(DocumentSerializer):
    """persistent query keyword serializer"""

    class Meta(object):
        model = PersistentQueryKeyword
        fields = ["id", "user_id", "content", "templates", "name"]
        read_only_fields = ("id", "user_id")

    def create(self, validated_data):
        """Create and return a new `PersistentQueryKeyword` instance, given the validated data."""
        # Create instance from the validated data and insert it in DB
        persistent_query_keyword = PersistentQueryKeyword(
            user_id=str(self.context["request"].user.id),
            content=validated_data["content"] if "content" in validated_data else None,
            templates=validated_data["templates"]
            if "templates" in validated_data
            else None,
            name=validated_data["name"] if "name" in validated_data else None,
        )
        return persistent_query_keyword_api.upsert(
            persistent_query_keyword, self.context["request"].user
        )

    def update(self, persistent_query_keyword, validated_data):
        """Update and return an existing `PersistentQueryKeyword` instance, given the validated
        data.
        """
        persistent_query_keyword.content = validated_data.get(
            "content", persistent_query_keyword.content
        )
        persistent_query_keyword.templates = validated_data.get(
            "templates", persistent_query_keyword.templates
        )
        persistent_query_keyword.name = validated_data.get(
            "name", persistent_query_keyword.name
        )
        return persistent_query_keyword_api.upsert(
            persistent_query_keyword, self.context["request"].user
        )


class PersistentQueryKeywordAdminSerializer(DocumentSerializer):
    """PersistentQueryKeyword Serializer"""

    class Meta(object):
        """Meta"""

        model = PersistentQueryKeyword
        fields = ["id", "user_id", "content", "templates", "name"]

    def create(self, validated_data):
        """
        Create and return a new `PersistentQueryKeyword` instance, given the validated data.
        """
        # Create data
        persistent_query_keyword = PersistentQueryKeyword(
            user_id=validated_data["user_id"],
            content=validated_data["content"] if "content" in validated_data else None,
            templates=validated_data["templates"]
            if "templates" in validated_data
            else None,
            name=validated_data["name"] if "name" in validated_data else None,
        )
        return persistent_query_keyword_api.upsert(
            persistent_query_keyword, self.context["request"].user
        )
