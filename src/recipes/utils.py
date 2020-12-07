# from graphene_django.rest_framework.mutation import SerializerMutation
import logging

from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import serializers

# from .exceptions import Example
import graphene
from graphene.types.mutation import MutationOptions
from graphql_jwt.decorators import login_required

# import time


logger = logging.getLogger(__name__)


class MutationOptions(MutationOptions):
    model_class = None  # type: models.Model
    serilizer_class = None  # type: serializers.Serializer
    model_operation = None  # type: str


class SerializerMutation(graphene.Mutation):
    @classmethod
    def __init_subclass_with_meta__(
        cls,
        model_class=None,
        serializer_class=None,
        model_operation=None,
        _meta=None,
        **options
    ):
        if not _meta:
            _meta = MutationOptions(cls)

        if not serializer_class:
            raise Exception("serializer_class is required for the SerializerMutation")

        if not model_operation:
            raise Exception("model_operation is required for the SerializerMutation")

        if model_class is None:
            serializer_meta = getattr(serializer_class, "Meta", None)
            if serializer_meta:
                model_class = getattr(serializer_meta, "model", None)

        if not model_class and model_operation in ["update", "delete"]:
            raise Exception(
                "model_class is required for the update and delete operations"
            )

        _meta.model_class = model_class
        _meta.serializer_class = serializer_class
        _meta.model_operation = model_operation
        super().__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        perform_operation = {
            "create": cls._preform_create,
            "update": cls._preform_update,
            "delete": cls._preform_delete,
        }.get(cls._meta.model_operation)

        return perform_operation(**kwargs)

    @classmethod
    def _preform_create(cls, input):
        serializer = cls._meta.serializer_class(data=input)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @classmethod
    def _preform_update(cls, input):
        instance = get_object_or_404(cls._meta.model_class, pk=input.get("id"))
        serializer = cls._meta.serializer_class(instance, data=input, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @classmethod
    def _preform_delete(cls, id):
        instance = get_object_or_404(cls._meta.model_class, pk=id)
        instance.delete()

        return instance


# TASK_NOT_FOUND_RETRY_CONFIG = {
#     "times": 1,
#     "incremental_wait": 0.1,
#     "on_exceptions": (Example,),
# }

# def retry(times, incremental_wait, on_exceptions):
#     """retry decorator:
#     - Retries the given func if any of {on_exceptions} happens
#     - It will retry the execution until {times} times, so, in the worse case,
#         it will run the func {times+1} times.
#     - Every time that retry the execution will wait an incremental of
#         {incremental_wait}. I.E: incremental_wait = 0.3sec, so it will wait 0.3s
#         in the first time, 0.6s in the second, 0.9s in the third and goes on...
#     """

#     def decorator(function):
#         def wrapper(*args, **kwargs):
#             return execute_recursively(1, *args, **kwargs)

#         def execute_recursively(count, *args, **kwargs):
#             try:
#                 return function(*args, **kwargs)
#             except on_exceptions:
#                 if count <= times:
#                     logger.warning(
#                         "Retrying failed function\n"
#                         f"Function: {function.__name__}\n"
#                         f"Counter: {count} out of {times}",
#                         exc_info=True,
#                     )
#                     time.sleep(incremental_wait * count)
#                     return execute_recursively(count + 1, *args, **kwargs)
#                 else:
#                     raise
#             else:
#                 logger.debug(f"Function: {function.__name__} succeeded")

#         return wrapper

#     return decorator
