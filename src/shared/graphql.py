from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import serializers

import graphene
from graphene.types.mutation import MutationOptions
from graphql_jwt.decorators import login_required

from . import exceptions


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
            raise exceptions.SerializerMutationMetaAttrException(
                attribute="serializer_class"
            )

        if not model_operation:
            raise exceptions.SerializerMutationMetaAttrException(
                attribute="model_operation"
            )

        if model_class is None:
            serializer_meta = getattr(serializer_class, "Meta", None)
            if serializer_meta:
                model_class = getattr(serializer_meta, "model", None)

        if not model_class and model_operation in ["update", "delete"]:
            raise exceptions.SerializerMutationMetaAttrException(
                attribute="model_class"
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
