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
    rent_amount: float = 500.0
    days_until_rent: int = 7

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

        # Handle rent
        self.days_until_rent -= 1
        if self.days_until_rent <= 0:
            if self.tracker.money >= self.rent_amount:
                self.tracker.money -= self.rent_amount
                events.append(f"Rent paid: ${self.rent_amount:.2f}")
                self.days_until_rent = 7  # Reset countdown
            else:
                events.append(f"Rent due but insufficient funds! Owed ${self.rent_amount:.2f}, have ${self.tracker.money:.2f}. Game over!")
                # Could add game over logic here

        summary = f"Day {self.current_day} complete. " + " | ".join(events) if events else f"Day {self.current_day} complete. No sales today."
        return summary

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
        manufacturer.stock += quantity
        return True, f"Successfully purchased {quantity} units of {manufacturer.product} for ${total_cost:.2f}"

    def sell_product(self, manufacturer: Manufacturer, quantity: int, selling_price: float, country: Country, site: SellingSite) -> tuple[bool, str]:
        """Manually sell products. Returns (success, message)."""
        if quantity <= 0:
            return False, "Quantity must be positive"

        if manufacturer.stock < quantity:
            return False, f"Insufficient stock. Have {manufacturer.stock}, need {quantity}"

        # Calculate costs and revenue
        unit_cost = manufacturer.unit_cost
        shipping_cost = country.shipping_cost
        tax_amount = selling_price * country.tax_rate
        site_fee = selling_price * site.fee_rate

        total_cost_per_unit = unit_cost + shipping_cost + tax_amount + site_fee
        total_revenue = selling_price * quantity
        total_cost = total_cost_per_unit * quantity
        profit = total_revenue - total_cost

        # Record the sale
        sale = SaleRecord(
            product=manufacturer.product,
            quantity=quantity,
            revenue=total_revenue,
            cost=total_cost,
            profit=profit,
            day=self.current_day
        )

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

        return True, f"Sold {quantity} units for ${total_revenue:.2f} profit. Money: ${self.tracker.money:.2f}"

    def _simulate_sales_for_manufacturer(self, manufacturer: Manufacturer) -> int:
        """Simulate automatic sales for a manufacturer. Returns units sold."""
        if not self.countries or not self.selling_sites:
            return 0

        # Simple sales simulation based on various factors
        base_demand = sum(country.demand_level for country in self.countries) / len(self.countries)
        quality_factor = manufacturer.quality / 10.0
        traffic_factor = sum(site.traffic for site in self.selling_sites) / len(self.selling_sites) / 10.0

        # Random factor for unpredictability
        random_factor = random.uniform(0.5, 1.5)

        # Calculate potential sales
        potential_sales = int(base_demand * quality_factor * traffic_factor * random_factor)

        # Limit by available stock
        actual_sales = min(potential_sales, manufacturer.stock)

        if actual_sales > 0:
            # Simulate selling at a reasonable price
            avg_country = self.countries[0]  # Use first country for simplicity
            avg_site = self.selling_sites[0]

            selling_price = manufacturer.unit_cost * random.uniform(2.0, 4.0)  # 2-4x markup

            # Calculate costs
            shipping_cost = avg_country.shipping_cost
            tax_amount = selling_price * avg_country.tax_rate
            site_fee = selling_price * avg_site.fee_rate

            total_cost_per_unit = manufacturer.unit_cost + shipping_cost + tax_amount + site_fee
            total_revenue = selling_price * actual_sales
            total_cost = total_cost_per_unit * actual_sales
            profit = total_revenue - total_cost

            # Record the sale
            sale = SaleRecord(
                product=manufacturer.product,
                quantity=actual_sales,
                revenue=total_revenue,
                cost=total_cost,
                profit=profit,
                day=self.current_day
            )

            self.tracker.sales.append(sale)
            self.tracker.total_sales += actual_sales
            self.tracker.total_revenue += total_revenue
            self.tracker.total_profit += profit
            self.tracker.money += profit

            manufacturer.stock -= actual_sales

        return actual_sales

    def _generate_random_event(self) -> str:
        """Generate a random event that affects the game."""
        events = [
            "Demand spike! Sales increased by 50% today.",
            "Supply chain delay. Manufacturer stock reduced by 20%.",
            "New competitor entered the market. Prices dropped 10%.",
            "Positive review went viral. Trust increased for all sites.",
            "Economic downturn. Demand decreased by 30%.",
            "Bulk discount opportunity. Unit costs reduced by 15%.",
            "Shipping strike. Shipping costs doubled.",
            "Tax audit. Extra taxes owed.",
            "Loyal customer bonus. Extra money received.",
            "Product recall. Lost some inventory."
        ]

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
Days until rent: {self.days_until_rent}
Manufacturers: {len(self.manufacturers)}
Countries: {len(self.countries)}
Selling Sites: {len(self.selling_sites)}"""
