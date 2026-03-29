from flask import Blueprint, jsonify, request
from marshmallow import ValidationError as MarshmallowValidationError

from schemas.form_schema import FormCreateSchema, FormOutputSchema
from services.errors import ValidationError
from services.form_service import FormService

forms_bp = Blueprint("forms", __name__, url_prefix="/forms")


@forms_bp.post("")
def create_form():
    payload = request.get_json(silent=True) or {}
    try:
        data = FormCreateSchema().load(payload)
        form = FormService.create_form(data)
    except MarshmallowValidationError as exc:
        raise ValidationError(str(exc.messages)) from exc

    return jsonify(FormOutputSchema().dump(form)), 201


@forms_bp.get("")
def get_forms():
    forms = FormService.list_forms()
    return jsonify(FormOutputSchema(many=True).dump(forms)), 200


@forms_bp.get("/<int:form_id>")
def get_form(form_id: int):
    form = FormService.get_form_by_id(form_id)
    return jsonify(FormOutputSchema().dump(form)), 200


@forms_bp.delete("/<int:form_id>")
def delete_form(form_id: int):
    FormService.delete_form(form_id)
    return jsonify({"message": "Form deleted successfully"}), 200


@forms_bp.put("/<int:form_id>")
def update_form(form_id: int):
    payload = request.get_json(silent=True) or {}
    try:
        data = FormCreateSchema().load(payload)
        form = FormService.update_form(form_id, data)
    except MarshmallowValidationError as exc:
        raise ValidationError(str(exc.messages)) from exc

    return jsonify(FormOutputSchema().dump(form)), 200
