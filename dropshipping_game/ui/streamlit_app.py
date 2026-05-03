import streamlit as st

from dropshipping_game.game import DropshippingGame
from dropshipping_game.gemini_client import GENAI_AVAILABLE


def main() -> None:
    st.title("🚚 Dropshipping Empire Game")

    # Initialize game in session state
    if 'game' not in st.session_state:
        st.session_state.game = DropshippingGame()

    game = st.session_state.game

    if game.advisor.api_key:
        if GENAI_AVAILABLE:
            st.success("🤖 Gemini AI advisor enabled")
        else:
            st.warning("Gemini API key set, but the required library is missing. Install google-genai.")
    else:
        st.info("Gemini AI advisor disabled. Set GEMINI_API_KEY to enable AI advice.")

    # Game status
    st.header("📊 Game Status")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Day", game.current_day)
        st.metric("Money", f"${game.tracker.money:.2f}")
    with col2:
        st.metric("Total Sales", game.tracker.total_sales)
        st.metric("Total Profit", f"${game.tracker.total_profit:.2f}")
    with col3:
        st.metric("Inventory Items", sum(game.inventory.values()))

    # Inventory
    if game.inventory:
        st.subheader("📦 Inventory")
        for product, qty in game.inventory.items():
            st.write(f"- {product}: {qty}")

    # Action selection
    st.header("🎯 Choose Action")
    actions = game.get_available_actions()
    action = st.selectbox("What would you like to do?", actions)

    if action == "Buy Products":
        st.subheader("🛒 Buy Products")
        col1, col2 = st.columns(2)

        with col1:
            manufacturer_options = [f"{m.name} - {m.product} (${m.unit_cost:.2f}, stock: {m.stock})" for m in game.manufacturers]
            selected_manufacturer = st.selectbox("Choose manufacturer:", manufacturer_options)

        with col2:
            quantity = st.number_input("Quantity:", min_value=1, value=10)

        if st.button("Buy"):
            manufacturer_name = selected_manufacturer.split(" - ")[0]
            result = game.buy_products(manufacturer_name, quantity)
            st.success(result)
            st.rerun()

    elif action == "Sell Products":
        st.subheader("💰 Sell Products")
        if not game.inventory:
            st.warning("No products in inventory to sell!")
        else:
            col1, col2, col3 = st.columns(3)

            with col1:
                product_options = list(game.inventory.keys())
                selected_product = st.selectbox("Choose product:", product_options)

            with col2:
                site_options = [s.name for s in game.selling_sites]
                selected_site = st.selectbox("Choose selling site:", site_options)

            with col3:
                country_options = [c.name for c in game.countries]
                selected_country = st.selectbox("Choose target country:", country_options)

            max_qty = game.inventory.get(selected_product, 0)
            quantity = st.number_input("Quantity:", min_value=1, max_value=max_qty, value=min(10, max_qty))

            if st.button("Sell"):
                result = game.sell_products(selected_product, selected_site, selected_country, quantity)
                st.success(result)
                st.rerun()

    elif action == "Check Inventory":
        st.subheader("📦 Current Inventory")
        if game.inventory:
            for product, qty in game.inventory.items():
                st.write(f"- {product}: {qty}")
        else:
            st.info("No products in inventory yet.")

    elif action == "View Stats":
        st.subheader("📈 Detailed Statistics")
        st.write(f"Total Revenue: ${game.tracker.total_revenue:.2f}")
        st.write(f"Total Profit: ${game.tracker.total_profit:.2f}")
        st.write(f"Total Sales Volume: {game.tracker.total_sales}")

        if game.tracker.sales:
            st.subheader("Recent Sales")
            for sale in game.tracker.sales[-5:]:  # Show last 5 sales
                st.write(f"- {sale.product}: {sale.quantity} units, Profit: ${sale.profit:.2f}")

    elif action == "Advance Day":
        st.subheader("⏭️ Advance to Next Day")
        if st.button("Advance Day"):
            result = game.advance_day()
            st.success(result)
            st.rerun()

    elif action == "Get AI Advice":
        st.subheader("🤖 AI Business Advisor")
        if st.button("Get Strategic Advice"):
            with st.spinner("Getting AI advice..."):
                advice = game.get_ai_advice()
            st.info(advice)

    # Market Information
    with st.expander("🌍 Market Information"):
        st.subheader("Countries")
        for country in game.countries:
            st.write(f"- **{country.name}**: Demand {country.demand_level:.1f}, Shipping ${country.shipping_cost:.2f}, Tax {country.tax_rate:.1%}")

        st.subheader("Manufacturers")
        for manufacturer in game.manufacturers:
            st.write(f"- **{manufacturer.name}**: {manufacturer.product} (${manufacturer.unit_cost:.2f}), Stock: {manufacturer.stock}")

        st.subheader("Selling Sites")
        for site in game.selling_sites:
            st.write(f"- **{site.name}**: Fee {site.fee_rate:.1%}, Traffic {site.traffic:.1f}, Trust {site.trust:.1f}")

    # Game Tips
    with st.expander("💡 Game Tips"):
        st.markdown("""
        - **Buy low, sell high**: Purchase products when you have cash, sell when demand is high
        - **Watch shipping costs**: Some countries are expensive to ship to
        - **Consider taxes**: High-tax countries reduce your profits
        - **Site fees matter**: Premium sites have higher fees but more traffic
        - **Advance days**: Market conditions change daily
        - **Goal**: Build your dropshipping empire and maximize profits!
        """)


if __name__ == "__main__":
    main()
