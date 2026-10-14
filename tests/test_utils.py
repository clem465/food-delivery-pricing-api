
from src.utils import (
    calculate_average,
    capitalize,
    clamp,
    slugify,
)

# CAPITALIZE

def test_should_capitalize_lowercase_word():
    # Arrange
    text = "hello"

    # Act
    result = capitalize(text)

    # Assert
    assert result == "Hello"


def test_should_lowercase_remaining_letters():
    assert capitalize("WORLD") == "World"


def test_should_return_empty_string_when_empty():
    assert capitalize("") == ""


def test_should_return_empty_string_when_null():
    assert capitalize(None) == ""


# CALCULATE AVERAGE

def test_should_calculate_average_of_three_numbers():
    assert calculate_average([10, 12, 14]) == 12


def test_should_return_number_when_single_value():
    assert calculate_average([15]) == 15


def test_should_return_zero_when_empty_list():
    assert calculate_average([]) == 0


def test_should_return_zero_when_null():
    assert calculate_average(None) == 0


def test_should_calculate_average_with_decimals():
    assert calculate_average([10, 11, 12]) == 11


# SLUGIFY

def test_should_convert_spaces_to_hyphens():
    assert slugify("Hello World") == "hello-world"


def test_should_remove_extra_spaces():
    assert slugify(" Spaces Everywhere ") == "spaces-everywhere"


def test_should_remove_special_characters():
    assert slugify("C'est l'ete !") == "cest-lete"


def test_should_return_empty_slug_when_empty():
    assert slugify("") == ""


# CLAMP

def test_should_keep_value_inside_range():
    assert clamp(5, 0, 10) == 5


def test_should_return_minimum_when_below_range():
    assert clamp(-5, 0, 10) == 0


def test_should_return_maximum_when_above_range():
    assert clamp(15, 0, 10) == 10


def test_should_handle_equal_bounds():
    assert clamp(0, 0, 0) == 0
