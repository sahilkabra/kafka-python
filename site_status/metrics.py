import logging
from typing import List

from .model import CheckEntity, CheckResponse, Site
from .repository import StatusRepository


def log_metrics(site_name: str):
    logging.info("metrics for {}".format(site_name))
    try:
        with StatusRepository.open_connection() as connection:
            site_check_records = StatusRepository.find_site_check_records(
                connection, site_name)
            log_uptime(site_check_records)
    finally:
        if connection.closed == 0:
            connection.close()


def log_uptime(site_check_records: List[CheckEntity]):
    logging.info("uptime")

    for check in site_check_records:
        logging.info("check {}".format(str(check)))
