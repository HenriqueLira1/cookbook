import pytest

from rest_framework import serializers


def assert_exception_raised(serializer, field):
    with pytest.raises(serializers.ValidationError) as exception:
        serializer.is_valid(raise_exception=True)

    assert_exception_has_only_one_error(exception, field)


def assert_exception_has_only_one_error(exception, attribute):
    assert attribute in exception.value.args[0]
    assert 1 == len(exception.value.args[0])
