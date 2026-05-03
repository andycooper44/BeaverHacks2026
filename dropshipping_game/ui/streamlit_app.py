import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dropshipping_game.game import DropshippingGame


def apply_page_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .app-banner {
            border: 1px solid rgba(49, 51, 63, 0.18);
            border-left: 6px solid #2e8b6d;
            background: var(--secondary-background-color);
            padding: 1.2rem 1.4rem;
            border-radius: 8px;
            margin-bottom: 1.2rem;
        }

        .app-banner h1 {
            margin: 0;
            color: var(--text-color);
            font-size: 2.1rem;
        }

        .app-banner p {
            margin: 0.35rem 0 0;
            color: var(--text-color);
            font-size: 1rem;
            opacity: 0.88;
        }

        .section-note {
            color: var(--text-color);
            margin-top: -0.35rem;
            margin-bottom: 0.8rem;
            opacity: 0.78;
        }

        .inventory-line {
            border: 1px solid rgba(49, 51, 63, 0.18);
            border-left: 4px solid #c76b21;
            padding: 0.55rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.4rem;
            background: var(--secondary-background-color);
            color: var(--text-color);
        }

        .inventory-line strong {
            color: var(--text-color);
        }

        .advice-box {
            border: 1px solid rgba(49, 51, 63, 0.18);
            border-left: 4px solid #5267b0;
            padding: 0.8rem 1rem;
            border-radius: 6px;
            background: var(--secondary-background-color);
            color: var(--text-color);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_page_banner() -> None:
    st.markdown(
        """
        <div class="app-banner">
            <h1>Dropshipping Empire</h1>
            <p>Buy inventory, choose markets, manage platform fees, and grow profit before rent comes due.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_note(text: str) -> None:
    st.markdown(f'<div class="section-note">{text}</div>', unsafe_allow_html=True)


def get_game() -> DropshippingGame:
    if "game" not in st.session_state:
        st.session_state.game = DropshippingGame()
    return st.session_state.game


def show_status(game: DropshippingGame) -> None:
    st.header("Business Overview")
    section_note("A quick read on cash, sales progress, inventory pressure, and rent timing.")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Day", game.current_day)
    col2.metric("Money", f"${game.tracker.money:.2f}")
    col3.metric("Total Sales", game.tracker.total_sales)
    col4.metric("Total Profit", f"${game.tracker.total_profit:.2f}")
    col5.metric("Days Until Rent", game.days_until_rent)

    if game.inventory:
        st.subheader("Inventory")
        for product, quantity in game.inventory.items():
            st.markdown(
                f'<div class="inventory-line"><strong>{product}</strong>: {quantity} units ready to sell</div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("No inventory yet. Buy products to start selling.")


def show_buy_products(game: DropshippingGame) -> None:
    st.subheader("Buy Products")
    section_note("Pick a supplier and buy stock. Your cash drops now, but inventory creates selling options.")
    manufacturer_options = [
        f"{manufacturer.name} - {manufacturer.product} (${manufacturer.unit_cost:.2f}, stock: {manufacturer.stock})"
        for manufacturer in game.manufacturers
    ]
    selected = st.selectbox("Manufacturer", manufacturer_options)
    quantity = st.number_input("Quantity", min_value=1, value=10, step=1)

    if st.button("Buy"):
        manufacturer_name = selected.split(" - ", 1)[0]
        st.success(game.buy_products(manufacturer_name, int(quantity)))
        st.rerun()


def show_sell_products(game: DropshippingGame) -> None:
    st.subheader("Sell Products")
    section_note("Choose where to sell. Demand, fees, shipping, and taxes all affect profit.")
    if not game.inventory:
        st.warning("No products in inventory to sell.")
        return

    product = st.selectbox("Product", list(game.inventory.keys()))
    site = st.selectbox(
        "Selling Site",
        [selling_site.name for selling_site in game.selling_sites],
    )
    country = st.selectbox("Country", [market.name for market in game.countries])
    max_quantity = game.inventory[product]
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=max_quantity,
        value=1,
        step=1,
    )

    if st.button("Sell"):
        st.success(game.sell_products(product, site, country, int(quantity)))
        st.rerun()


def show_stats(game: DropshippingGame) -> None:
    st.subheader("Sales Stats")
    section_note("Recent performance helps you spot which products and markets are worth repeating.")
    st.write(f"Total Revenue: ${game.tracker.total_revenue:.2f}")
    st.write(f"Total Profit: ${game.tracker.total_profit:.2f}")
    st.write(f"Total Sales Volume: {game.tracker.total_sales}")

    if game.tracker.sales:
        rows = [
            {
                "Day": sale.day,
                "Product": sale.product,
                "Quantity": sale.quantity,
                "Revenue": round(sale.revenue, 2),
                "Cost": round(sale.cost, 2),
                "Profit": round(sale.profit, 2),
            }
            for sale in game.tracker.sales[-10:]
        ]
        st.dataframe(rows, use_container_width=True)


def show_market_info(game: DropshippingGame) -> None:
    with st.expander("Market Information"):
        st.caption("Reference data for choosing products, markets, and selling platforms.")
        st.subheader("Countries")
        for country in game.countries:
            st.write(
                f"- **{country.name}**: demand {country.demand_level:.2f}, "
                f"shipping ${country.shipping_cost:.2f}, tax {country.tax_rate:.1%}"
            )

        st.subheader("Manufacturers")
        for manufacturer in game.manufacturers:
            st.write(
                f"- **{manufacturer.name}**: {manufacturer.product}, "
                f"unit cost ${manufacturer.unit_cost:.2f}, stock {manufacturer.stock}"
            )

        st.subheader("Selling Sites")
        for site in game.selling_sites:
            st.write(
                f"- **{site.name}**: fee {site.fee_rate:.1%}, "
                f"traffic {site.traffic:.2f}, trust {site.trust:.2f}"
            )


def main() -> None:
    st.set_page_config(page_title="Dropshipping Empire", page_icon="DE", layout="wide")
    apply_page_styles()
    show_page_banner()

    game = get_game()
    show_status(game)

    st.sidebar.header("Actions")
    if st.sidebar.button("Advance Day"):
        st.session_state.day_summary = game.advance_day()
        st.rerun()

    if "day_summary" in st.session_state:
        st.info(st.session_state.day_summary)

    action = st.sidebar.radio(
        "Choose Action",
        ["Buy Products", "Sell Products", "View Stats"],
    )

    if action == "Buy Products":
        show_buy_products(game)
    elif action == "Sell Products":
        show_sell_products(game)
    elif action == "View Stats":
        show_stats(game)

    show_market_info(game)


if __name__ == "__main__":
    main()
