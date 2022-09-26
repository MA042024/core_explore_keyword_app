""" Admin forms for Search Operators.
"""
from django import forms
from django.forms import ModelForm

from core_main_app.commons import exceptions as core_main_app_exceptions
from core_main_app.utils.xml import validate_xpath
from core_explore_keyword_app.components.search_operator.models import (
    SearchOperator,
)
from core_explore_keyword_app.components.search_operator import (
    api as search_operator_api,
)


class SearchOperatorForm(ModelForm):
    """Main form to edit search operators."""

    document_id = forms.CharField(required=False, widget=forms.HiddenInput())
    xpath_list = forms.CharField(
        help_text="Enter one xpath per line.",
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "/path/to/xpath", "class": "form-control"}
        ),
    )

    class Meta:
        """Meta"""

        model = SearchOperator
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Operator name", "class": "form-control"}
            )
        }

    def clean_xpath_list(self):
        """Validate the list of xpath.

        Returns:
        """
        data = self.cleaned_data["xpath_list"].split("\n")
        line_xpath = 0

        for xpath in data:
            line_xpath += 1
            try:
                validate_xpath(xpath)
            except core_main_app_exceptions.XMLError as exception:
                raise forms.ValidationError(
                    "XPath syntax error (line %d): %s"
                    % (line_xpath, str(exception))
                )

        return self.cleaned_data["xpath_list"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.xpath_list = [
            xpath.strip()
            for xpath in self.cleaned_data["xpath_list"].split("\n")
        ]
        if commit:
            for xpath in instance.xpath_list:
                # check if xpath already exist
                if any(
                    xpath in sub_xpath_list
                    for sub_xpath_list in search_operator_api.get_all_xpath_except_xpath(
                        instance
                    )
                ):
                    raise core_main_app_exceptions.ApiError(
                        "Xpath already exists"
                    )
            return search_operator_api.upsert(instance)
        return instance
