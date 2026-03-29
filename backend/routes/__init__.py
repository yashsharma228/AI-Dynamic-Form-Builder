"""API routes package."""

from routes.ai import ai_bp
from routes.forms import forms_bp
from routes.responses import responses_bp

__all__ = ["forms_bp", "responses_bp", "ai_bp"]
