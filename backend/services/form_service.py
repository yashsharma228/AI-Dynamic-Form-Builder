from typing import Any

from extensions import db
from models import Field, Form
from services.errors import NotFoundError


class FormService:
    @staticmethod
    def create_form(data: dict[str, Any]) -> Form:
        form = Form(
            title=data["title"],
            description=data.get("description"),
        )

        for index, field_data in enumerate(data["fields"]):
            field = Field(
                type=field_data["type"],
                label=field_data["label"],
                placeholder=field_data.get("placeholder"),
                is_required=field_data.get("is_required", False),
                sort_order=field_data.get("sort_order", index),
                options=field_data.get("options"),
                validation_rules=field_data.get("validation_rules"),
            )
            form.fields.append(field)

        db.session.add(form)
        db.session.commit()
        return form

    @staticmethod
    def list_forms() -> list[Form]:
        return Form.query.order_by(Form.created_at.desc()).all()

    @staticmethod
    def get_form_by_id(form_id: int) -> Form:
        form = db.session.get(Form, form_id)
        if not form:
            raise NotFoundError("Form not found")
        return form

    @staticmethod
    def delete_form(form_id: int) -> None:
        form = db.session.get(Form, form_id)
        if not form:
            raise NotFoundError("Form not found")
        db.session.delete(form)
        db.session.commit()

    @staticmethod
    def update_form(form_id: int, data: dict[str, Any]) -> Form:
        form = db.session.get(Form, form_id)
        if not form:
            raise NotFoundError("Form not found")

        form.title = data["title"]
        form.description = data.get("description")

        # Replace all fields
        for field in list(form.fields):
            db.session.delete(field)

        for index, field_data in enumerate(data["fields"]):
            field = Field(
                form_id=form.id,
                type=field_data["type"],
                label=field_data["label"],
                placeholder=field_data.get("placeholder"),
                is_required=field_data.get("is_required", False),
                sort_order=field_data.get("sort_order", index),
                options=field_data.get("options"),
                validation_rules=field_data.get("validation_rules"),
            )
            db.session.add(field)

        db.session.commit()
        db.session.refresh(form)
        return form
