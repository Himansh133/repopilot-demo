from decimal import Decimal as D

import pytest

from shop.cart import Cart
from shop.checkout import quote
from shop.coupons import Coupon


def make_cart(*items):
    cart = Cart()
    for sku, price, qty in items:
        cart.add(sku, price, qty)
    return cart


def test_subtotal_sums_lines():
    cart = make_cart(("mug", 15, 2), ("lamp", 30, 1))
    assert cart.subtotal() == D("60.00")


def test_cart_rejects_zero_qty():
    with pytest.raises(ValueError):
        make_cart(("mug", 15, 0))


def test_no_coupon_under_threshold_pays_shipping():
    q = quote(make_cart(("mug", 15, 2)))
    assert q.shipping == D("5.99")
    assert q.tax == D("2.40")
    assert q.total == D("38.39")


def test_no_coupon_over_threshold_ships_free():
    q = quote(make_cart(("lamp", 30, 2)))
    assert q.shipping == D("0.00")
    assert q.total == D("64.80")


def test_fixed_coupon_never_goes_below_zero():
    q = quote(make_cart(("pen", 3, 1)), [Coupon("BIG", "fixed", 10)])
    assert q.discount == D("3.00")
    assert q.tax == D("0.00")


def test_single_percent_coupon():
    q = quote(make_cart(("mug", 15, 2)), [Coupon("SAVE20", "percent", 20)])
    assert q.discount == D("6.00")
    assert q.total == D("25.92") + D("5.99")


def test_stacked_coupons_apply_one_after_another():
    cart = make_cart(("mug", 15, 2), ("lamp", 30, 1))
    q = quote(cart, [Coupon("SAVE20", "percent", 20), Coupon("EXTRA10", "percent", 10)])
    assert q.discount == D("16.80")
    assert q.tax == D("3.46")


def test_free_shipping_uses_amount_after_coupons():
    cart = make_cart(("mug", 15, 2), ("lamp", 30, 1))
    q = quote(cart, [Coupon("SAVE20", "percent", 20)])
    assert q.shipping == D("5.99")
    assert q.total == D("48.00") + D("3.84") + D("5.99")
