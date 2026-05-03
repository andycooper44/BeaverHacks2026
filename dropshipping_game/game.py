from dataclasses import dataclass, field
import random

from dropshipping_game.countries import Country
from dropshipping_game.manufacturers import Manufacturer
from dropshipping_game.selling_sites import SellingSite
from dropshipping_game.tracker import SalesTracker
from dropshipping_game.gemini_client import GeminiAdvisor


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
        # Countries
        self.countries = [
            Country("USA", 5.0, 0.08, 0.9, "High demand, expensive shipping"),
            Country("China", 15.0, 0.05, 0.7, "Cheap manufacturing, long shipping"),
            Country("Germany", 8.0, 0.19, 0.8, "Quality focus, high taxes"),
            Country("Brazil", 12.0, 0.12, 0.6, "Growing market, variable shipping"),
        ]

        # Manufacturers
        self.manufacturers = [
            Manufacturer("TechCorp", "Smartphone", 200.0, 1000, 0.85, "Reliable electronics"),
            Manufacturer("FashionHub", "T-Shirt", 15.0, 5000, 0.7, "Trendy clothing"),
            Manufacturer("HomeGoods Inc", "Coffee Maker", 45.0, 2000, 0.8, "Quality appliances"),
            Manufacturer("ToyWorld", "Action Figure", 8.0, 8000, 0.6, "Fun toys"),
        ]

        # Selling Sites
        self.selling_sites = [
            SellingSite("Amazon", 0.15, 0.95, 0.9, "High traffic, high fees"),
            SellingSite("eBay", 0.10, 0.8, 0.7, "Auction style, moderate fees"),
            SellingSite("Shopify Store", 0.05, 0.6, 0.8, "Your own store, low fees"),
            SellingSite("Facebook Marketplace", 0.03, 0.7, 0.6, "Local sales, low fees"),
        ]

        # Starting money
        self.tracker.money = 1000.0

    def get_available_actions(self) -> list[str]:
        """Get list of available player actions"""
        actions = ["Buy Products", "Sell Products", "Check Inventory", "View Stats", "Advance Day"]
        return actions

    def buy_products(self, manufacturer_name: str, quantity: int) -> str:
        """Buy products from a manufacturer"""
        manufacturer = next((m for m in self.manufacturers if m.name == manufacturer_name), None)
        if not manufacturer:
            return f"Manufacturer {manufacturer_name} not found."

        if quantity > manufacturer.stock:
            return f"Not enough stock. Available: {manufacturer.stock}"

        total_cost = manufacturer.unit_cost * quantity
        if total_cost > self.tracker.money:
            return f"Not enough money. Need ${total_cost:.2f}, have ${self.tracker.money:.2f}"

        # Make purchase
        manufacturer.stock -= quantity
        self.tracker.money -= total_cost
        self.inventory[manufacturer.product] = self.inventory.get(manufacturer.product, 0) + quantity

        return f"Bought {quantity} {manufacturer.product}(s) for ${total_cost:.2f}"

    def sell_products(self, product: str, site_name: str, country_name: str, quantity: int) -> str:
        """Sell products on a site to a country"""
        if product not in self.inventory or self.inventory[product] < quantity:
            return f"Not enough {product} in inventory. Have: {self.inventory.get(product, 0)}"

        site = next((s for s in self.selling_sites if s.name == site_name), None)
        country = next((c for c in self.countries if c.name == country_name), None)

        if not site or not country:
            return "Invalid site or country."

        # Calculate pricing and costs
        base_price = self._get_base_price(product)
        demand_multiplier = country.demand_level * site.traffic
        selling_price = base_price * demand_multiplier * (0.8 + random.random() * 0.4)  # Random variation

        revenue = selling_price * quantity
        site_fees = revenue * site.fee_rate
        shipping = country.shipping_cost * quantity
        taxes = revenue * country.tax_rate
        unit_cost = self._get_unit_cost(product)
        total_cost = (unit_cost * quantity) + shipping + taxes + site_fees

        profit = revenue - total_cost

        # Update inventory and tracker
        self.inventory[product] -= quantity
        self.tracker.money += profit
        self.tracker.total_sales += quantity
        self.tracker.total_revenue += revenue
        self.tracker.total_profit += profit

        # Record sale
        from dropshipping_game.tracker import SaleRecord
        sale = SaleRecord(product, quantity, revenue, total_cost, profit)
        self.tracker.sales.append(sale)

        return f"Sold {quantity} {product}(s) for ${revenue:.2f} profit. Total profit: ${profit:.2f}"

    def _get_base_price(self, product: str) -> float:
        """Get base selling price for a product"""
        prices = {
            "Smartphone": 400.0,
            "T-Shirt": 25.0,
            "Coffee Maker": 80.0,
            "Action Figure": 15.0,
        }
        return prices.get(product, 50.0)

    def _get_unit_cost(self, product: str) -> float:
        """Get unit cost for a product"""
        for m in self.manufacturers:
            if m.product == product:
                return m.unit_cost
        return 10.0

    def advance_day(self) -> str:
        """Advance to next day, update market conditions"""
        self.current_day += 1

        # Random market changes
        for country in self.countries:
            country.demand_level *= 0.95 + random.random() * 0.1  # Slight variation
            country.demand_level = max(0.1, min(1.0, country.demand_level))

        for manufacturer in self.manufacturers:
            # Restock some inventory
            manufacturer.stock += random.randint(0, 100)

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
