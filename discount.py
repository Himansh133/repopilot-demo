"""Price helpers for a small shop."""


def apply_discount(price, percent):
    """Return the price after taking `percent` percent off, rounded to 2 decimals."""
    if percent < 0 or percent > 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)


def total(prices):
    """Return the sum of all prices, rounded to 2 decimals."""
    return round(sum(prices), 2)
