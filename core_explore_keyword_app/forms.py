""" Explore by Keyword forms
"""
from django import forms


class KeywordForm(forms.Form):
    """
    Search by Keyword form
    """
    keywords = forms.CharField(widget=forms.TextInput())
    query_id = forms.CharField(widget=forms.HiddenInput())
