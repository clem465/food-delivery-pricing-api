from copy import deepcopy
from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.pricing import (
    PROMO_CODES,
    apply_promo_code,
    calculate_order_total,
    money,
)

app = FastAPI(
    title="Food Delivery Pricing API",
    version="1.0.0",
    description="API de tarification de livraison de repas",
)

orders = {}
next_order_id = 1


class Item(BaseModel):
    name: str
    price: float = Field(ge=0, allow_inf_nan=False)
    quantity: int = Field(gt=0)


class OrderRequest(BaseModel):
    items: list[Item]
    distance: float = Field(ge=0, allow_inf_nan=False)
    weight: float = Field(ge=0, allow_inf_nan=False)
    promoCode: str | None = None
    hour: float = Field(ge=0, lt=24, allow_inf_nan=False)
    dayOfWeek: str


class PromoRequest(BaseModel):
    code: str
    subtotal: float = Field(ge=0, allow_inf_nan=False)


def reset_orders():
    global next_order_id

    orders.clear()
    next_order_id = 1


def get_price(data: OrderRequest):
    try:
        return calculate_order_total(
            items=[item.model_dump() for item in data.items],
            distance=data.distance,
            weight=data.weight,
            promo_code=data.promoCode,
            hour=data.hour,
            day_of_week=data.dayOfWeek,
        )
    except (ValueError, LookupError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post("/orders/simulate")
def simulate_order(data: OrderRequest):
    return get_price(data)


@app.post("/orders", status_code=201)
def create_order(data: OrderRequest):
    global next_order_id

    price = get_price(data)

    order = {
        "id": next_order_id,
        "items": [item.model_dump() for item in data.items],
        "distance": data.distance,
        "weight": data.weight,
        "promoCode": data.promoCode,
        "hour": data.hour,
        "dayOfWeek": data.dayOfWeek,
        **price,
    }

    orders[next_order_id] = deepcopy(order)
    next_order_id += 1

    return order


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id not in orders:
        raise HTTPException(
            status_code=404,
            detail="Commande introuvable",
        )

    return deepcopy(orders[order_id])


@app.post("/promo/validate")
def validate_promo(data: PromoRequest):
    if not data.code:
        raise HTTPException(
            status_code=400,
            detail="Code promo obligatoire",
        )

    if not any(promo["code"] == data.code for promo in PROMO_CODES):
        raise HTTPException(
            status_code=404,
            detail="Code promo inconnu",
        )

    try:
        new_price = apply_promo_code(
            data.subtotal,
            data.code,
            today=date.today(),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "valid": True,
        "code": data.code,
        "subtotal": money(data.subtotal),
        "discount": money(data.subtotal - new_price),
        "newPrice": new_price,
    }
