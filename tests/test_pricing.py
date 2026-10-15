
from datetime import date

import pytest

from src.pricing import (
    apply_promo_code,
    calculate_delivery_fee,
    calculate_surge,
)


@pytest.mark.parametrize(
    ("distance", "weight", "expected"),
    [
        (2, 1, 2.00),
        (7, 3, 4.00),
        (5, 8, 4.50),
        (3, 1, 2.00),
        (10, 1, 5.50),
        (5, 5, 3.00),
        (0, 0, 2.00),
        (6, 2, 3.50),
        (10, 6, 7.00),
    ],
)
def test_should_calculate_delivery_fee(
    distance, weight, expected
):
    assert calculate_delivery_fee(distance, weight) == expected


@pytest.mark.parametrize(
    ("distance", "weight"),
    [
        (15, 1),
        (-1, 2),
        (2, -1),
        (None, 2),
    ],
)
def test_should_reject_invalid_delivery(distance, weight):
    with pytest.raises(ValueError):
        calculate_delivery_fee(distance, weight)


PROMOS = [
    {
        "code": "P20",
        "type": "percentage",
        "value": 20,
        "minOrder": 15,
        "expiresAt": "2026-12-31",
    },
    {
        "code": "F5",
        "type": "fixed",
        "value": 5,
        "minOrder": 10,
        "expiresAt": "2026-12-31",
    },
    {
        "code": "F10",
        "type": "fixed",
        "value": 10,
        "minOrder": 0,
        "expiresAt": "2026-12-31",
    },
    {
        "code": "FREE",
        "type": "percentage",
        "value": 100,
        "minOrder": 0,
        "expiresAt": "2026-12-31",
    },
    {
        "code": "OLD",
        "type": "percentage",
        "value": 10,
        "minOrder": 0,
        "expiresAt": "2020-01-01",
    },
]

TODAY = date(2026, 10, 14)


@pytest.mark.parametrize(
    ("subtotal", "code", "expected"),
    [
        (50, "P20", 40),
        (30, "F5", 25),
        (15, "P20", 12),
        (5, "F10", 0),
        (50, "FREE", 0),
        (0, None, 0),
        (50, "", 50),
        (0, "FREE", 0),
    ],
)
def test_should_apply_promotion(subtotal, code, expected):
    result = apply_promo_code(
        subtotal, code, PROMOS, TODAY
    )
    assert result == expected


@pytest.mark.parametrize(
    ("subtotal", "code", "error"),
    [
        (50, "OLD", ValueError),
        (10, "P20", ValueError),
        (50, "UNKNOWN", LookupError),
        (-10, "P20", ValueError),
    ],
)
def test_should_reject_invalid_promotion(
    subtotal, code, error
):
    with pytest.raises(error):
        apply_promo_code(
            subtotal, code, PROMOS, TODAY
        )


def test_should_accept_promo_expiring_today():
    promos = [
        {
            "code": "TODAY",
            "type": "fixed",
            "value": 5,
            "minOrder": 0,
            "expiresAt": "2026-10-14",
        }
    ]

    result = apply_promo_code(
        20, "TODAY", promos, TODAY
    )

    assert result == 15


@pytest.mark.parametrize(
    ("hour", "day", "expected"),
    [
        (15, "tuesday", 1.0),
        (12.5, "wednesday", 1.3),
        (20, "thursday", 1.5),
        (21, "friday", 1.8),
        (20, "saturday", 1.8),
        (14, "sunday", 1.2),
        (11.5, "monday", 1.0),
        (19, "monday", 1.5),
        (22, "friday", 0),
        (9.99, "monday", 0),
        (10, "monday", 1.0),
        (13.5, "tuesday", 1.0),
    ],
)
def test_should_calculate_surge(hour, day, expected):
    assert calculate_surge(hour, day) == expected


@pytest.mark.parametrize(
    ("hour", "day"),
    [
        (-1, "monday"),
        (24, "monday"),
        (12, "invalid"),
    ],
)
def test_should_reject_invalid_surge(hour, day):
    with pytest.raises(ValueError):
        calculate_surge(hour, day)
