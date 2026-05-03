from dataclasses import dataclass


@dataclass
class GeminiAdvisor:
    api_key: str = ""
    model_name: str = "gemini-1.5-flash"
    prompt: str = ""
    response_text: str = ""
