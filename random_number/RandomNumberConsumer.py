import logging

logger = logging.getLogger(__name__)


def consume(message: str):
    logger.info("Consumed message: {message}".format(message=message))
