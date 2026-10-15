
from datetime import date

import pytest

from src.pricing import (
    apply_promo_code,
    calculate_delivery_fee,
    calculate_order_total,
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
