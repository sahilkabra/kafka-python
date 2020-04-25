from typing import Optional
from dataclasses import dataclass
import requests
import re
import logging

logger = logging.getLogger(__name__)


def check_site(url: str, pattern: str):
    try:
        logger.info("checking {site} for availability".format(site=url))
        response = requests.get(url, timeout=5)

        status_code = response.status_code
        status_message = response.reason
        time_taken = response.elapsed.total_seconds()

        match_found = False

        if status_code == requests.codes.ok:
            match_found = re.search(pattern, response.text) != None

        response.close()

        logger.info(
            "{site}: status: {code} message: {message} regex_match: {match}".
            format(site=url,
                   code=status_code,
                   message=status_message,
                   match=match_found))

        return CheckResponse(status_code=status_code,
                             status_message=status_message,
                             time_taken=time_taken,
                             regex_matched=match_found)

    except requests.Timeout as ex:

        return CheckResponse(status_code=None,
                             status_message="Timeout",
                             time_taken=ex.response.elapsed.total_seconds,
                             regex_matched=False)

    except requests.RequestException as ex:

        return CheckResponse(
            status_code=ex.response.status_code if ex.response else None,
            status_message=str(ex.args[0]),
            time_taken=None,
            regex_matched=False)


@dataclass
class CheckResponse:
    status_code: Optional[int]
    time_taken: Optional[float]
    regex_matched: bool = False
    status_message: str = ""
