
from src.validators import (
    is_valid_age,
    is_valid_email,
    is_valid_password,
)

# ========================================
# TESTS EMAIL (7 tests)
# ========================================

def test_should_accept_valid_email():
    assert is_valid_email("user@example.com") is True


def test_should_accept_email_with_special_characters():
    assert is_valid_email("user.name+tag@domain.co") is True


def test_should_reject_email_without_at():
    assert is_valid_email("invalid") is False


def test_should_reject_email_without_username():
    assert is_valid_email("@domain.com") is False


def test_should_reject_email_without_domain():
    assert is_valid_email("user@") is False


def test_should_reject_empty_email():
    assert is_valid_email("") is False


def test_should_reject_null_email():
    assert is_valid_email(None) is False


def test_should_reject_email_with_domain_but_without_at():
    # Arrange
    email = "userexample.com"

    # Act
    result = is_valid_email(email)

    # Assert
    assert result is False

# ========================================
# TESTS PASSWORD (8 tests)
# ========================================

def test_should_accept_valid_password():
    result = is_valid_password("Passw0rd!")

    assert result == {
        "valid": True,
        "errors": [],
    }


def test_should_reject_short_password():
    result = is_valid_password("short")

    assert result["valid"] is False
    assert "Minimum 8 caractères" in result["errors"]
    assert "Majuscule manquante" in result["errors"]
    assert "Chiffre manquant" in result["errors"]
    assert "Caractère spécial manquant" in result["errors"]


def test_should_reject_password_without_uppercase():
    result = is_valid_password("alllowercase1!")

    assert result["valid"] is False
    assert "Majuscule manquante" in result["errors"]


def test_should_reject_password_without_lowercase():
    result = is_valid_password("ALLUPPERCASE1!")

    assert result["valid"] is False
    assert "Minuscule manquante" in result["errors"]


def test_should_reject_password_without_digit():
    result = is_valid_password("NoDigits!here")

    assert result["valid"] is False
    assert "Chiffre manquant" in result["errors"]


def test_should_reject_password_without_special_character():
    result = is_valid_password("NoSpecial1here")

    assert result["valid"] is False
    assert "Caractère spécial manquant" in result["errors"]


def test_should_reject_empty_password():
    result = is_valid_password("")

    assert result["valid"] is False
    assert len(result["errors"]) == 5


def test_should_reject_null_password():
    result = is_valid_password(None)

    assert result["valid"] is False
    assert len(result["errors"]) == 5


# ========================================
# TESTS AGE (8 tests)
# ========================================

def test_should_accept_valid_age():
    assert is_valid_age(25) is True


def test_should_accept_minimum_age():
    assert is_valid_age(0) is True


def test_should_accept_maximum_age():
    assert is_valid_age(150) is True


def test_should_reject_negative_age():
    assert is_valid_age(-1) is False


def test_should_reject_age_above_maximum():
    assert is_valid_age(151) is False


def test_should_reject_decimal_age():
    assert is_valid_age(25.5) is False


def test_should_reject_string_age():
    assert is_valid_age("25") is False


def test_should_reject_null_age():
    assert is_valid_age(None) is False
