# Dropshipping Game

A complete dropshipping business simulation game built with Python and Streamlit.

## How to Play

You're running a dropshipping business! Buy products from manufacturers, sell them on different platforms to various countries, and manage your profits while dealing with shipping costs, taxes, and platform fees.

### Game Mechanics
- **Buy Products**: Purchase inventory from manufacturers at wholesale prices
- **Sell Products**: Sell your inventory on different platforms to different countries
- **Advance Days**: Time passes, market conditions change
- **Track Profits**: Monitor your money, sales, and overall business performance

### Strategic Elements
- Different countries have varying demand levels, shipping costs, and tax rates
- Selling platforms have different fee structures and traffic levels
- Market conditions change daily
- AI advisor available (requires Gemini API key)

## Run

```powershell
py -m pip install -r requirements.txt
py -m streamlit run dropshipping_game/ui/streamlit_app.py
```

## Gemini Setup

1. Set your Gemini API key:

```powershell
setx GEMINI_API_KEY "your_api_key_here"
```

2. Restart your terminal so the environment variable is available.
3. Run the game again with Streamlit.

## Files

- `dropshipping_game/game.py`: Main game logic and mechanics
- `dropshipping_game/tracker.py`: Sales and financial tracking
- `dropshipping_game/countries.py`: Country data (demand, costs, taxes)
- `dropshipping_game/manufacturers.py`: Manufacturer data (products, pricing, stock)
- `dropshipping_game/selling_sites.py`: Platform data (fees, traffic, trust)
- `dropshipping_game/gemini_client.py`: AI advisor integration
- `dropshipping_game/ui/streamlit_app.py`: Interactive web UI

## AI Features

Set `GEMINI_API_KEY` environment variable to enable AI-powered business advice.

## Goal

Build your dropshipping empire and maximize profits over time!
