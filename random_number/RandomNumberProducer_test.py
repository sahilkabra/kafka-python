import pytest

from random_number import RandomNumberProducer


def test_should_generate_random_number():
    assert next(RandomNumberProducer.produce()) <= 10
