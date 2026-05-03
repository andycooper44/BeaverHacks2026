import os
from dataclasses import dataclass

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


@dataclass
class GeminiAdvisor:
    api_key: str = ""
    model_name: str = "gemini-1.5-flash"
    prompt: str = ""
    response_text: str = ""

    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.getenv("GEMINI_API_KEY", "")

    def get_advice(self, game_state: str) -> str:
        """Get AI advice based on current game state"""
        if not self.api_key:
            return "No Gemini API key set. Set GEMINI_API_KEY environment variable for AI advice."

        if not GEMINI_AVAILABLE:
            return "Google Generative AI library not installed. Run 'pip install google-generativeai' for AI advice."

        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)

            prompt = f"""
You are an expert dropshipping business advisor. Based on this game state, give one strategic tip (2-3 sentences max):

{game_state}

What should the player focus on next?
"""

            response = model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return f"Error getting AI advice: {str(e)}"
