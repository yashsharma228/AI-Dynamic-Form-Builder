from flask import Blueprint, jsonify, request
from marshmallow import ValidationError as MarshmallowValidationError

from schemas.response_schema import ResponseCreateSchema, ResponseOutputSchema
from services.errors import ValidationError
from services.response_service import ResponseService

responses_bp = Blueprint("responses", __name__)


@responses_bp.post("/responses")
def submit_response():
    payload = request.get_json(silent=True) or {}
    try:
        data = ResponseCreateSchema().load(payload)
        response_obj = ResponseService.submit_response(data)
    except MarshmallowValidationError as exc:
        raise ValidationError(str(exc.messages)) from exc

    return jsonify(ResponseOutputSchema().dump(response_obj)), 201


@responses_bp.get("/responses/<int:form_id>")
def get_responses(form_id: int):
    responses = ResponseService.get_responses_for_form(form_id)
    return jsonify(ResponseOutputSchema(many=True).dump(responses)), 200
