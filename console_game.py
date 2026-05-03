#!/usr/bin/env python3
"""
Console-based Dropshipping Game
Run this if Streamlit isn't working yet.
"""

from dropshipping_game.game import DropshippingGame


def main():
    print("🚚 Dropshipping Empire - Console Edition")
    print("=" * 50)

    game = DropshippingGame()

    while True:
        print(f"\n📊 Day {game.current_day} | Money: ${game.tracker.money:.2f}")
        print(f"Total Profit: ${game.tracker.total_profit:.2f}")

        if game.inventory:
            print("📦 Inventory:")
            for product, qty in game.inventory.items():
                print(f"  - {product}: {qty}")
        else:
            print("📦 Inventory: Empty")

        print("\n🎯 Available Actions:")
        actions = game.get_available_actions()
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")

        try:
            choice = input("\nChoose action (number or name): ").strip()

            # Try to parse as number first
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(actions):
                    action = actions[choice_idx]
                else:
                    print("Invalid choice.")
                    continue
            except ValueError:
                # Try as action name
                if choice in actions:
                    action = choice
                else:
                    print("Invalid action.")
                    continue

            if action == "Buy Products":
                print("\n🛒 Available Manufacturers:")
                for i, m in enumerate(game.manufacturers, 1):
                    print(f"{i}. {m.name} - {m.product} (${m.unit_cost:.2f}, stock: {m.stock})")

                try:
                    m_choice = int(input("Choose manufacturer (number): ")) - 1
                    if 0 <= m_choice < len(game.manufacturers):
                        manufacturer = game.manufacturers[m_choice]
                        qty = int(input(f"How many {manufacturer.product}s to buy? "))
                        result = game.buy_products(manufacturer.name, qty)
                        print(f"✅ {result}")
                    else:
                        print("Invalid manufacturer.")
                except ValueError:
                    print("Invalid input.")

            elif action == "Sell Products":
                if not game.inventory:
                    print("❌ No products to sell!")
                    continue

                print("\n📦 Your Inventory:")
                products = list(game.inventory.keys())
                for i, product in enumerate(products, 1):
                    print(f"{i}. {product} ({game.inventory[product]} available)")

                try:
                    p_choice = int(input("Choose product to sell (number): ")) - 1
                    if 0 <= p_choice < len(products):
                        product = products[p_choice]

                        print("\n🌍 Available Countries:")
                        for i, c in enumerate(game.countries, 1):
                            print(f"{i}. {c.name} (demand: {c.demand_level:.1f}, shipping: ${c.shipping_cost:.2f})")

                        c_choice = int(input("Choose country (number): ")) - 1
                        if 0 <= c_choice < len(game.countries):
                            country = game.countries[c_choice]

                            print("\n🏪 Available Selling Sites:")
                            for i, s in enumerate(game.selling_sites, 1):
                                print(f"{i}. {s.name} (fee: {s.fee_rate:.1%}, traffic: {s.traffic:.1f})")

                            s_choice = int(input("Choose site (number): ")) - 1
                            if 0 <= s_choice < len(game.selling_sites):
                                site = game.selling_sites[s_choice]

                                max_qty = game.inventory[product]
                                qty = int(input(f"How many to sell (max {max_qty})? "))
                                if 1 <= qty <= max_qty:
                                    result = game.sell_products(product, site.name, country.name, qty)
                                    print(f"✅ {result}")
                                else:
                                    print("Invalid quantity.")
                            else:
                                print("Invalid site.")
                        else:
                            print("Invalid country.")
                    else:
                        print("Invalid product.")
                except ValueError:
                    print("Invalid input.")

            elif action == "Check Inventory":
                if game.inventory:
                    print("\n📦 Current Inventory:")
                    for product, qty in game.inventory.items():
                        print(f"  - {product}: {qty}")
                else:
                    print("\n📦 No products in inventory.")

            elif action == "View Stats":
                print("
📈 Game Statistics:"                print(f"  Total Sales: {game.tracker.total_sales}")
                print(f"  Total Revenue: ${game.tracker.total_revenue:.2f}")
                print(f"  Total Profit: ${game.tracker.total_profit:.2f}")

                if game.tracker.sales:
                    print(f"\nRecent Sales (last {min(5, len(game.tracker.sales))}):")
                    for sale in game.tracker.sales[-5:]:
                        print(f"  - {sale.product}: {sale.quantity} units, Profit: ${sale.profit:.2f}")

            elif action == "Advance Day":
                result = game.advance_day()
                print(f"✅ {result}")

            elif action == "Get AI Advice":
                print("\n🤖 Getting AI advice...")
                advice = game.get_ai_advice()
                print(f"💡 {advice}")

        except KeyboardInterrupt:
            print("\n\n👋 Thanks for playing!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()