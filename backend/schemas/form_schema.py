from marshmallow import Schema, ValidationError, fields, validate, validates_schema

ALLOWED_FIELD_TYPES = {"text", "email", "select", "checkbox", "number", "date", "time", "datetime-local", "textarea", "tel"}


class FieldInputSchema(Schema):
    type = fields.String(required=True, validate=validate.OneOf(list(ALLOWED_FIELD_TYPES)))
    label = fields.String(required=True, validate=validate.Length(min=1, max=255))
    placeholder = fields.String(required=False, allow_none=True, validate=validate.Length(max=255))
    is_required = fields.Boolean(required=False, load_default=False)
    sort_order = fields.Int(required=False, load_default=0)
    options = fields.List(fields.String(), required=False, allow_none=True)
    validation_rules = fields.Dict(required=False, allow_none=True)

    @validates_schema
    def validate_options(self, data, **kwargs):
        field_type = data.get("type")
        options = data.get("options")

        if field_type == "select":
            if not options or len(options) < 1:
                raise ValidationError(
                    "Select field must include at least one option.",
                    field_name="options",
                )
        elif options:
            raise ValidationError(
                "Options are only valid for select fields.",
                field_name="options",
            )


class FormCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String(required=False, allow_none=True)
    fields = fields.List(fields.Nested(FieldInputSchema), required=True, validate=validate.Length(min=1))


class FieldOutputSchema(Schema):
    id = fields.Int(required=True)
    type = fields.String(required=True)
    label = fields.String(required=True)
    placeholder = fields.String(allow_none=True)
    is_required = fields.Boolean(required=True)
    sort_order = fields.Int(required=True)
    options = fields.Raw(allow_none=True)
    validation_rules = fields.Raw(allow_none=True)


class FormOutputSchema(Schema):
    id = fields.Int(required=True)
    title = fields.String(required=True)
    description = fields.String(allow_none=True)
    is_active = fields.Boolean(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    fields = fields.List(fields.Nested(FieldOutputSchema), required=True)
