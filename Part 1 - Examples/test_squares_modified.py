numbers = [1, 2, 3, 4, 5, 6]


def is_even(number):
    return number % 2 == 0


def square(number):
    return number * number


def is_divisible_by_three(number):
    return number % 3 == 0


def is_not_divisible_by_three(number):
    return not is_divisible_by_three(number)


def is_wanted(number):
    return is_even(number) and is_not_divisible_by_three(number)


def squares_of_wanted_numbers_imperative(numbers):
    result = []
    for number in numbers:
        if is_even(number):
            if is_not_divisible_by_three(number):
                result.append(square(number))
    return result


def squares_of_wanted_numbers_declarative(numbers):
    return [square(number) for number in numbers if is_wanted(number)]


def squares_of_wanted_numbers_functional(numbers):
    return list(map(square, filter(is_not_divisible_by_three, filter(is_even, numbers))))


def test_wanted_numbers_are_even_and_not_divisible_by_three():
    assert [number for number in numbers if is_wanted(number)] == [2, 4]


def test_all_styles_give_the_same_answer():
    assert (
        squares_of_wanted_numbers_imperative(numbers)
        == squares_of_wanted_numbers_declarative(numbers)
        == squares_of_wanted_numbers_functional(numbers)
        == [4, 16]
    )


def test_imperative_version_does_not_change_its_input():
    original_numbers = list(numbers)
    squares_of_wanted_numbers_imperative(numbers)
    assert numbers == original_numbers
