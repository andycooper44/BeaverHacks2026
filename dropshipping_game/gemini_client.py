import os
from dataclasses import dataclass

try:
    from google import genai

    GENAI_AVAILABLE = True
    GENAI_MODERN = True
except ImportError:
    try:
        import google.generativeai as genai

        GENAI_AVAILABLE = True
        GENAI_MODERN = False
    except ImportError:
        GENAI_AVAILABLE = False
        GENAI_MODERN = False


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

        if not GENAI_AVAILABLE:
            return "Google Gemini AI library not installed. Run 'pip install google-genai' for AI advice."

        prompt = f"""
You are an expert dropshipping business advisor. Based on this game state, give one strategic tip (2-3 sentences max):

{game_state}

What should the player focus on next?
"""

        try:
            if GENAI_MODERN:
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel(model=self.model_name)
                response = model.generate(prompt=prompt)
            else:
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel(self.model_name)
                response = model.generate_content(prompt)

            if hasattr(response, "text"):
                return response.text.strip()
            if hasattr(response, "candidates") and response.candidates:
                return response.candidates[0].content.strip()
            return str(response)
        except Exception as e:
            return f"Error getting AI advice: {str(e)}"
