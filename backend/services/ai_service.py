import os
import json
import logging
from typing import Any

from openai import OpenAI

from schemas.ai_schema import AIGenerateResponseSchema
from services.errors import ValidationError


logger = logging.getLogger(__name__)


class AIService:
    @staticmethod
    def _build_system_prompt() -> str:
        return (
            "You generate dynamic form definitions as strict JSON only. "
            "Return an object with keys: title (string), description (string), fields (array). "
            "Each field must include: type, label. "
            "Supported type values are: text, email, select, checkbox. "
            "Only select fields may include options (array of strings with at least one entry). "
            "Do not include markdown, comments, or extra keys."
        )

    @staticmethod
    def _mock_generate(prompt: str) -> dict[str, Any]:
        normalized = prompt.lower()

        title = "Generated Form"
        description = "Form generated from prompt"
        fields = [{"type": "text", "label": "Name"}, {"type": "email", "label": "Email"}]

        if "feedback" in normalized:
            title = "Feedback Form"
            description = "Collect structured feedback from users"
            fields.append({"type": "select", "label": "Rating", "options": ["1", "2", "3", "4", "5"]})
            fields.append({"type": "checkbox", "label": "Would recommend"})
        elif "registration" in normalized or "signup" in normalized:
            title = "Registration Form"
            description = "Collect details for registration"
            fields.append({"type": "text", "label": "Company"})
            fields.append({"type": "checkbox", "label": "Agree to terms"})

        return {"title": title, "description": description, "fields": fields}

    @staticmethod
    def _generate_with_openai(prompt: str, api_key: str, model: str) -> dict[str, Any]:
        base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("OPENROUTER_BASE_URL")
        app_url = os.getenv("OPENROUTER_APP_URL", "http://localhost:5173")
        app_name = os.getenv("OPENROUTER_APP_NAME", "AI Dynamic Form Builder")

        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url

        if base_url and "openrouter.ai" in base_url:
            client_kwargs["default_headers"] = {
                "HTTP-Referer": app_url,
                "X-Title": app_name,
            }

        client = OpenAI(**client_kwargs)
        completion = client.chat.completions.create(
            model=model,
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": AIService._build_system_prompt()},
                {"role": "user", "content": prompt},
            ],
        )

        content = completion.choices[0].message.content
        if not content:
            raise ValidationError("OpenAI returned an empty response")

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValidationError("OpenAI did not return valid JSON") from exc

        if not isinstance(parsed, dict):
            raise ValidationError("OpenAI output must be a JSON object")

        return parsed

    @staticmethod
    def generate_form_from_prompt(prompt: str) -> dict[str, Any]:
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("AI_API_KEY")
        model = os.getenv("OPENAI_MODEL") or os.getenv("OPENROUTER_MODEL") or "gpt-4o-mini"

        if not api_key:
            generated = AIService._mock_generate(prompt)
        else:
            try:
                generated = AIService._generate_with_openai(prompt, api_key=api_key, model=model)
            except Exception as exc:
                logger.warning("OpenAI generation failed, using mock fallback: %s", str(exc))
                generated = AIService._mock_generate(prompt)

        errors = AIGenerateResponseSchema().validate(generated)
        if errors:
            raise ValidationError(f"AI output failed validation: {errors}")

        return generated
