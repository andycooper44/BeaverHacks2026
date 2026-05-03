from dataclasses import dataclass


@dataclass
class SellingSite:
    name: str = ""
    fee_rate: float = 0.0
    traffic: float = 0.0
    trust: float = 0.0
    notes: str = ""
