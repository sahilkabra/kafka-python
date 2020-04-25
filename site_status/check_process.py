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
        with StatusRepository.open_connection() as connection:
            site_id = StatusRepository.find_site_id(connection,
                                                    response.site.name)

            if site_id is None:
                site_id = StatusRepository.create_site_record(
                    connection, response.site.name, response.site.url)

            assert site_id is not None
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

            site_check_record = StatusRepository.create_site_check_record(
                connection, entity)

            connection.commit()

            assert site_check_record is not None
            logger.info("created site check record {} for {}".format(
                site_check_record.id, response.site.name))

    finally:
        if connection.closed == 0:
            connection.close()
