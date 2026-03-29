from flask import Blueprint, jsonify, request
from marshmallow import ValidationError as MarshmallowValidationError

from schemas.ai_schema import AIGenerateRequestSchema, AIGenerateResponseSchema
from services.ai_service import AIService
from services.errors import ValidationError

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")


@ai_bp.post("/generate-form")
def generate_form():
    payload = request.get_json(silent=True) or {}
    try:
        data = AIGenerateRequestSchema().load(payload)
        generated = AIService.generate_form_from_prompt(data["prompt"])
        validated = AIGenerateResponseSchema().load(generated)
    except MarshmallowValidationError as exc:
        raise ValidationError(str(exc.messages)) from exc

    return jsonify(validated), 200
