""" REST views for the search operators.
"""
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions
from core_main_app.utils.decorators import api_staff_member_required
import core_explore_keyword_app.components.search_operator.api as search_operator_api
from core_explore_keyword_app.rest.search_operators.serializers import (
    SearchOperatorSerializer,
)


class SearchOperatorList(APIView):
    """List search operators"""

    def get(self, request):
        """Get all search operators

        Args:
            request: HTTP request

        Returns:

            - code: 200
              content: List of search operators
            - code: 500
              content: Internal server error
        """
        try:
            search_operator_list = search_operator_api.get_all()

            # Serialize object
            serializer = SearchOperatorSerializer(
                search_operator_list, many=True
            )

            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @method_decorator(api_staff_member_required())
    def post(self, request):
        """Create a search operator

        Parameters:
            {
                "name": "search_operator_name",
                "xpath_list": ["/x/path/one", "/x/path/two"],
            }

        Args:
            request: HTTP request

        Returns:

            - code: 201
              content: Created search operator
            - code: 400
              content: Validation error / not unique / model error
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializer
            serializer = SearchOperatorSerializer(data=request.data)

            # Validate data
            serializer.is_valid(raise_exception=True)

            # Save data
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.ModelError as model_exception:
            content = {"message": str(model_exception)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.NotUniqueError as not_unique_error:
            content = {"message": str(not_unique_error)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as key_error:
            content = {"message": str(key_error)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.ApiError as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as exception:
            content = {"message": str(exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SearchOperatorDetail(APIView):
    """Search operator detail"""

    def get(self, request, pk):
        """Retrieve search operator from database

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:
            SearchOperator
        """
        try:
            # Get object
            search_operator = search_operator_api.get_by_id(pk)

            # Serialize object
            serializer = SearchOperatorSerializer(search_operator)

            # Return response
            return Response(serializer.data)
        except exceptions.DoesNotExist:
            content = {"message": "Search operator not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @method_decorator(api_staff_member_required())
    def patch(self, request, pk):
        """Update a search operator

        Parameters:
            {
                "name": "new_name",
                "xpath_list": ["/x/path/one/new", "/x/path/two/new"]
            }

        Args:
            request: HTTP request
            pk: ObjectId

        Returns:
            - code: 200
              content: Updated data
            - code: 400
              content: Validation error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            search_operator = search_operator_api.get_by_id(pk)

            # Build serializer
            search_operator_serializer = SearchOperatorSerializer(
                instance=search_operator, data=request.data, partial=True
            )

            # Validate and save search operator
            search_operator_serializer.is_valid(raise_exception=True)
            search_operator_serializer.save()

            return Response(
                search_operator_serializer.data, status=status.HTTP_200_OK
            )
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = {"message": "Search operator not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @method_decorator(api_staff_member_required())
    def delete(self, request, pk):
        """Delete a search operator

        Args:
            request: HTTP request
            pk: ObjectId

        Returns:
            - code: 204
              content: Deletion success
            - code: 403
              content: Authentication error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            search_operator = search_operator_api.get_by_id(pk)

            # delete object
            search_operator_api.delete(search_operator)

            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except exceptions.DoesNotExist:
            content = {"message": "Workspace not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
