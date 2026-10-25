numbers = [1, 2, 3, 4, 5, 6]


def is_even(number):
    return number % 2 == 0


def square(number):
    return number * number


def squares_of_evens_imperative(numbers):
    result = []
    for number in numbers:
        if is_even(number):
            result.append(square(number))
    return result


def squares_of_evens_declarative(numbers):
    return [square(number) for number in numbers if is_even(number)]


def test_both_styles_give_the_same_answer():
    assert squares_of_evens_imperative(numbers) == squares_of_evens_declarative(numbers) == [4, 16, 36]