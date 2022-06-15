from time import sleep

import pytest

import pendulum

from pendulum.utils._compat import PYPY


@pytest.fixture(autouse=True)
def setup():
    pendulum.travel_back()

    yield

    pendulum.travel_back()


@pytest.mark.skipif(PYPY, reason="Time travelling not available on PyPy")
def test_travel():
    now = pendulum.now()

    pendulum.travel(minutes=5)

    assert pendulum.now().diff_for_humans(now) == "5 minutes after"


@pytest.mark.skipif(PYPY, reason="Time travelling not available on PyPy")
def test_travel_with_frozen_time():
    pendulum.travel(minutes=5, freeze=True)

    now = pendulum.now()

    sleep(0.01)

    assert now == pendulum.now()


@pytest.mark.skipif(PYPY, reason="Time travelling not available on PyPy")
def test_travel_to():
    dt = pendulum.datetime(2022, 1, 19, tz="local")

    pendulum.travel_to(dt)

    assert pendulum.now().date() == dt.date()


@pytest.mark.skipif(PYPY, reason="Time travelling not available on PyPy")
def test_freeze():
    pendulum.freeze()

    pendulum.travel(minutes=5)

    assert pendulum.now() == pendulum.now()

    pendulum.travel_back()

    pendulum.travel(minutes=5)

    assert pendulum.now() != pendulum.now()

    pendulum.freeze()

    assert pendulum.now() == pendulum.now()

    pendulum.travel_back()

    with pendulum.freeze():
        assert pendulum.now() == pendulum.now()

    assert pendulum.now() != pendulum.now()
