import logging

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ExampleSerializer

logger = logging.getLogger(__name__)


def log_request(func):
    def wrapper(self, request, *args, **kwargs):
        logger.debug("Example")
        return func(self, request, *args, **kwargs)

    return wrapper


class IngredientsView(APIView):
    def __init__(self):
        pass

    @log_request
    def get(self, request):
        return Response()

    @log_request
    def post(self, request):
        serializer = ExampleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response()
