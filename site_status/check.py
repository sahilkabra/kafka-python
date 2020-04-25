import logging
import re

import requests

from .model import (CheckResponse, Site)

logger = logging.getLogger(__name__)


def check_site(site: Site, pattern: str) -> CheckResponse:
    try:
        logger.info("checking {site} for availability".format(site=site.url))
        response = requests.get(site.url, timeout=5)

        status_code = response.status_code
        status_message = response.reason
        time_taken = response.elapsed.total_seconds()

        match_found = False

        if status_code == requests.codes.ok:
            match_found = re.search(pattern, response.text) != None

        response.close()

        logger.info(
            "{site}: status: {code} message: {message} regex_match: {match}".
            format(site=site.name,
                   code=status_code,
                   message=status_message,
                   match=match_found))

        return CheckResponse(site=site,
                             status_code=status_code,
                             status_message=status_message,
                             time_taken=time_taken,
                             regex_matched=match_found)

    except requests.Timeout as ex:

        return CheckResponse(site=site,
                             status_code=None,
                             status_message="Timeout",
                             time_taken=None,
                             regex_matched=False)

    except requests.RequestException as ex:

        return CheckResponse(
            site=site,
            status_code=ex.response.status_code if ex.response else None,
            status_message=str(ex.args[0]),
            time_taken=None,
            regex_matched=False)
