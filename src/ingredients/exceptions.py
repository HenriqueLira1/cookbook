import logging

logger = logging.getLogger("ingredients.exceptions")


class IngredientsException(Exception):
    pass


class Example(IngredientsException):
    pass
