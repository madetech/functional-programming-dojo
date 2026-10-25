import pytest

FIRST_RECURSIVE_POSITION = 2
EXPECTED_FIRST_TEN = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
FIRST_TEN_POSITIONS = range(10)


def fibonacci_imperative(position):
    previous = 0
    current = 1
    for _ in range(position):
        next_number = previous + current
        previous = current
        current = next_number
    return previous


def reject_negative_position(position):
    if position < 0:
        raise ValueError(f"Fibonacci position must be 0 or more, got {position}")


def fibonacci_recursive(position):
    reject_negative_position(position)
    if position < FIRST_RECURSIVE_POSITION:
        return position
    return fibonacci_recursive(position - 1) + fibonacci_recursive(position - 2)


def fibonacci_with_accumulator(position, previous=0, current=1):
    if position == 0:
        return previous
    return fibonacci_with_accumulator(position - 1, current, previous + current)


def test_all_versions_produce_the_same_sequence():
    for fibonacci in (fibonacci_imperative, fibonacci_recursive, fibonacci_with_accumulator):
        assert [fibonacci(position) for position in FIRST_TEN_POSITIONS] == EXPECTED_FIRST_TEN


def test_negative_position_is_rejected():
    with pytest.raises(ValueError):
        fibonacci_recursive(-1)
