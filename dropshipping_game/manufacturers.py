import random
from dataclasses import dataclass


@dataclass
class Manufacturer:
    name: str = ""
    product: str = ""
    unit_cost: float = 0.0
    stock: int = 0
    quality: float = 0.0
    notes: str = ""

    def can_fulfill(self, quantity: int) -> bool:
        return quantity > 0 and self.stock >= quantity

    def purchase_cost(self, quantity: int) -> float:
        return self.unit_cost * quantity

    def remove_stock(self, quantity: int) -> None:
        self.stock -= quantity

    def restock(self) -> None:
        self.stock += random.randint(0, 100)


BASE_PRICES: dict[str, float] = {
    "Smartphone": 400.0,
    "T-Shirt": 25.0,
    "Coffee Maker": 80.0,
    "Action Figure": 15.0,
}


def create_default_manufacturers() -> list[Manufacturer]:
    return [
        Manufacturer("TechCorp", "Smartphone", 200.0, 1000, 0.85, "Reliable electronics"),
        Manufacturer("FashionHub", "T-Shirt", 15.0, 5000, 0.7, "Trendy clothing"),
        Manufacturer("HomeGoods Inc", "Coffee Maker", 45.0, 2000, 0.8, "Quality appliances"),
        Manufacturer("ToyWorld", "Action Figure", 8.0, 8000, 0.6, "Fun toys"),
    ]


def find_manufacturer(manufacturers: list[Manufacturer], name: str) -> Manufacturer | None:
    return next((manufacturer for manufacturer in manufacturers if manufacturer.name == name), None)


def find_manufacturer_by_product(
    manufacturers: list[Manufacturer],
    product: str,
) -> Manufacturer | None:
    return next((manufacturer for manufacturer in manufacturers if manufacturer.product == product), None)


def get_base_price(product: str) -> float:
    return BASE_PRICES.get(product, 50.0)


def get_unit_cost(manufacturers: list[Manufacturer], product: str) -> float:
    manufacturer = find_manufacturer_by_product(manufacturers, product)
    if manufacturer is None:
        return 10.0

    return manufacturer.unit_cost
