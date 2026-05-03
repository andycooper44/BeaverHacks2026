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
from dropshipping_game.gemini_client import GeminiAdvisor


# Create sample game data
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


# Initialize game state in session
if 'game' not in st.session_state:
    st.session_state.game = create_sample_game()

if 'advisor' not in st.session_state:
    api_key = os.getenv("GEMINI_API_KEY", "")
    st.session_state.advisor = GeminiAdvisor(api_key=api_key)

game: DropshippingGame = st.session_state.game
advisor: GeminiAdvisor = st.session_state.advisor


def main() -> None:
    st.title("🚀 Dropshipping Empire")

    # Sidebar for actions
    with st.sidebar:
        st.header("🎮 Game Actions")

        if st.button("⏭️ Advance Day", type="primary"):
            with st.spinner("Processing day..."):
                summary = game.advance_day()
                st.success(summary)
                st.rerun()

        st.divider()

        # Buy inventory section
        st.subheader("🛒 Buy Inventory")
        manufacturer_names = [m.name for m in game.manufacturers]
        if manufacturer_names:
            selected_manufacturer = st.selectbox(
                "Select Manufacturer",
                manufacturer_names,
                key="buy_manufacturer"
            )
            manufacturer = next(m for m in game.manufacturers if m.name == selected_manufacturer)

            col1, col2 = st.columns(2)
            with col1:
                quantity = st.number_input("Quantity", min_value=1, value=10, key="buy_quantity")
            with col2:
                total_cost = manufacturer.unit_cost * quantity
                st.metric("Total Cost", f"${total_cost:.2f}")

            if st.button("💰 Purchase", key="buy_button"):
                success, message = game.buy_inventory(manufacturer, quantity)
                if success:
                    st.success(message)
                else:
                    st.error(message)
                st.rerun()

        st.divider()

        # Manual sale section
        st.subheader("💸 Manual Sale")
        if manufacturer_names and game.countries and game.selling_sites:
            sale_manufacturer = st.selectbox(
                "Product",
                manufacturer_names,
                key="sale_manufacturer"
            )
            manufacturer = next(m for m in game.manufacturers if m.name == sale_manufacturer)

            col1, col2 = st.columns(2)
            with col1:
                sale_quantity = st.number_input("Quantity", min_value=1, max_value=manufacturer.stock, value=min(5, manufacturer.stock), key="sale_quantity")
                sale_price = st.number_input("Price per unit", min_value=0.01, value=float(manufacturer.unit_cost * 3), key="sale_price")
            with col2:
                country_names = [c.name for c in game.countries]
                selected_country = st.selectbox("Country", country_names, key="sale_country")
                site_names = [s.name for s in game.selling_sites]
                selected_site = st.selectbox("Platform", site_names, key="sale_site")

            if st.button("🛍️ Sell", key="sell_button"):
                country = next(c for c in game.countries if c.name == selected_country)
                site = next(s for s in game.selling_sites if s.name == selected_site)

                success, message = game.sell_product(manufacturer, sale_quantity, sale_price, country, site)
                if success:
                    st.success(message)
                else:
                    st.error(message)
                st.rerun()

    # Main content
    # Game Overview
    st.header("📊 Business Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Day", game.current_day)
    with col2:
        st.metric("Money", f"${game.tracker.money:.2f}")
    with col3:
        st.metric("Total Sales", game.tracker.total_sales)
    with col4:
        st.metric("Total Profit", f"${game.tracker.total_profit:.2f}")

    # Sales Tracker
    if game.tracker.sales:
        st.header("💰 Recent Sales")
        sales_df = [
            {
                "Product": sale.product,
                "Quantity": sale.quantity,
                "Revenue": f"${sale.revenue:.2f}",
                "Cost": f"${sale.cost:.2f}",
                "Profit": f"${sale.profit:.2f}"
            }
            for sale in game.tracker.sales[-10:]  # Show last 10 sales
        ]
        st.dataframe(sales_df, use_container_width=True)

    # Countries
    if game.countries:
        st.header("🌍 Markets")
        cols = st.columns(min(3, len(game.countries)))
        for i, country in enumerate(game.countries):
            with cols[i % len(cols)]:
                with st.expander(f"📍 {country.name}"):
                    st.metric("Demand Level", f"{country.demand_level:.1f}")
                    st.metric("Shipping Cost", f"${country.shipping_cost:.2f}")
                    st.metric("Tax Rate", f"{country.tax_rate:.1%}")
                    if country.notes:
                        st.caption(country.notes)

    # Manufacturers
    if game.manufacturers:
        st.header("🏭 Suppliers")
        cols = st.columns(min(3, len(game.manufacturers)))
        for i, manufacturer in enumerate(game.manufacturers):
            with cols[i % len(cols)]:
                with st.expander(f"🏭 {manufacturer.name}"):
                    st.metric("Product", manufacturer.product)
                    st.metric("Unit Cost", f"${manufacturer.unit_cost:.2f}")
                    st.metric("Stock", manufacturer.stock)
                    st.metric("Quality", f"{manufacturer.quality:.1f}")
                    if manufacturer.notes:
                        st.caption(manufacturer.notes)

    # Selling Sites
    if game.selling_sites:
        st.header("🛒 Sales Platforms")
        cols = st.columns(min(3, len(game.selling_sites)))
        for i, site in enumerate(game.selling_sites):
            with cols[i % len(cols)]:
                with st.expander(f"🛒 {site.name}"):
                    st.metric("Fee Rate", f"{site.fee_rate:.1%}")
                    st.metric("Traffic", f"{site.traffic:.1f}")
                    st.metric("Trust", f"{site.trust:.1f}")
                    if site.notes:
                        st.caption(site.notes)

    # AI Advisor
    st.header("🤖 AI Business Advisor")
    if not advisor._use_api():
        st.info("Gemini is not configured, so this app is using sample/local advice instead.")

    # Get current game state for AI
    game_state = {
        "current_day": game.current_day,
        "money": game.tracker.money,
        "total_sales": game.tracker.total_sales,
        "total_revenue": game.tracker.total_revenue,
        "total_profit": game.tracker.total_profit,
        "countries": [{"name": c.name, "demand_level": c.demand_level, "shipping_cost": c.shipping_cost, "tax_rate": c.tax_rate} for c in game.countries],
        "manufacturers": [{"name": m.name, "product": m.product, "unit_cost": m.unit_cost, "stock": m.stock, "quality": m.quality} for m in game.manufacturers],
        "selling_sites": [{"name": s.name, "fee_rate": s.fee_rate, "traffic": s.traffic, "trust": s.trust} for s in game.selling_sites],
        "recent_sales": [{"product": s.product, "quantity": s.quantity, "revenue": s.revenue, "profit": s.profit} for s in game.tracker.sales[-5:]],
        "notes": game.notes
    }

    if st.button("🎯 Get Business Advice", key="ai_advice"):
        with st.spinner("Getting AI insights..."):
            advice = advisor.get_business_advice(game_state)
            st.write(advice)

    if st.button("📊 Market Analysis", key="market_analysis"):
        with st.spinner("Analyzing market conditions..."):
            analysis = advisor.get_market_analysis(game_state)
            st.write(analysis)

    # Custom question
    custom_question = st.text_input("Ask the AI advisor a specific question:", key="custom_question")
    if st.button("❓ Ask AI", key="ask_ai") and custom_question:
        with st.spinner("Getting personalized advice..."):
            answer = advisor.get_strategy_recommendation(game_state, custom_question)
            st.write(f"**Q:** {custom_question}")
            st.write(f"**A:** {answer}")

    # Notes
    if game.notes:
        st.header("📝 Business Notes")
        st.write(game.notes)


if __name__ == "__main__":
    main()
