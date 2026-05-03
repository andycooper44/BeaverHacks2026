from dataclasses import dataclass, field
import random
from typing import Optional

from dropshipping_game.countries import Country
from dropshipping_game.manufacturers import Manufacturer
from dropshipping_game.selling_sites import SellingSite
from dropshipping_game.tracker import SalesTracker, SaleRecord


@dataclass
class DropshippingGame:
    tracker: SalesTracker = field(default_factory=SalesTracker)
    countries: list[Country] = field(default_factory=list)
    manufacturers: list[Manufacturer] = field(default_factory=list)
    selling_sites: list[SellingSite] = field(default_factory=list)
    current_day: int = 0
    notes: str = ""
    rent_amount: float = 500.0
    days_until_rent: int = 7

    def advance_day(self) -> str:
        """Advance to the next day and simulate sales. Returns a summary of what happened."""
        self.current_day += 1
        events = []

        # Simulate sales for each manufacturer
        for manufacturer in self.manufacturers:
            if manufacturer.stock > 0:
                sales_made = self._simulate_sales_for_manufacturer(manufacturer)
                if sales_made > 0:
                    events.append(f"Sold {sales_made} units of {manufacturer.product}")

        # Random events
        if random.random() < 0.3:  # 30% chance of random event
            event = self._generate_random_event()
            events.append(event)

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

    def buy_inventory(self, manufacturer: Manufacturer, quantity: int) -> tuple[bool, str]:
        """Purchase inventory from a manufacturer. Returns (success, message)."""
        if quantity <= 0:
            return False, "Quantity must be positive"

        if manufacturer not in self.manufacturers:
            return False, "Manufacturer not found"

        total_cost = manufacturer.unit_cost * quantity
        if self.tracker.money < total_cost:
            return False, f"Insufficient funds. Need ${total_cost:.2f}, have ${self.tracker.money:.2f}"

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

        self.tracker.sales.append(sale)
        self.tracker.total_sales += quantity
        self.tracker.total_revenue += total_revenue
        self.tracker.total_profit += profit
        self.tracker.money += profit

        manufacturer.stock -= quantity

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

        event = random.choice(events)

        # Apply some effects based on the event
        if "Demand spike" in event:
            # Temporarily increase demand
            for country in self.countries:
                country.demand_level *= 1.5
        elif "Supply chain delay" in event:
            # Reduce stock
            for manufacturer in self.manufacturers:
                manufacturer.stock = int(manufacturer.stock * 0.8)
        elif "Bulk discount" in event:
            # Reduce costs
            for manufacturer in self.manufacturers:
                manufacturer.unit_cost *= 0.85
        elif "Shipping strike" in event:
            # Increase shipping costs
            for country in self.countries:
                country.shipping_cost *= 2.0
        elif "Economic downturn" in event:
            # Reduce demand
            for country in self.countries:
                country.demand_level *= 0.7

        return event

    def get_game_summary(self) -> str:
        """Get a summary of the current game state."""
        return f"""Day {self.current_day}
Money: ${self.tracker.money:.2f}
Total Sales: {self.tracker.total_sales}
Total Revenue: ${self.tracker.total_revenue:.2f}
Total Profit: ${self.tracker.total_profit:.2f}
Days until rent: {self.days_until_rent}
Manufacturers: {len(self.manufacturers)}
Countries: {len(self.countries)}
Selling Sites: {len(self.selling_sites)}"""
