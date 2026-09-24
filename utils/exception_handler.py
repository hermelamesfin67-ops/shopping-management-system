from rest_framework.views import exception_handler
from rest_framework.response import Response

from .exceptions import BaseAppException


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if isinstance(exc, BaseAppException):
        return Response(
            {
                "error": str(exc)
            },
            status=exc.status_code
        )

    return response
