from datetime import datetime, timedelta

import pytest

from .metrics import *
from .model import SiteCheckRecord

now = datetime.now().astimezone()


class TestDownTimeCalculation:
    def test_should_return_empty_downtimes_when_site_is_always_available(self):
        site_check_records = _create_record_for_status_codes([200] * 10)

        assert get_down_times(site_check_records) == []

    def test_should_return_empty_downtimes_when_no_record(self):
        assert get_down_times([]) == []

    def test_should_return_duration_for_single_downtime(self):
        status_codes = ([200] * 5) + [503, 502, 404, None] + ([200] * 2)

        site_check_records = _create_record_for_status_codes(status_codes)

        down_times = get_down_times(site_check_records)

        assert len(down_times) == 1
        assert down_times[0].from_time == site_check_records[8].check_time
        assert down_times[0].to_time == site_check_records[5].check_time

    def test_should_return_durations_for_multiple_downtimes(self):
        status_codes = (([200] * 2) + [503, 502] + ([200] * 2) + [None, 404] +
                        ([200] * 2))
        site_check_records = _create_record_for_status_codes(status_codes)

        down_times = get_down_times(site_check_records)

        assert len(down_times) == 2
        assert down_times[1].from_time == site_check_records[3].check_time
        assert down_times[1].to_time == site_check_records[2].check_time
        assert down_times[0].from_time == site_check_records[7].check_time
        assert down_times[0].to_time == site_check_records[6].check_time

    def test_should_return_current_time_as_downtime(self):
        status_codes = [503, 502, None, 404] + ([200] * 2)
        site_check_records = _create_record_for_status_codes(status_codes)

        down_times = get_down_times(site_check_records)

        assert len(down_times) == 1
        assert down_times[0].from_time == site_check_records[3].check_time
        assert down_times[0].to_time == site_check_records[0].check_time


class TestAvailabilityCalculation:
    def test_should_return_availability_as_100_when_site_never_down(self):
        status_codes = [200] * 10
        site_check_records = _create_record_for_status_codes(status_codes)

        availability = calculate_availability(site_check_records)

        assert availability == 100

    def test_should_return_availability_as_0_when_site_always_down(self):
        status_codes = [404] * 10
        site_check_records = _create_record_for_status_codes(status_codes)

        availability = calculate_availability(site_check_records)

        assert availability == 0

    def test_should_return_availability_as_96_43_when_site_down_for_1_minute_in_30_minutes(
        self):
        status_codes = ([200] * 10) + [404] * 2 + [200] * 18
        site_check_records = _create_record_for_status_codes(status_codes)

        availability = calculate_availability(site_check_records)

        assert availability == 96.43

    def test_should_return_none_when_no_records(self):
        assert calculate_availability([]) is None


class TestResponseTimeCalculation:
    def test_should_return_none_when_no_records(self):
        assert calculate_avg_response_time([]) is None

    def test_should_return_average_of_all_response_times(self):
        site_check_records = [
            _create_site_check_record(response_time=200),
            _create_site_check_record(response_time=100)
        ]

        assert calculate_avg_response_time(site_check_records) == 150

    def test_should_ignore_empty_response_times(self):
        site_check_records = [
            _create_site_check_record(response_time=200),
            _create_site_check_record(response_time=100),
            _create_site_check_record(response_time=None)
        ]

        assert calculate_avg_response_time(site_check_records) == 150


def _create_record_for_status_codes(
        status_codes: List[int]) -> List[SiteCheckRecord]:
    return [
        _create_site_check_record(status_code=status_codes[i - 1],
                                  check_time=(now - _minutes(i)))
        for i in range(1, len(status_codes))
    ]


def _create_site_check_record(status_code: int = 200,
                              check_time: datetime = now,
                              response_time: int = 200) -> SiteCheckRecord:
    return SiteCheckRecord(name="test",
                           url="test",
                           id=1,
                           site_id=1,
                           check_time=check_time,
                           http_status_code=status_code,
                           http_status_reason="mock",
                           response_time=response_time)


def _minutes(value: int) -> timedelta:
    return timedelta(minutes=value)
