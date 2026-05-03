import os
import sys

# Ensure the project root is on sys.path when Streamlit runs this module.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from dropshipping_game.game import DropshippingGame


game: DropshippingGame = DropshippingGame()


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
