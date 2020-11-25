import logging

logger = logging.getLogger(__name__)


class IngredientsException(Exception):
    pass


class Example(IngredientsException):
    pass
