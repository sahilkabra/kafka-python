from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import jsonpickle


@dataclass
class Site:
    url: str
    name: str


@dataclass
class CheckResponse:
    site: Site
    status_code: Optional[int]
    time_taken: Optional[float]
    regex_matched: bool = False
    status_message: str = ""
    date: datetime = datetime.now().astimezone()

    def to_json(self) -> str:
        return jsonpickle.encode(self)

    @staticmethod
    def from_json(json: str):
        return jsonpickle.decode(json)


@dataclass
class CheckEntity:
    id: Optional[int]
    site_id: int
    check_time: datetime
    http_status_code: Optional[int]
    http_status_reason: str
    response_time: Optional[int]
