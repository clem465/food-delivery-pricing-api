import pytest
from fastapi.testclient import TestClient

from src.app import app, orders, reset_orders

client = TestClient(app)

VALID_ORDER = {
    "items": [
        {
            "name": "Pizza",
            "price": 12.50,
            "quantity": 2,
        }
    ],
    "distance": 5,
    "weight": 2,
    "hour": 15,
    "dayOfWeek": "tuesday",
}


@pytest.fixture(autouse=True)
def clean_orders():
    reset_orders()
    yield
    reset_orders()


def test_should_simulate_normal_order():
    response = client.post("/orders/simulate", json=VALID_ORDER)

    assert response.status_code == 200
    assert response.json()["total"] == 28


def test_should_simulate_order_with_promo():
    data = {**VALID_ORDER, "promoCode": "BIENVENUE20"}

    response = client.post("/orders/simulate", json=data)

    assert response.status_code == 200
    assert response.json()["discount"] == 5
    assert response.json()["total"] == 23


def test_should_reject_expired_promo():
    data = {**VALID_ORDER, "promoCode": "EXPIRE"}

    response = client.post("/orders/simulate", json=data)

    assert response.status_code == 400
    assert "expiré" in response.json()["detail"]


def test_should_reject_empty_cart():
    data = {**VALID_ORDER, "items": []}

    response = client.post("/orders/simulate", json=data)

    assert response.status_code == 400


def test_should_reject_out_of_zone():
    data = {**VALID_ORDER, "distance": 15}

    response = client.post("/orders/simulate", json=data)

    assert response.status_code == 400


def test_should_reject_closed_restaurant():
    data = {**VALID_ORDER, "hour": 23}

    response = client.post("/orders/simulate", json=data)

    assert response.status_code == 400


def test_should_apply_friday_surge():
    data = {
        **VALID_ORDER,
        "hour": 20,
        "dayOfWeek": "friday",
    }

    response = client.post("/orders/simulate", json=data)

    assert response.status_code == 200
    assert response.json()["surge"] == 1.8
    assert response.json()["deliveryFee"] == 5.4
    assert response.json()["total"] == 30.4


def test_should_create_order():
    response = client.post("/orders", json=VALID_ORDER)

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["total"] == 28


def test_should_retrieve_created_order():
    created = client.post("/orders", json=VALID_ORDER)
    order_id = created.json()["id"]

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    assert response.json()["id"] == order_id


def test_should_generate_unique_order_ids():
    first = client.post("/orders", json=VALID_ORDER)
    second = client.post("/orders", json=VALID_ORDER)

    assert first.json()["id"] != second.json()["id"]


def test_should_reject_invalid_order_creation():
    data = {**VALID_ORDER, "distance": 15}

    response = client.post("/orders", json=data)

    assert response.status_code == 400


def test_should_not_save_invalid_order():
    data = {**VALID_ORDER, "distance": 15}

    client.post("/orders", json=data)

    assert len(orders) == 0


def test_should_return_404_for_unknown_order():
    response = client.get("/orders/999")

    assert response.status_code == 404


def test_should_return_complete_order_structure():
    created = client.post("/orders", json=VALID_ORDER)

    response = client.get(f"/orders/{created.json()['id']}")

    assert {
        "id",
        "items",
        "subtotal",
        "discount",
        "deliveryFee",
        "surge",
        "total",
    }.issubset(response.json().keys())


def test_should_return_correct_order_total():
    client.post("/orders", json=VALID_ORDER)

    response = client.get("/orders/1")

    assert response.status_code == 200
    assert response.json()["subtotal"] == 25
    assert response.json()["deliveryFee"] == 3
    assert response.json()["total"] == 28


def test_should_validate_promo():
    response = client.post(
        "/promo/validate",
        json={
            "code": "BIENVENUE20",
            "subtotal": 50,
        },
    )

    assert response.status_code == 200
    assert response.json()["valid"] is True
    assert response.json()["newPrice"] == 40


def test_should_reject_expired_promo_validation():
    response = client.post(
        "/promo/validate",
        json={"code": "EXPIRE", "subtotal": 50},
    )

    assert response.status_code == 400
    assert "expiré" in response.json()["detail"]


def test_should_reject_promo_below_minimum():
    response = client.post(
        "/promo/validate",
        json={
            "code": "BIENVENUE20",
            "subtotal": 5,
        },
    )

    assert response.status_code == 400
    assert "minimum" in response.json()["detail"]


def test_should_return_404_for_unknown_promo():
    response = client.post(
        "/promo/validate",
        json={"code": "UNKNOWN", "subtotal": 50},
    )

    assert response.status_code == 404


def test_should_reject_missing_promo_code():
    response = client.post(
        "/promo/validate",
        json={"subtotal": 50},
    )

    assert response.status_code == 422


def test_should_reject_empty_promo_code():
    response = client.post(
        "/promo/validate",
        json={"code": "", "subtotal": 50},
    )

    assert response.status_code == 400
