from dataclasses import dataclass
from typing import Optional

import jsonpickle


@dataclass
class CheckResponse:
    site_url: str
    status_code: Optional[int]
    time_taken: Optional[float]
    regex_matched: bool = False
    status_message: str = ""

    def to_json(self) -> str:
        return jsonpickle.encode(self)

    @staticmethod
    def from_json(json: str):
        return jsonpickle.decode(json)
