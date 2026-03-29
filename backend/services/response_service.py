from typing import Any

from extensions import db
from models import Response
from services.errors import ValidationError
from services.form_service import FormService


class ResponseService:
    @staticmethod
    def submit_response(data: dict[str, Any]) -> Response:
        form = FormService.get_form_by_id(data["form_id"])

        expected_labels = {field.label for field in form.fields}
        submitted_labels = set(data["answers"].keys())

        missing_labels = expected_labels - submitted_labels
        if missing_labels:
            raise ValidationError(f"Missing answers for fields: {', '.join(sorted(missing_labels))}")

        response = Response(
            form_id=form.id,
            answers=data["answers"],
            respondent_email=data.get("respondent_email"),
        )
        db.session.add(response)
        db.session.commit()
        return response

    @staticmethod
    def get_responses_for_form(form_id: int) -> list[Response]:
        FormService.get_form_by_id(form_id)
        return Response.query.filter_by(form_id=form_id).order_by(Response.submitted_at.desc()).all()
