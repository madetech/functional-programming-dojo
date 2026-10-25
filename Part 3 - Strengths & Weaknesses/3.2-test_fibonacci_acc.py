import sys

import pytest

SAFE_POSITION = 500
TOO_DEEP_POSITION = 5000


def fibonacci_with_accumulator(position, previous=0, current=1):
    if position == 0:
        return previous
    return fibonacci_with_accumulator(position - 1, current, previous + current)


def fibonacci_imperative(position):
    previous = 0
    current = 1
    for _ in range(position):
        next_number = previous + current
        previous = current
        current = next_number
    return previous


def test_python_has_a_recursion_limit():
    print(f"Python's recursion limit is {sys.getrecursionlimit()}")
    assert TOO_DEEP_POSITION > sys.getrecursionlimit()


def test_accumulator_works_below_the_limit():
    assert fibonacci_with_accumulator(SAFE_POSITION) == fibonacci_imperative(SAFE_POSITION)


def test_accumulator_runs_out_of_stack_above_the_limit():
    with pytest.raises(RecursionError):
        fibonacci_with_accumulator(TOO_DEEP_POSITION)


def test_imperative_version_has_no_such_limit():
    assert fibonacci_imperative(TOO_DEEP_POSITION) > 0
