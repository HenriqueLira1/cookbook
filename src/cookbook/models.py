import enum

from django.db import models


class EnumChoices(enum.Enum):
    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]

    def __repr__(self):
        return f"{self.name} = {self.value}"

    def __str__(self):
        return self.value


class DbEnumField(models.Field):
    """PosgreSQL ENUM base field.
    Expects to be inherited by some class implementing a Meta class.
    """

    def __init__(self, *args, **kwargs):
        kwargs["choices"] = self.Meta.enum.choices()
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return self.Meta.db_type_name

    def get_prep_value(self, value, **kwargs):
        if isinstance(value, str) or value is None:
            return value

        return value.value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None

        return self.Meta.enum(value)
