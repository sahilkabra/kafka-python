from typing import Optional

import httpretty
import pytest

from .check import check_site

uri = "http://test.example.com"


@httpretty.activate
def test_success_response():
    httpretty.register_uri(method=httpretty.GET,
                           uri=uri,
                           body="<html><body>Some content</body></html>")

    __test(200, True, expected_message="OK", regex="content")


@httpretty.activate
def test_not_found_response():
    httpretty.register_uri(method=httpretty.GET, uri=uri, status=404)

    __test(404, False, expected_message="Not Found")


@httpretty.activate
def test_regex_not_matched():
    httpretty.register_uri(method=httpretty.GET,
                           uri=uri,
                           body="<html><body>Some content</body></html>")

    __test(200, False, regex="should not be found", expected_message="OK")


@httpretty.activate
def test_site_down():
    __test(None,
           False,
           regex="not found",
           uri="http://invalid",
           expected_message="Name or service not known")


def __test(expected_status_code: Optional[int],
           expected_regex_match: bool,
           expected_message: str,
           regex: str = "",
           uri: str = uri):
    response = check_site(uri, regex)

    assert response.status_code == expected_status_code
    assert response.regex_matched == expected_regex_match
    assert expected_message in response.status_message
