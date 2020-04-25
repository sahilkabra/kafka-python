import unittest
import pytest

import site_status.check_process
from .model import CheckEntity, CheckResponse, Site

"""
@mock.patch("site_status.check_process.StatusRepository")
def test_success_response(mock_repository):
    response = CheckResponse(site=Site(name="test", url="url"), status_code=200, time_taken=0.023, status_message="ok")
    process(response)

    mock_repository.assert_called_with(

"""
