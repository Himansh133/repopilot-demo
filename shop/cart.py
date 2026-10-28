"""Shopping cart."""

from dataclasses import dataclass, field

from shop.money import ZERO, to_money


@dataclass
class Line:
    sku: str
    unit_price: object
    qty: int


@dataclass
class Cart:
    lines: list = field(default_factory=list)

    def add(self, sku, unit_price, qty=1):
        if qty < 1:
            raise ValueError("qty must be at least 1")
        self.lines.append(Line(sku, to_money(unit_price), qty))

    def subtotal(self):
        return sum((line.unit_price * line.qty for line in self.lines), ZERO)
