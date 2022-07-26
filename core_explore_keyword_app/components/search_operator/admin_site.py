""" Custom admin site for the Search Operator model
"""
from django.contrib import admin


class CustomSearchOperatorAdmin(admin.ModelAdmin):
    """CustomSearchOperatorAdmin"""

    readonly_fields = ["xpath_list", "dot_notation_list"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Search Operators"""
        return False
