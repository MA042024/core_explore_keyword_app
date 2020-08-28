""" Admin forms for Search Operators.
"""
from django import forms
from django_mongoengine.forms import DocumentForm
from core_main_app.utils.xml import validate_xpath
from core_main_app.commons import exceptions as core_main_app_exceptions

from core_explore_keyword_app.components.search_operator.models import SearchOperator


class SearchOperatorForm(DocumentForm):
    """Main form to edit search operators."""

    document_id = forms.CharField(required=False, widget=forms.HiddenInput())
    xpath_list = forms.CharField(
        help_text="Enter one xpath per line.",
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "/path/to/xpath", "class": "form-control"}
        ),
    )

    class Meta(object):
        document = SearchOperator
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
            except core_main_app_exceptions.XMLError as e:
                raise forms.ValidationError(
                    "XPath syntax error (line %d): %s" % (line_xpath, str(e))
                )

        return self.cleaned_data["xpath_list"]
