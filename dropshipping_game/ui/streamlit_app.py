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

if 'day_summary' not in st.session_state:
    st.session_state.day_summary = ""

if 'tutorial_step' not in st.session_state:
    st.session_state.tutorial_step = 1  # Start tutorial on first load

game: DropshippingGame = st.session_state.game
advisor: GeminiAdvisor = st.session_state.advisor


def main() -> None:
    # Tutorial dialogs
    if st.session_state.tutorial_step == 1:
        @st.dialog("Welcome to Dropshipping Empire! 🎉")
        def tutorial_step_1():
            st.write("Welcome to your dropshipping business simulation!")
            st.write("This tutorial will guide you through the game features.")
            st.write("Click 'Next' to continue.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Next", key="tut_next_1"):
                    st.session_state.tutorial_step = 2
                    st.rerun()
            with col2:
                if st.button("Skip Tutorial", key="tut_skip"):
                    st.session_state.tutorial_step = 0
                    st.rerun()
        tutorial_step_1()

    elif st.session_state.tutorial_step == 2:
        @st.dialog("Business Overview 📊")
        def tutorial_step_2():
            st.write("This section shows your current business status:")
            st.write("- **Day**: How many days you've been running the business")
            st.write("- **Money**: Your current cash balance")
            st.write("- **Total Sales**: Units sold so far")
            st.write("- **Total Profit**: Overall profit made")
            if st.button("Next", key="tut_next_2"):
                st.session_state.tutorial_step = 3
                st.rerun()
        tutorial_step_2()

    elif st.session_state.tutorial_step == 3:
        @st.dialog("Game Actions 🎮")
        def tutorial_step_3():
            st.write("The sidebar contains your main game actions:")
            st.write("- **Advance Day**: Simulate a day passing with automatic sales and events")
            st.write("- **Buy Inventory**: Purchase products from manufacturers")
            st.write("- **Manual Sale**: Sell products directly at custom prices")
            if st.button("Next", key="tut_next_3"):
                st.session_state.tutorial_step = 4
                st.rerun()
        tutorial_step_3()

    elif st.session_state.tutorial_step == 4:
        @st.dialog("Buying Inventory 🛒")
        def tutorial_step_4():
            st.write("To buy inventory:")
            st.write("1. Select a manufacturer from the dropdown")
            st.write("2. Choose the quantity you want to buy")
            st.write("3. Check the total cost")
            st.write("4. Click 'Purchase' if you have enough money")
            st.write("Products will be added to your stock for selling.")
            if st.button("Next", key="tut_next_4"):
                st.session_state.tutorial_step = 5
                st.rerun()
        tutorial_step_4()

    elif st.session_state.tutorial_step == 5:
        @st.dialog("Manual Sales 💸")
        def tutorial_step_5():
            st.write("To make a manual sale:")
            st.write("1. Select the product (manufacturer)")
            st.write("2. Choose quantity to sell (can't exceed stock)")
            st.write("3. Set your selling price per unit")
            st.write("4. Pick the country (affects shipping/tax)")
            st.write("5. Choose the sales platform (affects fees)")
            st.write("6. Click 'Sell' to complete the transaction")
            if st.button("Next", key="tut_next_5"):
                st.session_state.tutorial_step = 6
                st.rerun()
        tutorial_step_5()

    elif st.session_state.tutorial_step == 6:
        @st.dialog("Markets 🌍")
        def tutorial_step_6():
            st.write("Markets (Countries) have different characteristics:")
            st.write("- **Demand Level**: How much people want to buy (higher = more sales)")
            st.write("- **Shipping Cost**: Cost to ship per unit")
            st.write("- **Tax Rate**: Percentage tax on sales")
            st.write("Choose countries that match your strategy!")
            if st.button("Next", key="tut_next_6"):
                st.session_state.tutorial_step = 7
                st.rerun()
        tutorial_step_6()

    elif st.session_state.tutorial_step == 7:
        @st.dialog("Suppliers 🏭")
        def tutorial_step_7():
            st.write("Manufacturers supply your products:")
            st.write("- **Unit Cost**: Price to buy each item")
            st.write("- **Stock**: How many you currently have")
            st.write("- **Quality**: Affects automatic sales (higher = better)")
            st.write("Buy from suppliers with good quality-to-cost ratios!")
            if st.button("Next", key="tut_next_7"):
                st.session_state.tutorial_step = 8
                st.rerun()
        tutorial_step_7()

    elif st.session_state.tutorial_step == 8:
        @st.dialog("Sales Platforms 🛒")
        def tutorial_step_8():
            st.write("Platforms where you sell products:")
            st.write("- **Fee Rate**: Commission they take per sale")
            st.write("- **Traffic**: How many potential customers (higher = more sales)")
            st.write("- **Trust**: Customer confidence (affects conversions)")
            st.write("Balance fees vs. traffic when choosing platforms!")
            if st.button("Next", key="tut_next_8"):
                st.session_state.tutorial_step = 9
                st.rerun()
        tutorial_step_8()

    elif st.session_state.tutorial_step == 9:
        @st.dialog("AI Business Advisor 🤖")
        def tutorial_step_9():
            st.write("The AI advisor can help you:")
            st.write("- Get business advice based on your current state")
            st.write("- Analyze market conditions")
            st.write("- Answer specific strategy questions")
            st.write("Set GEMINI_API_KEY for real AI, otherwise uses sample advice.")
            if st.button("Next", key="tut_next_9"):
                st.session_state.tutorial_step = 10
                st.rerun()
        tutorial_step_9()

    elif st.session_state.tutorial_step == 10:
        @st.dialog("Gameplay Loop 🔄")
        def tutorial_step_10():
            st.write("The main gameplay loop:")
            st.write("1. **Buy inventory** from manufacturers")
            st.write("2. **Advance day** to simulate sales and events")
            st.write("3. **Check results** in Business Overview")
            st.write("4. **Make manual sales** for extra profit")
            st.write("5. **Use AI advisor** for strategy tips")
            st.write("6. Repeat and grow your business!")
            st.write("Events happen randomly each day - adapt your strategy!")
            if st.button("Start Playing!", key="tut_finish"):
                st.session_state.tutorial_step = 0  # End tutorial
                st.rerun()
        tutorial_step_10()

    st.title("🚀 Dropshipping Empire")

    # Sidebar for actions
    with st.sidebar:
        st.header("🎮 Game Actions")

        if st.button("📚 Tutorial", key="restart_tutorial"):
            st.session_state.tutorial_step = 1
            st.rerun()

        st.divider()

        if st.button("⏭️ Advance Day", type="primary"):
            with st.spinner("Processing day..."):
                st.session_state.day_summary = game.advance_day()
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
        manufacturer_names_with_stock = [m.name for m in game.manufacturers if m.stock > 0]
        if manufacturer_names_with_stock and game.countries and game.selling_sites:
            sale_manufacturer = st.selectbox(
                "Product",
                manufacturer_names_with_stock,
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
    if st.session_state.day_summary:
        st.info(st.session_state.day_summary)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Day", game.current_day)
    with col2:
        st.metric("Money", f"${game.tracker.money:.2f}")
    with col3:
        st.metric("Total Sales", game.tracker.total_sales)
    with col4:
        st.metric("Total Profit", f"${game.tracker.total_profit:.2f}")
    with col5:
        st.metric("Days Until Rent", game.days_until_rent)

    # Sales Tracker
    if game.tracker.sales:
        st.header("💰 Recent Sales")
        sales_df = [
            {
                "Day": sale.day,
                "Product": sale.product,
                "Quantity": sale.quantity,
                "Revenue": f"${sale.revenue:.2f}",
                "Cost": f"${sale.cost:.2f}",
                "Profit": f"${sale.profit:.2f}"
            }
            for sale in game.tracker.sales[-10:]  # Show last 10 sales
        ]
        st.dataframe(sales_df, use_container_width=True)

        # Sales Chart
        st.subheader("📈 Profit Over Time")
        # Aggregate profit by day
        profit_by_day = {}
        for sale in game.tracker.sales:
            profit_by_day[sale.day] = profit_by_day.get(sale.day, 0) + sale.profit

        if profit_by_day:
            days = sorted(profit_by_day.keys())
            profits = [profit_by_day[day] for day in days]
            chart_data = {"Day": days, "Daily Profit": profits}
            st.line_chart(chart_data, x="Day", y="Daily Profit")
        else:
            st.write("No sales data yet.")

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
    if advisor.api_key:
        st.header("🤖 AI Business Advisor")

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
    else:
        st.header("🤖 AI Advisor")
        st.info("Set GEMINI_API_KEY environment variable to enable AI business advice.")

    # Notes
    if game.notes:
        st.header("📝 Business Notes")
        st.write(game.notes)


if __name__ == "__main__":
    main()
