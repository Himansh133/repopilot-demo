"""Money helpers. All amounts are Decimal, rounded half-up to whole cents."""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")
ZERO = Decimal("0.00")


def to_money(value):
    """Round a number to cents. Floats go through str() so 0.1 stays 0.1."""
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)
