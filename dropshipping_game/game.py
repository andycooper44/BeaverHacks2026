from dataclasses import dataclass, field

from dropshipping_game.countries import Country, create_default_countries, find_country
from dropshipping_game.gemini_client import GeminiAdvisor
from dropshipping_game.manufacturers import (
    Manufacturer,
    create_default_manufacturers,
    find_manufacturer,
    get_base_price,
    get_unit_cost,
)
from dropshipping_game.selling_sites import (
    SellingSite,
    create_default_selling_sites,
    find_selling_site,
)
from dropshipping_game.tracker import SaleRecord, SalesTracker


@dataclass
class DropshippingGame:
    tracker: SalesTracker = field(default_factory=SalesTracker)
    countries: list[Country] = field(default_factory=list)
    manufacturers: list[Manufacturer] = field(default_factory=list)
    selling_sites: list[SellingSite] = field(default_factory=list)
    inventory: dict[str, int] = field(default_factory=dict)
    advisor: GeminiAdvisor = field(default_factory=GeminiAdvisor)
    current_day: int = 1
    notes: str = ""
    rent_amount: float = 500.0
    days_until_rent: int = 7

    def __post_init__(self) -> None:
        if not self.countries:
            self.countries = create_default_countries()
        if not self.manufacturers:
            self.manufacturers = create_default_manufacturers()
        if not self.selling_sites:
            self.selling_sites = create_default_selling_sites()
        if self.tracker.money == 0:
            self.tracker.money = 1000.0

    def get_available_actions(self) -> list[str]:
        actions = ["Buy Products", "Sell Products", "Check Inventory", "View Stats", "Advance Day"]
        if self.advisor.api_key:
            actions.append("Get AI Advice")
        return actions

    def buy_products(self, manufacturer_name: str, quantity: int) -> str:
        manufacturer = find_manufacturer(self.manufacturers, manufacturer_name)
        if manufacturer is None:
            return f"Manufacturer {manufacturer_name} not found."
        if quantity <= 0:
            return "Quantity must be greater than zero."
        if not manufacturer.can_fulfill(quantity):
            return f"Not enough stock. Available: {manufacturer.stock}"

        total_cost = manufacturer.purchase_cost(quantity)
        if total_cost > self.tracker.money:
            return f"Not enough money. Need ${total_cost:.2f}, have ${self.tracker.money:.2f}"

        manufacturer.remove_stock(quantity)
        self.tracker.spend_money(total_cost)
        self.inventory[manufacturer.product] = self.inventory.get(manufacturer.product, 0) + quantity
        return f"Bought {quantity} {manufacturer.product}(s) for ${total_cost:.2f}"

    def sell_products(self, product: str, site_name: str, country_name: str, quantity: int) -> str:
        if quantity <= 0:
            return "Quantity must be greater than zero."
        if self.inventory.get(product, 0) < quantity:
            return f"Not enough {product} in inventory. Have: {self.inventory.get(product, 0)}"

        site = find_selling_site(self.selling_sites, site_name)
        country = find_country(self.countries, country_name)
        if site is None or country is None:
            return "Invalid site or country."

        revenue, total_cost, profit = self._calculate_sale(product, site, country, quantity)
        self.inventory[product] -= quantity
        if self.inventory[product] == 0:
            del self.inventory[product]

        sale = SaleRecord(
            product=product,
            quantity=quantity,
            revenue=revenue,
            cost=total_cost,
            profit=profit,
            day=self.current_day,
        )
        self.tracker.record_sale(sale)
        return f"Sold {quantity} {product}(s) for ${revenue:.2f}. Profit: ${profit:.2f}"

    def advance_day(self) -> str:
        self.current_day += 1
        events: list[str] = []

        for country in self.countries:
            country.update_demand()
        for manufacturer in self.manufacturers:
            manufacturer.restock()

        self.days_until_rent -= 1
        if self.days_until_rent <= 0:
            self.tracker.spend_money(self.rent_amount)
            self.days_until_rent = 7
            events.append(f"Rent paid: ${self.rent_amount:.2f}")

        if not events:
            events.append("Market conditions changed.")
        return f"Advanced to day {self.current_day}. " + " ".join(events)

    def get_game_status(self) -> str:
        inventory_text = ", ".join(
            f"{product}: {quantity}" for product, quantity in self.inventory.items()
        ) or "Empty"
        return (
            f"Day: {self.current_day}\n"
            f"Money: ${self.tracker.money:.2f}\n"
            f"Total Sales: {self.tracker.total_sales}\n"
            f"Total Profit: ${self.tracker.total_profit:.2f}\n"
            f"Days Until Rent: {self.days_until_rent}\n"
            f"Inventory: {inventory_text}"
        )

    def snapshot(self) -> dict[str, object]:
        return {
            "current_day": self.current_day,
            "money": round(self.tracker.money, 2),
            "total_sales": self.tracker.total_sales,
            "total_revenue": round(self.tracker.total_revenue, 2),
            "total_profit": round(self.tracker.total_profit, 2),
            "days_until_rent": self.days_until_rent,
            "rent_amount": self.rent_amount,
            "inventory": self.inventory,
            "manufacturers": [
                {
                    "name": manufacturer.name,
                    "product": manufacturer.product,
                    "unit_cost": manufacturer.unit_cost,
                    "stock": manufacturer.stock,
                    "quality": manufacturer.quality,
                    "notes": manufacturer.notes,
                }
                for manufacturer in self.manufacturers
            ],
            "countries": [
                {
                    "name": country.name,
                    "shipping_cost": country.shipping_cost,
                    "tax_rate": country.tax_rate,
                    "demand_level": round(country.demand_level, 2),
                    "notes": country.notes,
                }
                for country in self.countries
            ],
            "selling_sites": [
                {
                    "name": site.name,
                    "fee_rate": site.fee_rate,
                    "traffic": site.traffic,
                    "trust": site.trust,
                    "notes": site.notes,
                }
                for site in self.selling_sites
            ],
            "recent_sales": [
                {
                    "day": sale.day,
                    "product": sale.product,
                    "quantity": sale.quantity,
                    "revenue": round(sale.revenue, 2),
                    "cost": round(sale.cost, 2),
                    "profit": round(sale.profit, 2),
                }
                for sale in self.tracker.sales[-5:]
            ],
        }

    def get_ai_advice(self) -> str:
        return self.advisor.get_advice(self.snapshot())

    def _calculate_sale(
        self,
        product: str,
        site: SellingSite,
        country: Country,
        quantity: int,
    ) -> tuple[float, float, float]:
        selling_price = site.calculate_price(get_base_price(product), country)
        revenue = selling_price * quantity
        unit_cost = get_unit_cost(self.manufacturers, product)
        total_cost = (
            unit_cost * quantity
            + country.calculate_shipping(quantity)
            + country.calculate_taxes(revenue)
            + site.calculate_fee(revenue)
        )
        profit = revenue - total_cost
        return revenue, total_cost, profit
