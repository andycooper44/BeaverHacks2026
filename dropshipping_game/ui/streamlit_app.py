import os
import sys

# Ensure the project root is on sys.path when Streamlit runs this module.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from dropshipping_game.game import DropshippingGame
from dropshipping_game.countries import Country
from dropshipping_game.manufacturers import Manufacturer
from dropshipping_game.selling_sites import SellingSite
from dropshipping_game.tracker import SaleRecord


# Create sample game data
def create_sample_game() -> DropshippingGame:
    game = DropshippingGame()
    game.current_day = 15
    game.tracker.money = 2500.00
    game.tracker.total_sales = 45
    game.tracker.total_revenue = 3200.00
    game.tracker.total_profit = 1200.00

    # Sample sales
    game.tracker.sales = [
        SaleRecord(product="Wireless Earbuds", quantity=5, revenue=250.00, cost=125.00, profit=125.00),
        SaleRecord(product="Smart Watch", quantity=2, revenue=400.00, cost=180.00, profit=220.00),
        SaleRecord(product="Phone Case", quantity=10, revenue=150.00, cost=50.00, profit=100.00),
        SaleRecord(product="Laptop Stand", quantity=3, revenue=120.00, cost=60.00, profit=60.00),
    ]

    # Sample countries
    game.countries = [
        Country(name="USA", shipping_cost=5.99, tax_rate=0.08, demand_level=8.5, notes="High demand, fast shipping"),
        Country(name="Canada", shipping_cost=8.50, tax_rate=0.12, demand_level=7.2, notes="Good market, higher taxes"),
        Country(name="UK", shipping_cost=12.00, tax_rate=0.20, demand_level=6.8, notes="Premium market, Brexit impacts"),
    ]

    # Sample manufacturers
    game.manufacturers = [
        Manufacturer(name="TechCorp", product="Wireless Earbuds", unit_cost=25.00, stock=150, quality=9.2, notes="Reliable supplier, good quality"),
        Manufacturer(name="GadgetPro", product="Smart Watch", unit_cost=90.00, stock=75, quality=8.8, notes="Premium products, higher cost"),
        Manufacturer(name="CaseMaker", product="Phone Case", unit_cost=5.00, stock=500, quality=7.5, notes="Bulk supplier, basic quality"),
    ]

    # Sample selling sites
    game.selling_sites = [
        SellingSite(name="Amazon", fee_rate=0.15, traffic=10.0, trust=9.5, notes="High traffic, platform fees"),
        SellingSite(name="eBay", fee_rate=0.10, traffic=7.5, trust=8.2, notes="Auction style, good reach"),
        SellingSite(name="Shopify Store", fee_rate=0.02, traffic=3.2, trust=9.8, notes="Your own store, low fees"),
    ]

    game.notes = "Sample dropshipping game data. Start with $2500 and build your business!"

    return game


game: DropshippingGame = create_sample_game()


def main() -> None:
    st.title("🚀 Dropshipping Game")

    # Game Overview
    st.header("📊 Game Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Day", game.current_day)
    with col2:
        st.metric("Money", f"${game.tracker.money:.2f}")
    with col3:
        st.metric("Total Profit", f"${game.tracker.total_profit:.2f}")

    # Sales Tracker
    st.header("💰 Sales Tracker")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Sales", game.tracker.total_sales)
        st.metric("Total Revenue", f"${game.tracker.total_revenue:.2f}")
    with col2:
        st.metric("Total Profit", f"${game.tracker.total_profit:.2f}")

    if game.tracker.sales:
        st.subheader("Recent Sales")
        sales_df = [
            {
                "Product": sale.product,
                "Quantity": sale.quantity,
                "Revenue": f"${sale.revenue:.2f}",
                "Cost": f"${sale.cost:.2f}",
                "Profit": f"${sale.profit:.2f}"
            }
            for sale in game.tracker.sales[-5:]  # Show last 5 sales
        ]
        st.table(sales_df)
    else:
        st.info("No sales recorded yet.")

    # Countries
    if game.countries:
        st.header("🌍 Countries")
        for country in game.countries:
            with st.expander(f"📍 {country.name}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Shipping Cost", f"${country.shipping_cost:.2f}")
                with col2:
                    st.metric("Tax Rate", f"{country.tax_rate:.1%}")
                with col3:
                    st.metric("Demand Level", f"{country.demand_level:.1f}")
                if country.notes:
                    st.write(f"**Notes:** {country.notes}")

    # Manufacturers
    if game.manufacturers:
        st.header("🏭 Manufacturers")
        for manufacturer in game.manufacturers:
            with st.expander(f"🏭 {manufacturer.name}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Product", manufacturer.product)
                    st.metric("Unit Cost", f"${manufacturer.unit_cost:.2f}")
                with col2:
                    st.metric("Stock", manufacturer.stock)
                with col3:
                    st.metric("Quality", f"{manufacturer.quality:.1f}")
                if manufacturer.notes:
                    st.write(f"**Notes:** {manufacturer.notes}")

    # Selling Sites
    if game.selling_sites:
        st.header("🛒 Selling Sites")
        for site in game.selling_sites:
            with st.expander(f"🛒 {site.name}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Fee Rate", f"{site.fee_rate:.1%}")
                with col2:
                    st.metric("Traffic", f"{site.traffic:.1f}")
                with col3:
                    st.metric("Trust", f"{site.trust:.1f}")
                if site.notes:
                    st.write(f"**Notes:** {site.notes}")

    # Notes
    if game.notes:
        st.header("📝 Game Notes")
        st.write(game.notes)


if __name__ == "__main__":
    main()
