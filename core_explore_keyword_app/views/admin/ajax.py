""" Ajax views for core_explore_keyword_app
"""
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from mongoengine.base import NON_FIELD_ERRORS

from core_explore_keyword_app.components.search_operator import (
    api as search_operator_api,
)
from core_explore_keyword_app.components.search_operator.models import SearchOperator
from core_explore_keyword_app.views.admin.forms import SearchOperatorForm
from core_main_app.commons.exceptions import ApiError


class SearchOperatorConfigModalView(View):
    """View for saving the configuration of a search operator"""

    @staticmethod
    def post(request):
        """Method called after editing a search operator.

        Args:
            request:

        Returns:
        """
        operator_form = SearchOperatorForm(request.POST)

        if not operator_form.is_valid():
            return render(
                request,
                "core_explore_keyword_app/admin/search_ops_manager/modal/config/form.html",
                context={"form": operator_form},
            )
        else:
            action = "created"

            xpath_list = [
                xpath.strip()
                for xpath in operator_form.cleaned_data["xpath_list"].split("\n")
            ]

            operator = SearchOperator(
                name=operator_form.cleaned_data["name"], xpath_list=xpath_list
            )

            if "document_id" in request.POST and request.POST["document_id"] != "":
                operator.pk = operator_form.cleaned_data["document_id"]
                action = "edited"

            try:
                search_operator_api.upsert(operator)
            except ApiError as e:
                operator_form.add_error(NON_FIELD_ERRORS, str(e))
                return render(
                    request,
                    "core_explore_keyword_app/admin/search_ops_manager/modal/config/form.html",
                    context={"form": operator_form},
                )

            messages.add_message(
                request, messages.SUCCESS, "Operator successfully %s!" % action
            )

            return JsonResponse({})


class SearchOperatorDeleteModalView(View):
    """View for deleting a search operator"""

    @staticmethod
    def post(request):
        """Method called after confirmation of the deletion of a search operator.

        Args:
            request:

        Returns:
        """
        if "id" not in request.POST:
            messages.add_message(request, messages.ERROR, "Invalid delete request.")
            return JsonResponse({}, status=400)

        try:
            operator = search_operator_api.get_by_id(request.POST["id"])
            search_operator_api.delete(operator)

            messages.add_message(
                request, messages.INFO, "Operator %s deleted." % operator.name
            )
            return JsonResponse({}, status=200)
        except ApiError as e:
            messages.add_message(
                request, messages.ERROR, "Failed to delete operator: %s." % str(e)
            )
            return JsonResponse({}, status=500)
