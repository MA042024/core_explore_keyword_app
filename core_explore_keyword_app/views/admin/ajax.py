""" Ajax views for core_explore_keyword_app
"""
from django.contrib import messages
from django.core.exceptions import NON_FIELD_ERRORS
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from core_explore_keyword_app.components.search_operator import (
    api as search_operator_api,
)
from core_explore_keyword_app.views.admin.forms import SearchOperatorForm
from core_main_app.commons.exceptions import ApiError


class SearchOperatorConfigModalView(View):
    """View for saving the configuration of a search operator"""

    @staticmethod
    def post(request):
        """Method called after editing or creating a search operator.

        Args:
            request:

        Returns:
        """
        instance = None
        action = "created"
        if "document_id" in request.POST and request.POST["document_id"] != "":
            action = "edited"
            instance = search_operator_api.get_by_id(request.POST["document_id"])

        operator_form = SearchOperatorForm(request.POST, instance=instance)

        if not operator_form.is_valid():
            return render(
                request,
                "core_explore_keyword_app/admin/search_ops_manager/modal/config/form.html",
                context={"form": operator_form},
            )

        try:
            operator_form.save()
        except ApiError as exception:
            operator_form.add_error(NON_FIELD_ERRORS, str(exception))
            return render(
                request,
                "core_explore_keyword_app/admin/search_ops_manager/modal/config/form.html",
                context={"form": operator_form},
            )

        messages.add_message(
            request, messages.SUCCESS, "Operator successfully %s!" % action
        )

        return JsonResponse({})

    @staticmethod
    def get(request):
        """Method called after editing a search operator.

        Args:
            request:

        Returns:
        """
        try:

            operator = search_operator_api.get_by_id(request.GET["document_id"])
            xpath_list = "\n".join(operator.xpath_list)
            operator_form = SearchOperatorForm(
                initial={"xpath_list": xpath_list, "document_id": operator.id},
                instance=operator,
            )

            return render(
                request,
                "core_explore_keyword_app/admin/search_ops_manager/modal/config/form.html",
                context={"form": operator_form},
            )
        except ApiError as exception:
            messages.add_message(
                request, messages.ERROR, "Failed to find operator: %s." % str(exception)
            )


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

        except ApiError as exception:
            messages.add_message(
                request,
                messages.ERROR,
                "Failed to delete operator: %s." % str(exception),
            )
            return JsonResponse({}, status=500)
