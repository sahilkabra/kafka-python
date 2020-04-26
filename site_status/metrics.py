import logging
from datetime import datetime
from typing import List, Optional
from functools import reduce

from .model import DownTime, SiteCheckRecord
from .repository import StatusRepository

logger = logging.getLogger(__name__)

site_down_status_codes = [404, 408, 410, 503, 502, 598, 599, None]
datetime_format = "%Y-%m-%d %H:%M (%Z)"


def log_metrics(site_name: str):
    logger.info(f"metrics for {site_name}")

    try:
        with StatusRepository.open_connection() as connection:
            site_check_records = StatusRepository.find_site_check_records(
                connection, site_name)
    finally:
        if connection.closed == 0:
            connection.close()

    availability = calculate_availability(site_check_records)
    avg_response_time = calculat_avg_response_time(site_check_records)
    downtimes = get_down_times(site_check_records)

    logger.info(f"availability: {availability}")

    if downtimes:
        logger.info("site downtimes:")

    for d in downtimes:
        logger.info(
            f"from: {d.from_time.strftime(datetime_format)} to: {d.to_time.strftime(datetime_format)}"
        )


def calculate_availability(
        site_check_records: List[SiteCheckRecord]) -> Optional[float]:
    logging.info("availability")

    if len(site_check_records) == 0:
        return None

    sorted_records = _sort(site_check_records)

    downtime = 0.0
    for d in get_down_times(sorted_records):
        downtime += d.duration()

    check_duration = (sorted_records[-1].check_time -
                      sorted_records[0].check_time)

    return 100 - round(((downtime / check_duration.total_seconds()) * 100), 2)


def calculat_avg_response_time(site_check_records: List[SiteCheckRecord]):
    logging.info("response time")


def get_down_times(
        site_check_records: List[SiteCheckRecord]) -> List[DownTime]:
    down_times = []
    from_time: Optional[datetime] = None
    to_time: Optional[datetime] = None

    for r in _sort(site_check_records):
        if r.http_status_code in site_down_status_codes:
            if from_time is None:
                from_time = r.check_time
            else:
                to_time = r.check_time
        if r.http_status_code not in site_down_status_codes and from_time is not None and to_time is not None:
            down_times.append(DownTime(from_time=from_time, to_time=to_time))
            from_time = None
            to_time = None

    # if the latest record also is DOWN, then the site is currently down
    if from_time is not None and to_time is not None:
        down_times.append(DownTime(from_time=from_time, to_time=to_time))

    return down_times


def _sort(records: List[SiteCheckRecord]) -> List[SiteCheckRecord]:
    return sorted(records, key=lambda x: x.check_time)
