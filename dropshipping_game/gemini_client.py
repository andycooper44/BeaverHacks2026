import os
from dataclasses import dataclass
from pathlib import Path

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


def load_gemini_api_key() -> str:
    """Load Gemini API key from the environment or a local .env file."""

    return load_env_value("GEMINI_API_KEY")


def load_env_value(name: str) -> str:
    """Load a value from the environment or a local .env file."""

    env_value = os.getenv(name, "").strip()
    if env_value:
        return env_value

    env_paths = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parents[1] / ".env",
    ]

    for env_path in env_paths:
        if not env_path.exists():
            continue

        for line in env_path.read_text(encoding="utf-8").splitlines():
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue
            if "=" not in clean_line:
                continue

            key, value = clean_line.split("=", 1)
            if key.strip() == name:
                return value.strip().strip('"').strip("'")

    return ""


@dataclass
class GeminiAdvisor:
    api_key: str = ""
    model_name: str = ""
    prompt: str = ""
    response_text: str = ""

    def __post_init__(self):
        if not self.api_key:
            self.api_key = load_gemini_api_key()
        if not self.model_name:
            self.model_name = load_env_value("GEMINI_MODEL") or "gemini-2.5-flash"

    def get_advice(self, game_state: str) -> str:
        """Get AI advice based on current game state"""
        if not self.api_key:
            return "No Gemini API key set. Add GEMINI_API_KEY to .env or your environment."

        if not GENAI_AVAILABLE:
            return "Google Gemini AI library not installed. Run 'pip install google-genai' for AI advice."

        prompt = f"""
You are an expert dropshipping business advisor. Based on this game state, give one strategic tip (2-3 sentences max):

{game_state}

What should the player focus on next?
"""

        try:
            if GENAI_MODERN:
                client = genai.Client(api_key=self.api_key)
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )
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
