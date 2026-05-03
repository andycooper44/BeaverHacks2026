from dropshipping_game.game import DropshippingGame
from dropshipping_game.countries import Country
from dropshipping_game.manufacturers import Manufacturer
from dropshipping_game.selling_sites import SellingSite
from dropshipping_game.gemini_client import GeminiAdvisor
import os


def create_sample_game() -> DropshippingGame:
    """Create a game with sample data for testing."""
    game = DropshippingGame()

    # Sample countries
    game.countries = [
        Country(name="USA", shipping_cost=5.99, tax_rate=0.08, demand_level=8.5, notes="High demand, fast shipping"),
        Country(name="Canada", shipping_cost=8.50, tax_rate=0.12, demand_level=7.2, notes="Good market, higher taxes"),
        Country(name="UK", shipping_cost=12.00, tax_rate=0.20, demand_level=6.8, notes="Premium market"),
    ]

    # Sample manufacturers
    game.manufacturers = [
        Manufacturer(name="TechCorp", product="Wireless Earbuds", unit_cost=25.00, stock=50, quality=9.2, notes="Premium audio"),
        Manufacturer(name="GadgetPro", product="Smart Watch", unit_cost=90.00, stock=25, quality=8.8, notes="Fitness tracking"),
        Manufacturer(name="CaseMaker", product="Phone Case", unit_cost=5.00, stock=200, quality=7.5, notes="Bulk supplier"),
    ]

    # Sample selling sites
    game.selling_sites = [
        SellingSite(name="Amazon", fee_rate=0.15, traffic=10.0, trust=9.5, notes="High traffic"),
        SellingSite(name="eBay", fee_rate=0.10, traffic=7.5, trust=8.2, notes="Auction style"),
        SellingSite(name="Shopify Store", fee_rate=0.02, traffic=3.2, trust=9.8, notes="Your own store"),
    ]

    game.tracker.money = 1000.00  # Starting money
    game.notes = "Welcome to your dropshipping business!"

    return game


def demo_gameplay():
    """Demonstrate the game functionality."""
    print("🚀 Dropshipping Game Demo\n")

    # Create game
    game = create_sample_game()
    print("Initial game state:")
    print(game.get_game_summary())
    print()

    # Test buying inventory
    print("Testing inventory purchase...")
    success, message = game.buy_inventory(game.manufacturers[0], 20)  # Buy 20 earbuds
    print(f"Result: {message}")
    print(f"Money after purchase: ${game.tracker.money:.2f}")
    print()

    # Test manual sale
    print("Testing manual sale...")
    success, message = game.sell_product(
        manufacturer=game.manufacturers[0],
        quantity=5,
        selling_price=75.00,  # Sell at $75 each
        country=game.countries[0],  # USA
        site=game.selling_sites[0]  # Amazon
    )
    print(f"Result: {message}")
    print()

    # Advance a few days to simulate sales
    print("Advancing days and simulating sales...")
    for day in range(3):
        summary = game.advance_day()
        print(f"Day {game.current_day}: {summary}")
        print(f"Money: ${game.tracker.money:.2f}, Stock: {game.manufacturers[0].stock}")
    print()

    # Show final state
    print("Final game state:")
    print(game.get_game_summary())
    print()

    # Test Gemini AI (fallback works without an API key)
    api_key = os.getenv("GEMINI_API_KEY", "")
    advisor = GeminiAdvisor(api_key=api_key)
    print("🤖 Gemini advisor is active. Using sample advice locally while Gemini is disabled.")

    # Convert game state to dict for AI
    game_state = {
        "current_day": game.current_day,
        "money": game.tracker.money,
        "total_sales": game.tracker.total_sales,
        "total_revenue": game.tracker.total_revenue,
        "total_profit": game.tracker.total_profit,
        "countries": [{"name": c.name, "demand_level": c.demand_level, "shipping_cost": c.shipping_cost, "tax_rate": c.tax_rate} for c in game.countries],
        "manufacturers": [{"name": m.name, "product": m.product, "unit_cost": m.unit_cost, "stock": m.stock, "quality": m.quality} for m in game.manufacturers],
        "selling_sites": [{"name": s.name, "fee_rate": s.fee_rate, "traffic": s.traffic, "trust": s.trust} for s in game.selling_sites],
        "recent_sales": [{"product": s.product, "quantity": s.quantity, "revenue": s.revenue, "profit": s.profit} for s in game.tracker.sales[-3:]],
        "notes": game.notes
    }

    advice = advisor.get_business_advice(game_state)
    print(f"AI Advice: {advice[:500]}..." if len(advice) > 500 else f"AI Advice: {advice}")


if __name__ == "__main__":
    demo_gameplay()
