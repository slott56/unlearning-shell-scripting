"""
Unlearning Shell Scripting.  Chapter 6. The summary computation and doctest examples.
"""

from dataclasses import dataclass
import datetime
from pathlib import Path
from statistics import mean


@dataclass
class Result:
    path: Path
    skip_reason: str | None
    returncode: int | None
    start: datetime.datetime
    end: datetime.datetime
    output: list[str]


def average_duration(history: list[Result]) -> float:
    """
    Computes average run time for all the processing steps.

    >>> from pathlib import Path
    >>> import datetime
    >>> from summary_example import Result, average_duration
    >>> samples = [
    ...     Result(Path("example"), None, 0,
    ...         datetime.datetime(2025, 7, 10, 1, 2, 3),
    ...         datetime.datetime(2025, 7, 10, 1, 3, 33),
    ...         ["messages"]
    ...     )
    ... ]
    >>> average_duration(samples)
    90
    """
    durations = [
        (result.end - result.start).seconds for result in history
    ]
    return mean(durations)


import unittest


@unittest.expectedFailure
class TestSummary(unittest.TestCase):
    def setUp(self) -> None:
        self.samples = [
            Result(
                Path("example1"),
                None,
                0,
                datetime.datetime(2025, 7, 10, 1, 2, 3),
                datetime.datetime(2025, 7, 10, 1, 3, 33),
                ["messages 1"],
            ),
            Result(
                Path("example2"),
                None,
                2,
                datetime.datetime(2025, 7, 10, 1, 4, 5),
                datetime.datetime(2025, 7, 10, 1, 4, 6),
                ["messages 2"],
            ),
            Result(
                Path("example3"),
                "Not run for reasons",
                None,
                datetime.datetime(2025, 7, 10, 1, 5, 7),
                datetime.datetime(2025, 7, 10, 1, 5, 7),
                [],
            ),
        ]

    def test(self) -> None:
        self.assertEqual(average_duration(self.samples), 45.5)
