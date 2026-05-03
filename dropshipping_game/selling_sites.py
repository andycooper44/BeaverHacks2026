import random
from dataclasses import dataclass

from dropshipping_game.countries import Country


@dataclass
class SellingSite:
    name: str = ""
    fee_rate: float = 0.0
    traffic: float = 0.0
    trust: float = 0.0
    notes: str = ""

    def calculate_fee(self, revenue: float) -> float:
        return revenue * self.fee_rate

    def calculate_price(self, base_price: float, country: Country) -> float:
        demand_multiplier = country.demand_level * self.traffic
        variation = 0.8 + random.random() * 0.4
        return base_price * demand_multiplier * variation


def create_default_selling_sites() -> list[SellingSite]:
    return [
        SellingSite("Amazon", 0.15, 0.95, 0.9, "High traffic, high fees"),
        SellingSite("eBay", 0.10, 0.8, 0.7, "Auction style, moderate fees"),
        SellingSite("Shopify Store", 0.05, 0.6, 0.8, "Your own store, low fees"),
        SellingSite("Facebook Marketplace", 0.03, 0.7, 0.6, "Local sales, low fees"),
    ]


def find_selling_site(selling_sites: list[SellingSite], name: str) -> SellingSite | None:
    return next((site for site in selling_sites if site.name == name), None)
