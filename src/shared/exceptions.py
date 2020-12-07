import logging

logger = logging.getLogger(__name__)


class SerializerMutationMetaAttrException(Exception):
    def __init__(self, attribute: str):
        message = f"{attribute} is required for the SerializerMutation"

        logger.critical(message, exc_info=True)
        super().__init__(message)
