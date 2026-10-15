from datetime import date
from decimal import ROUND_HALF_UP, Decimal

PROMO_CODES = [
    {
        "code": "BIENVENUE20",
        "type": "percentage",
        "value": 20,
        "minOrder": 15.00,
        "expiresAt": "2026-12-31",
    },
    {
        "code": "REDUC5",
        "type": "fixed",
        "value": 5,
        "minOrder": 10,
        "expiresAt": "2026-12-31",
    },
    {
        "code": "EXPIRE",
        "type": "percentage",
        "value": 10,
        "minOrder": 0,
        "expiresAt": "2020-01-01",
    },
]


def money(value):
    return float(
        Decimal(str(value)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )


def valid_number(value):
    return type(value) in (int, float) and 0 <= value < float("inf")


def calculate_delivery_fee(distance, weight):
    if not valid_number(distance) or not valid_number(weight):
        raise ValueError("Distance ou poids invalide")

    if distance > 10:
        raise ValueError("Livraison hors zone")

    fee = Decimal("2.00")

    if distance > 3:
        fee += (Decimal(str(distance)) - Decimal("3")) * Decimal("0.50")

    if weight > 5:
        fee += Decimal("1.50")

    return money(fee)


def apply_promo_code(
    subtotal,
    promo_code,
    promo_codes=None,
    today=None,
):
    if not valid_number(subtotal):
        raise ValueError("Sous-total invalide")

    if not promo_code:
        return money(subtotal)

    if not isinstance(promo_code, str):
        raise ValueError("Code promo invalide")

    if promo_codes is None:
        promo_codes = PROMO_CODES

    if today is None:
        today = date.today()

    promo = next(
        (p for p in promo_codes if p["code"] == promo_code),
        None,
    )

    if promo is None:
        raise LookupError("Code promo inconnu")

    if not valid_number(promo.get("minOrder")):
        raise ValueError("Configuration promo invalide")

    if subtotal < promo["minOrder"]:
        raise ValueError("Montant minimum non atteint")

    try:
        expiration = date.fromisoformat(promo["expiresAt"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Date d'expiration invalide") from exc

    if today > expiration:
        raise ValueError("Code promo expiré")

    value = promo.get("value")

    if not valid_number(value):
        raise ValueError("Valeur promo invalide")

    amount = Decimal(str(subtotal))
    discount = Decimal(str(value))

    if promo["type"] == "percentage":
        if discount > 100:
            raise ValueError("Pourcentage invalide")
        amount *= 1 - discount / 100

    elif promo["type"] == "fixed":
        amount -= discount

    else:
        raise ValueError("Type de promotion inconnu")

    return money(max(Decimal("0"), amount))


def calculate_surge(hour, day_of_week):
    if not valid_number(hour) or hour >= 24:
        raise ValueError("Heure invalide")

    if not isinstance(day_of_week, str):
        raise ValueError("Jour invalide")

    day = day_of_week.lower()

    valid_days = (
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    )

    if day not in valid_days:
        raise ValueError("Jour invalide")

    if hour < 10 or hour >= 22:
        return 0

    if day == "sunday":
        return 1.2

    if day in ("friday", "saturday"):
        if 19 <= hour < 22:
            return 1.8
        return 1.0

    if 12 <= hour < 13.5:
        return 1.3

    if 19 <= hour < 21:
        return 1.5

    return 1.0


def calculate_order_total(
    items,
    distance,
    weight,
    promo_code=None,
    hour=15,
    day_of_week="tuesday",
    promo_codes=None,
    today=None,
):
    if not isinstance(items, list) or not items:
        raise ValueError("Panier vide ou invalide")

    subtotal = Decimal("0")

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Article invalide")

        price = item.get("price")
        quantity = item.get("quantity")

        if not valid_number(price):
            raise ValueError("Prix d'article invalide")

        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantité invalide")

        subtotal += Decimal(str(price)) * quantity

    subtotal = money(subtotal)

    surge = calculate_surge(hour, day_of_week)

    if surge == 0:
        raise ValueError("Restaurant fermé")

    delivery = calculate_delivery_fee(distance, weight)

    discounted = apply_promo_code(
        subtotal,
        promo_code,
        promo_codes=promo_codes,
        today=today,
    )

    discount = money(Decimal(str(subtotal)) - Decimal(str(discounted)))

    delivery_fee = money(Decimal(str(delivery)) * Decimal(str(surge)))

    total = money(Decimal(str(discounted)) + Decimal(str(delivery_fee)))

    return {
        "subtotal": subtotal,
        "discount": discount,
        "deliveryFee": delivery_fee,
        "surge": surge,
        "total": total,
    }
