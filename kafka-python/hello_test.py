import pytest
from hello import HelloSayer


def test_hello():
  assert HelloSayer().say_hello("x") == "hello x"

