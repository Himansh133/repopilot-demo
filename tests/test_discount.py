import pytest

from discount import apply_discount, total


def test_ten_percent_off():
    assert apply_discount(200, 10) == 180


def test_no_discount():
    assert apply_discount(50, 0) == 50


def test_rejects_bad_percent():
    with pytest.raises(ValueError):
        apply_discount(50, 150)


def test_total():
    assert total([1.10, 2.20]) == 3.30
