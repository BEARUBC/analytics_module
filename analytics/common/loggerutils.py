import contextlib
import logging
from collections import OrderedDict
from collections.abc import Callable, Generator
from logging import Logger
from typing import Optional

from analytics.common.timeutils import TimerStats, multitimer_ms, timer_ms


def log_params(**kwargs) -> OrderedDict[str, str]:
    return OrderedDict[str, str](**kwargs)


@contextlib.contextmanager
def simple_trace(
    msg: str,
    logger: Logger,
    log_start: bool = False,
    log_level: int = logging.INFO,
    additional: Optional[OrderedDict[str, str]] = None,
) -> Generator[None, None, None]:
    """
    Wraps a block of code and logs information about the timing of the wrapped method

    :param msg: Message to log to the given logger
    :param logger: Logger to write to
    :param log_start: Whether to log a message when starting an operation. Defaults to False - generally should only
                      be used if wrapping a long-running operation
    :param log_level: Log level to use. Defaults to INFO
    :param additional: Optional dict storing additional key-value pairs to log. Can be modified, allowing users to
                       add additional information into the 'completed' message
    """
    if not logger.isEnabledFor(log_level):
        yield
        return
    success = False
    if log_start:
        kwargs_str = __format_kwargs(additional)
        logger.log(log_level, f"{msg} started{kwargs_str}")
    with timer_ms() as t:
        try:
            yield
            success = True
        finally:
            kwargs_str = __format_kwargs(additional)
            logger.log(log_level, f"{msg} completed success={success} took={t():.2f} ms{kwargs_str}")


@contextlib.contextmanager
def detail_trace(
    msg: str,
    logger: Logger,
    log_start: bool = False,
    log_level: int = logging.INFO,
    additional: Optional[OrderedDict[str, str]] = None,
) -> Generator[Callable[[str], None], None, None]:
    """
    Wraps a block of code and logs information about the timing of the wrapped method. This also yields a callable
    which can be invoked to add more granular timing information (see multitimer_ms).

    :param msg: Message to log to the given logger
    :param logger: Logger to write to
    :param log_start: Whether to log a message when starting an operation. Defaults to False - generally should only
                      be used if wrapping a long-running operation
    :param log_level: Log level to use. Defaults to INFO
    :param additional: Optional dict storing additional key-value pairs to log. Can be modified, allowing users to
                       add additional information into the 'completed' message
    """
    if not logger.isEnabledFor(log_level):
        yield lambda _: None
        return

    success = False
    stats = TimerStats()
    if log_start:
        kwargs_str = __format_kwargs(additional)
        logger.log(log_level, f"{msg} started{kwargs_str}")
    with multitimer_ms() as (t, s):

        def step(label: str) -> None:
            time = s()
            if label in stats:
                stats[label] += time
            else:
                stats[label] = time

        try:
            yield step
            success = True
        finally:
            step("trace_overhead")
            kwargs_str = __format_kwargs(additional)
            stats_str = f" ({stats.summary()})"
            logger.log(log_level, f"{msg} completed success={success} took={t():.2f} ms{stats_str}{kwargs_str}")


@contextlib.contextmanager
def threshold_trace(
    msg: str,
    logger: Logger,
    threshold_ms: float,
    log_level: int = logging.INFO,
    additional: Optional[OrderedDict[str, str]] = None,
) -> Generator[Callable[[str], None], None, None]:
    """
    Similar to detail_trace, but never logs starting messages, and will only log an ending message if the wrapped
    operation exceeded the specified threshold_ms

    :param msg: Message to log to the given logger
    :param logger: Logger to write to
    :param threshold_ms: Threshold (in milliseconds) at which we should log details if overall operation time exceeds
    :param log_level: Log level to use. Defaults to INFO
    :param additional: Optional dict storing additional key-value pairs to log. Can be modified, allowing users to
                       add additional information into the 'completed' message
    """
    if not logger.isEnabledFor(log_level):
        yield lambda _: None
        return

    success = False
    stats = TimerStats()
    with multitimer_ms() as (t, s):

        def step(label: str) -> None:
            time = s()
            if label in stats:
                stats[label] += time
            else:
                stats[label] = time

        try:
            yield step
            success = True
        finally:
            step("trace_overhead")
            final = t()
            if final >= threshold_ms and logger.isEnabledFor(log_level):
                kwargs_str = __format_kwargs(additional)
                stats_str = f" ({stats.summary()})"
                logger.log(log_level, f"{msg} completed success={success} took={t():.2f} ms{stats_str}{kwargs_str}")


def __format_kwargs(kwargs_dict: Optional[OrderedDict[str, str]]) -> str:
    kwargs_str = ""
    if kwargs_dict:
        kwargs_str = " " + " ".join([f"{k}={v}" for k, v in kwargs_dict.items()])
    return kwargs_str