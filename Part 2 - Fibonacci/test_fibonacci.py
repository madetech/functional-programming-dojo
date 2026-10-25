# 2.2 Imperative

def fibonacci_imperative(position):
    previous = 0
    current = 1
    for _ in range(position):
        next_number = previous + current
        previous = current
        current = next_number
    return previous

# 2.3 Pure Functions

fibonacci_so_far = [0, 1]

def next_fibonacci_impure():
    fibonacci_so_far.append(fibonacci_so_far[-1] + fibonacci_so_far[-2])
    return fibonacci_so_far[-1]

print(next_fibonacci_impure(), next_fibonacci_impure())  # 1 2 - different every call


def next_pair(pair):
    previous, current = pair
    return (current, previous + current)


assert next_pair((0, 1)) == (1, 1)
assert next_pair((0, 1)) == (1, 1)  # call it as often as you like

# 2.4 Immutability

fibonacci_start = (0, 1)
fibonacci_extended = (*fibonacci_start, 1)

assert fibonacci_start == (0, 1)        # the original is untouched
assert fibonacci_extended == (0, 1, 1)  # a brand new tuple


# 2.5 Recursion
FIRST_RECURSIVE_POSITION = 2

def fibonacci_recursive(position):
    if position < FIRST_RECURSIVE_POSITION:
        return position
    return fibonacci_recursive(position - 1) + fibonacci_recursive(position - 2)

def fibonacci_with_accumulator(position, previous=0, current=1):
    if position == 0:
        return previous
    return fibonacci_with_accumulator(position - 1, current, previous + current)

EXPECTED_FIRST_TEN = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
FIRST_TEN_POSITIONS = range(10)

def test_all_versions_produce_the_same_sequence():
    for fibonacci in (fibonacci_imperative, fibonacci_recursive, fibonacci_with_accumulator):
        assert [fibonacci(position) for position in FIRST_TEN_POSITIONS] == EXPECTED_FIRST_TEN