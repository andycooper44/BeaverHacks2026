from dataclasses import dataclass, field

from dropshipping_game.countries import Country
from dropshipping_game.manufacturers import Manufacturer
from dropshipping_game.selling_sites import SellingSite
from dropshipping_game.tracker import SalesTracker


@dataclass
class DropshippingGame:
    tracker: SalesTracker = field(default_factory=SalesTracker)
    countries: list[Country] = field(default_factory=list)
    manufacturers: list[Manufacturer] = field(default_factory=list)
    selling_sites: list[SellingSite] = field(default_factory=list)
    current_day: int = 0
    notes: str = ""
