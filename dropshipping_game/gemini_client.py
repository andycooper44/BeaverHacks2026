from dataclasses import dataclass
import os
from typing import Optional, Dict, Any
import google.generativeai as genai


@dataclass
class GeminiAdvisor:
    api_key: str = ""
    model_name: str = "gemini-1.5-flash"
    prompt: str = ""
    response_text: str = ""
    model: Optional[Any] = None

    def __post_init__(self):
        """Initialize the Gemini model if API key is provided."""
        if self.api_key:
            self._initialize_model()

    def _initialize_model(self) -> None:
        """Initialize the Gemini API client."""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            print(f"Failed to initialize Gemini model: {e}")
            self.model = None

    def set_api_key(self, api_key: str) -> None:
        """Set the API key and initialize the model."""
        self.api_key = api_key
        self._initialize_model()

    def get_business_advice(self, game_state: Dict[str, Any]) -> str:
        """Get business advice based on current game state."""
        if not self.model:
            return "Gemini API not configured. Set GEMINI_API_KEY environment variable."

        try:
            # Create a detailed prompt about the business situation
            prompt = self._create_business_prompt(game_state)

            response = self.model.generate_content(prompt)
            self.response_text = response.text
            return self.response_text

        except Exception as e:
            return f"Error getting AI advice: {str(e)}"

    def get_market_analysis(self, game_state: Dict[str, Any]) -> str:
        """Analyze market conditions and provide insights."""
        if not self.model:
            return "Gemini API not configured."

        try:
            prompt = f"""Analyze the current dropshipping market conditions:

Game State: {game_state}

Provide insights on:
1. Best countries to target based on demand vs costs
2. Most profitable products to focus on
3. Optimal pricing strategies
4. Risk factors to watch out for
5. Growth opportunities

Be specific and actionable."""

            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            return f"Error getting market analysis: {str(e)}"

    def get_strategy_recommendation(self, game_state: Dict[str, Any], question: str) -> str:
        """Get specific strategy advice for a question."""
        if not self.model:
            return "Gemini API not configured."

        try:
            prompt = f"""Dropshipping Business Strategy Question:

Game State: {game_state}

Question: {question}

Provide detailed, actionable advice for this dropshipping business scenario."""

            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            return f"Error getting strategy recommendation: {str(e)}"

    def _create_business_prompt(self, game_state: Dict[str, Any]) -> str:
        """Create a comprehensive business analysis prompt."""
        return f"""You are an expert dropshipping business consultant. Analyze this dropshipping business and provide strategic advice:

Current Business State:
- Day: {game_state.get('current_day', 0)}
- Money: ${game_state.get('money', 0):.2f}
- Total Sales: {game_state.get('total_sales', 0)}
- Total Revenue: ${game_state.get('total_revenue', 0):.2f}
- Total Profit: ${game_state.get('total_profit', 0):.2f}

Available Markets (Countries):
{self._format_countries(game_state.get('countries', []))}

Available Manufacturers:
{self._format_manufacturers(game_state.get('manufacturers', []))}

Available Selling Platforms:
{self._format_selling_sites(game_state.get('selling_sites', []))}

Recent Sales:
{self._format_recent_sales(game_state.get('recent_sales', []))}

Business Notes: {game_state.get('notes', 'None')}

Provide 3-5 specific, actionable recommendations for growing this dropshipping business. Consider:
- Which products to focus on
- Which markets to prioritize
- Pricing strategies
- Inventory management
- Platform selection
- Risk mitigation

Be concise but specific."""

    def _format_countries(self, countries: list) -> str:
        """Format countries list for the prompt."""
        if not countries:
            return "None"
        return "\n".join([
            f"- {c.get('name', 'Unknown')}: Demand {c.get('demand_level', 0):.1f}, "
            f"Shipping ${c.get('shipping_cost', 0):.2f}, Tax {c.get('tax_rate', 0):.1%}"
            for c in countries
        ])

    def _format_manufacturers(self, manufacturers: list) -> str:
        """Format manufacturers list for the prompt."""
        if not manufacturers:
            return "None"
        return "\n".join([
            f"- {m.get('name', 'Unknown')}: {m.get('product', 'Unknown')} "
            f"@ ${m.get('unit_cost', 0):.2f}, Stock: {m.get('stock', 0)}, Quality: {m.get('quality', 0):.1f}"
            for m in manufacturers
        ])

    def _format_selling_sites(self, sites: list) -> str:
        """Format selling sites list for the prompt."""
        if not sites:
            return "None"
        return "\n".join([
            f"- {s.get('name', 'Unknown')}: Fee {s.get('fee_rate', 0):.1%}, "
            f"Traffic {s.get('traffic', 0):.1f}, Trust {s.get('trust', 0):.1f}"
            for s in sites
        ])

    def _format_recent_sales(self, sales: list) -> str:
        """Format recent sales for the prompt."""
        if not sales:
            return "None"
        recent = sales[-3:]  # Last 3 sales
        return "\n".join([
            f"- {s.get('product', 'Unknown')}: {s.get('quantity', 0)} units, "
            f"Revenue ${s.get('revenue', 0):.2f}, Profit ${s.get('profit', 0):.2f}"
            for s in recent
        ])
