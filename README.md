# Dropshipping Game Barebones Draft

Very barebones Python scaffold for a customizable dropshipping game.

The files mostly contain typed classes and placeholder variables. Add your own
game rules, UI, Gemini prompts, and data.

## Files

- `dropshipping_game/game.py`: main game class shell
- `dropshipping_game/tracker.py`: money and sales class shells
- `dropshipping_game/countries.py`: country class shell
- `dropshipping_game/manufacturers.py`: manufacturer class shell
- `dropshipping_game/selling_sites.py`: selling site class shell
- `dropshipping_game/gemini_client.py`: Gemini class shell
- `dropshipping_game/ui/streamlit_app.py`: Streamlit placeholder

## Run

```powershell
pip install -r requirements.txt
python main.py
streamlit run dropshipping_game/ui/streamlit_app.py
```

## Gemini

Set `GEMINI_API_KEY` when you are ready to test AI suggestions.

## Changelog

Sayer:
-Added a more descriptive UI in streamlit, Including placement of iteractability.
-added message every day to display sales and events
-Added tutorial
-Added graph of recent sales 
-fixed crash when stock was zero
