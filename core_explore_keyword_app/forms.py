""" Explore by Keyword forms
"""
from django import forms

from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)


class KeywordForm(forms.Form):
    """
    Search by Keyword form
    """

    keywords = forms.CharField(widget=forms.TextInput(), required=False)
    query_id = forms.CharField(widget=forms.HiddenInput())
    user_id = forms.CharField(widget=forms.HiddenInput())
    global_templates = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(), required=False
    )
    user_templates = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(), required=False
    )
    order_by_field = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        """Init Keyword form"""
        request = kwargs.pop("request")
        super(KeywordForm, self).__init__(*args, **kwargs)

        # initialize template filters
        global_templates = [
            (template_version_manager.id, template_version_manager.title)
            for template_version_manager in template_version_manager_api.get_active_global_version_manager(
                request=request
            )
        ]
        user_templates = [
            (template_version_manager.id, template_version_manager.title)
            for template_version_manager in template_version_manager_api.get_active_version_manager_by_user_id(
                request=request
            )
        ]
        self.fields["global_templates"].choices = global_templates
        self.fields["user_templates"].choices = user_templates
