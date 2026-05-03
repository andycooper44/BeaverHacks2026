import random
from dataclasses import dataclass


@dataclass
class Country:
    name: str = ""
    shipping_cost: float = 0.0
    tax_rate: float = 0.0
    demand_level: float = 0.0
    notes: str = ""

    def calculate_shipping(self, quantity: int) -> float:
        return self.shipping_cost * quantity

    def calculate_taxes(self, revenue: float) -> float:
        return revenue * self.tax_rate

    def update_demand(self) -> None:
        self.demand_level *= 0.95 + random.random() * 0.1
        self.demand_level = max(0.1, min(1.0, self.demand_level))


def create_default_countries() -> list[Country]:
    return [
        Country("USA", 5.0, 0.08, 0.9, "High demand, expensive shipping"),
        Country("China", 15.0, 0.05, 0.7, "Cheap manufacturing, long shipping"),
        Country("Germany", 8.0, 0.19, 0.8, "Quality focus, high taxes"),
        Country("Brazil", 12.0, 0.12, 0.6, "Growing market, variable shipping"),
    ]


def find_country(countries: list[Country], name: str) -> Country | None:
    return next((country for country in countries if country.name == name), None)
