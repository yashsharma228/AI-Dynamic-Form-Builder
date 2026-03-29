"""OpenRouter API client for simple direct API calls."""

import os
import requests
import logging

logger = logging.getLogger(__name__)


def mock_response():
    """Fallback mock response when API call fails."""
    return {
        "choices": [
            {
                "message": {
                    "content": '{"title": "Default Form", "description": "Mock form", "fields": [{"type": "text", "label": "Name"}]}'
                }
            }
        ]
    }


def generate_form(prompt: str) -> dict:
    """Generate a form using OpenRouter API.
    
    Args:
        prompt: User's form generation prompt
        
    Returns:
        API response dict with generated form structure
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        return mock_response()
    
    try:
        base_url = os.getenv("OPENROUTER_BASE_URL")
        model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        app_url = os.getenv("OPENROUTER_APP_URL", "http://localhost:5173")
        app_name = os.getenv("OPENROUTER_APP_NAME", "AI Dynamic Form Builder")
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": app_url,
                "X-Title": app_name,
            },
            json={
                "model": model,
                "temperature": 0.2,
                "response_format": {"type": "json_object"},
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You generate dynamic form definitions as strict JSON only. "
                            "Return an object with keys: title (string), description (string), fields (array). "
                            "Each field must include: type, label. "
                            "Supported type values are: text, email, select, checkbox. "
                            "Only select fields may include options (array of strings with at least one entry). "
                            "Do not include markdown, comments, or extra keys."
                        )
                    },
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30
        )
        
        return response.json()

    except Exception as e:
        logger.exception("OpenRouter API error: %s", str(e))
        return mock_response()
