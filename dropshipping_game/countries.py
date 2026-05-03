from dataclasses import dataclass


@dataclass
class Country:
    name: str = ""
    shipping_cost: float = 0.0
    tax_rate: float = 0.0
    demand_level: float = 0.0
    notes: str = ""
