from dataclasses import dataclass


@dataclass
class Manufacturer:
    name: str = ""
    product: str = ""
    unit_cost: float = 0.0
    stock: int = 0
    quality: float = 0.0
    notes: str = ""
