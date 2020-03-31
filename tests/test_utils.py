import pytest
from covid19.utils import fresh_pin, gen_token


def test_pin():
    p = fresh_pin()
    assert p


def test_token():
    pin = fresh_pin()
    email = 'sbk@sbk.sbk'
    t = gen_token(email, pin)
    assert t