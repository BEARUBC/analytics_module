import contextlib
import time
from collections import OrderedDict
from collections.abc import Callable, Generator
from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict


class StartAndEnd(BaseModel):
    model_config = ConfigDict(frozen=True)

    start: datetime
    end: datetime

    @property
    def elapsed(self) -> timedelta:
        return self.end - self.start


@contextlib.contextmanager
def timer() -> Generator[Callable[[], float], None, None]:
    """
    Contextmanager function that will return the seconds elapsed since the initial call to timer()

    :return: Lambda yielding time elapsed (in seconds) since initial call to timer()
    """
    start = time.perf_counter()
    yield lambda: (time.perf_counter() - start)


@contextlib.contextmanager
def timer_ms() -> Generator[Callable[[], float], None, None]:
    """
    Contextmanager function that will return the milliseconds elapsed since the initial call to timer_ms()

    :return: Lambda yielding time elapsed (in milliseconds) since initial call to timer_ms()
    """
    with timer() as t:
        yield lambda: t() * 1000


@contextlib.contextmanager
def stopwatch() -> Generator[Callable[[], float], None, None]:
    """
    Contextmanager yielding a lambda that will return the seconds elapsed since either the
    last call to the lambda, or the initial call to stopwatch()

    :return: Lambda yielding time elapsed (in seconds) between last invocation and current invocation
    """
    start = time.perf_counter()

    def delta() -> float:
        nonlocal start
        end = time.perf_counter()
        d = end - start
        start = end
        return d

    yield lambda: delta()


@contextlib.contextmanager
def stopwatch_ms() -> Generator[Callable[[], float], None, None]:
    """
    Contextmanager yielding a lambda that will return the milliseconds elapsed since either the
    last call to the lambda, or the initial call to stopwatch_ms()

    :return: Lambda yielding time elapsed (in milliseconds) between last invocation and current invocation
    """
    with stopwatch() as s:
        yield lambda: s() * 1000


@contextlib.contextmanager
def multitimer() -> (
    Generator[tuple[Callable[[], float], Callable[[], float]], None, None]
):
    """
    Contextmanager yielding a union of both timer() and stopwatch(). Useful for instrumenting situations where
    we need both the total elapsed wall-clock time and a more detailed breakdown

    :return: (timer() lambda, stopwatch() lambda)
    """
    with timer() as t:
        with stopwatch() as s:
            yield t, s


@contextlib.contextmanager
def multitimer_ms() -> (
    Generator[tuple[Callable[[], float], Callable[[], float]], None, None]
):
    """
    Contextmanager yielding a union of both timer_ms() and stopwatch_ms(). Useful for instrumenting situations where
    we need both the total elapsed wall-clock time and a more detailed breakdown

    :return: (timer_ms() lambda, stopwatch_ms() lambda)
    """
    with timer_ms() as t:
        with stopwatch_ms() as s:
            yield t, s


class TimerStats(OrderedDict[str, float]):
    """
    Very simple helper class that acts as an OrderedDict[str, float] (preserving insertion order).
    The summary() function will print all of the dict entries in the form "k1=v1 k2=v2" (etc)
    """

    def summary(self) -> str:
        return " ".join([f"{k}={v:.2f}" for k, v in self.items()])


@contextlib.contextmanager
def start_and_end() -> Generator[Callable[[], StartAndEnd], None, None]:
    """
    Contextmanager yielding a function that computes a tuple of:
        * time context manager was entered
        * time of function evaluation

    :return: Function yielding a tuple of (start utcnow time, current utcnow time)
    """
    start = datetime.utcnow()

    def _delta() -> StartAndEnd:
        nonlocal start
        end = datetime.utcnow()
        return StartAndEnd(start=start, end=end)

    yield lambda: _delta()
