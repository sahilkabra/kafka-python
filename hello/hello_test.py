import pytest

from hello.hello import HelloSayer


def test_hello():
    assert HelloSayer().say_hello("name") == "hello name"
