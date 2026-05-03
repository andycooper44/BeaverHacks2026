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
    current_day: int = 1
    notes: str = ""
    inventory: dict[str, int] = field(default_factory=dict)  # product -> quantity
    advisor: GeminiAdvisor = field(default_factory=GeminiAdvisor)

    def __post_init__(self):
        self._initialize_game_data()

    def _initialize_game_data(self):
        """Initialize game with sample data"""
        self.countries = create_default_countries()
        self.manufacturers = create_default_manufacturers()
        self.selling_sites = create_default_selling_sites()
        self.tracker.money = 1000.0

    def get_available_actions(self) -> list[str]:
        """Get list of available player actions"""
        actions = ["Buy Products", "Sell Products", "Check Inventory", "View Stats", "Advance Day"]
        if self.advisor.api_key:
            actions.append("Get AI Advice")
        return actions

    def buy_products(self, manufacturer_name: str, quantity: int) -> str:
        """Buy products from a manufacturer"""
        manufacturer = find_manufacturer(self.manufacturers, manufacturer_name)
        if not manufacturer:
            return f"Manufacturer {manufacturer_name} not found."

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
        """Sell products on a site to a country"""
        if product not in self.inventory or self.inventory[product] < quantity:
            return f"Not enough {product} in inventory. Have: {self.inventory.get(product, 0)}"

        site = find_selling_site(self.selling_sites, site_name)
        country = find_country(self.countries, country_name)

        if not site or not country:
            return "Invalid site or country."

        selling_price = site.calculate_price(get_base_price(product), country)
        revenue = selling_price * quantity
        site_fees = site.calculate_fee(revenue)
        shipping = country.calculate_shipping(quantity)
        taxes = country.calculate_taxes(revenue)
        unit_cost = get_unit_cost(self.manufacturers, product)
        total_cost = (unit_cost * quantity) + shipping + taxes + site_fees
        profit = revenue - total_cost

        self.inventory[product] -= quantity
        sale = SaleRecord(product, quantity, revenue, total_cost, profit)
        self.tracker.record_sale(sale)

        return f"Sold {quantity} {product}(s) for ${revenue:.2f} profit. Total profit: ${profit:.2f}"

    def advance_day(self) -> str:
        """Advance to next day, update market conditions"""
        self.current_day += 1

        for country in self.countries:
            country.update_demand()

        for manufacturer in self.manufacturers:
            manufacturer.restock()

        return f"Advanced to day {self.current_day}. Market conditions have changed."

    def get_game_status(self) -> str:
        """Get current game status summary"""
        status = f"""
Day: {self.current_day}
Money: ${self.tracker.money:.2f}
Total Sales: {self.tracker.total_sales}
Total Profit: ${self.tracker.total_profit:.2f}

Inventory:
"""
        for product, qty in self.inventory.items():
            status += f"- {product}: {qty}\n"

        return status.strip()

    def get_ai_advice(self) -> str:
        """Get AI-powered business advice"""
        game_state = f"""
Day: {self.current_day}
Money: ${self.tracker.money:.2f}
Inventory: {self.inventory}
Total Profit: ${self.tracker.total_profit:.2f}
Recent sales: {len(self.tracker.sales)} transactions
"""
        return self.advisor.get_advice(game_state)
