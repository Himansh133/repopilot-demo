"""Coupons. A coupon takes a percentage or a fixed amount off."""

from dataclasses import dataclass

from shop.money import to_money


@dataclass(frozen=True)
class Coupon:
    code: str
    kind: str  # "percent" or "fixed"
    value: object

    def __post_init__(self):
        if self.kind not in ("percent", "fixed"):
            raise ValueError(f"unknown coupon kind: {self.kind}")


def discount_for(coupon, amount):
    """How much `coupon` takes off `amount`. Never more than `amount` itself."""
    if coupon.kind == "percent":
        off = to_money(amount * to_money(coupon.value) / 100)
    else:
        off = to_money(coupon.value)
    return min(off, amount)
