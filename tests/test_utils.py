
from src.utils import (
    calculate_average,
    capitalize,
    clamp,
    group_by,
    parse_price,
    slugify,
    sort_students,
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

def test_should_sort_students_by_grade_ascending():
    # Arrange
    students = [
        {"name": "Alice", "grade": 15, "age": 20},
        {"name": "Bob", "grade": 10, "age": 22},
        {"name": "Charlie", "grade": 18, "age": 19},
    ]

    # Act
    result = sort_students(students, "grade", "asc")

    # Assert
    assert [student["grade"] for student in result] == [
        10, 15, 18
    ]
    
def test_should_sort_students_by_grade_descending():
    students = [
        {"name": "Alice", "grade": 15, "age": 20},
        {"name": "Bob", "grade": 10, "age": 22},
        {"name": "Charlie", "grade": 18, "age": 19},
    ]

    result = sort_students(students, "grade", "desc")

    assert [s["grade"] for s in result] == [18, 15, 10]

def test_should_sort_students_by_name_ascending():
    students = [
        {"name": "Charlie", "grade": 18, "age": 19},
        {"name": "Alice", "grade": 15, "age": 20},
        {"name": "Bob", "grade": 10, "age": 22},
    ]

    result = sort_students(students, "name", "asc")

    assert [s["name"] for s in result] == [
        "Alice", "Bob", "Charlie"
    ]

def test_should_sort_students_by_age_ascending():
    students = [
        {"name": "Alice", "grade": 15, "age": 20},
        {"name": "Bob", "grade": 10, "age": 22},
        {"name": "Charlie", "grade": 18, "age": 19},
    ]

    result = sort_students(students, "age", "asc")

    assert [s["age"] for s in result] == [19, 20, 22]

def test_should_return_empty_array_when_students_null():
    assert sort_students(None, "grade") == []

def test_should_return_empty_array_when_students_empty():
    assert sort_students([], "grade") == []

def test_should_not_modify_original_students():
    students = [
        {"name": "Bob", "grade": 10, "age": 22},
        {"name": "Alice", "grade": 15, "age": 20},
    ]

    original = [student.copy() for student in students]

    sort_students(students, "name", "asc")

    assert students == original

def test_should_default_to_ascending_order():
    students = [
        {"name": "Charlie", "grade": 18, "age": 19},
        {"name": "Alice", "grade": 15, "age": 20},
        {"name": "Bob", "grade": 10, "age": 22},
    ]

    result = sort_students(students, "name")

    assert [s["name"] for s in result] == [
        "Alice", "Bob", "Charlie"
    ]
    

def test_should_parse_decimal_string():
    assert parse_price("12.99") == 12.99


def test_should_parse_comma_decimal():
    assert parse_price("12,99") == 12.99


def test_should_parse_price_with_suffix_euro():
    assert parse_price("12.99 €") == 12.99


def test_should_parse_price_with_prefix_euro():
    assert parse_price("€12.99") == 12.99


def test_should_accept_numeric_price():
    assert parse_price(12.99) == 12.99


def test_should_convert_free_to_zero():
    assert parse_price("gratuit") == 0


def test_should_reject_invalid_price():
    assert parse_price("abc") is None


def test_should_reject_negative_price():
    assert parse_price("-5.00") is None


def test_should_reject_null_price():
    assert parse_price(None) is None


def test_should_reject_boolean_price():
    assert parse_price(True) is None


def test_should_group_by_role():
    users = [
        {"name": "Alice", "role": "dev"},
        {"name": "Bob", "role": "design"},
        {"name": "Charlie", "role": "dev"},
    ]

    result = group_by(users, "role")

    assert len(result["dev"]) == 2
    assert len(result["design"]) == 1
    assert result["dev"][0]["name"] == "Alice"


def test_should_return_empty_groups_when_empty():
    assert group_by([], "role") == {}


def test_should_return_empty_groups_when_null():
    assert group_by(None, "role") == {}


def test_should_group_missing_keys_under_none():
    users = [{"name": "Alice"}]

    result = group_by(users, "role")

    assert result[None] == users


def test_should_group_all_items_in_one_group():
    users = [
        {"name": "Alice", "role": "dev"},
        {"name": "Bob", "role": "dev"},
    ]

    result = group_by(users, "role")

    assert len(result["dev"]) == 2


def test_should_reject_invalid_group_input():
    import pytest

    with pytest.raises(ValueError):
        group_by("invalid", "role")
