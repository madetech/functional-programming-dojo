import timeit

FIRST_RECURSIVE_POSITION = 2
FIRST_TWO_FIBONACCI_NUMBERS = (0, 1)
EXPECTED_FIRST_TEN = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
TIMING_POSITION = 30
TIMING_RUNS = 1


# Stretch 1: a pure fibonacci_sequence built from next_pair

def next_pair(pair):
    previous, current = pair
    return (current, previous + current)


def fibonacci_sequence(length, pair=FIRST_TWO_FIBONACCI_NUMBERS, sequence_so_far=()):
    if len(sequence_so_far) == length:
        return sequence_so_far
    previous, _ = pair
    return fibonacci_sequence(length, next_pair(pair), (*sequence_so_far, previous))


def test_sequence_of_ten_matches_the_known_numbers():
    assert fibonacci_sequence(10) == EXPECTED_FIRST_TEN


def test_sequence_of_zero_is_empty():
    assert fibonacci_sequence(0) == ()


def test_sequence_is_a_tuple():
    assert isinstance(fibonacci_sequence(5), tuple)


def test_sequence_gives_the_same_answer_twice():
    assert fibonacci_sequence(10) == fibonacci_sequence(10)


# Stretch 2: timing the naive recursion against the accumulator

def fibonacci_recursive(position):
    if position < FIRST_RECURSIVE_POSITION:
        return position
    return fibonacci_recursive(position - 1) + fibonacci_recursive(position - 2)


def fibonacci_with_accumulator(position, previous=0, current=1):
    if position == 0:
        return previous
    return fibonacci_with_accumulator(position - 1, current, previous + current)


def time_in_seconds(fibonacci):
    return timeit.timeit(lambda: fibonacci(TIMING_POSITION), number=TIMING_RUNS)


if __name__ == "__main__":
    recursive_seconds = time_in_seconds(fibonacci_recursive)
    accumulator_seconds = time_in_seconds(fibonacci_with_accumulator)
    print(f"fibonacci_recursive({TIMING_POSITION}):        {recursive_seconds:.6f}s")
    print(f"fibonacci_with_accumulator({TIMING_POSITION}): {accumulator_seconds:.6f}s")
    print(f"The accumulator was about {recursive_seconds / accumulator_seconds:,.0f} times faster")
