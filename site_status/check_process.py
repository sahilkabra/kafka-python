import logging
from typing import Optional

from .model import CheckEntity, CheckResponse, Site
from .repository import StatusRepository

logger = logging.getLogger(__name__)


def consume(message: str):
    logger.info("Received message {message}".format(message=message))
    process(CheckResponse.from_json(message))


def process(response: CheckResponse):
    try:
        repository = StatusRepository()
        repository.open_connection()
        site_id = repository.find_site_id(response.site.name)

        if site_id is None:
            site_id = repository.create_site_record(response.site.name,
                                                    response.site.url)

        logger.info("found site id {}".format(site_id))

        response_time: Optional[int] = None

        if response.time_taken is not None:
            response_time = round(response.time_taken * 1000)

        entity = CheckEntity(id=None,
                             site_id=site_id,
                             check_time=response.date,
                             http_status_code=response.status_code,
                             http_status_reason=response.status_message,
                             response_time=response_time)

        site_check_record = repository.create_site_check_record(entity)
        repository.commit()

        logger.info("created site check record {}".format(site_check_record))
    finally:
        repository.close()
