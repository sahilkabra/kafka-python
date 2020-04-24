import random
from typing import Iterator


def produce() -> int:
    return random.randint(5, 10)
