"""Order quotes.

Rules:
- Coupons apply in the order given. Each coupon applies to what is left after
  the coupons before it, so 20% then 10% off 100.00 leaves 72.00, not 70.00.
- Tax is charged on the amount left after all coupons.
- Shipping is free when the amount left after all coupons is at least
  FREE_SHIPPING_FROM; otherwise SHIPPING_FEE is added. Tax does not count.
"""

from dataclasses import dataclass
from decimal import Decimal

from shop.coupons import discount_for
from shop.money import ZERO, to_money

TAX_RATE = Decimal("0.08")
FREE_SHIPPING_FROM = Decimal("50.00")
SHIPPING_FEE = Decimal("5.99")


@dataclass(frozen=True)
class Quote:
    subtotal: Decimal
    discount: Decimal
    tax: Decimal
    shipping: Decimal
    total: Decimal


def quote(cart, coupons=()):
    subtotal = cart.subtotal()
    discount = ZERO
    remaining = subtotal
    for c in coupons:
        off = discount_for(c, remaining)
        discount += off
        remaining -= off
    after_discount = remaining
    tax = to_money(after_discount * TAX_RATE)
    shipping = ZERO if remaining >= FREE_SHIPPING_FROM else SHIPPING_FEE
    return Quote(subtotal, discount, tax, shipping, after_discount + tax + shipping)
