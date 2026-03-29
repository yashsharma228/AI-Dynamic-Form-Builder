from marshmallow import Schema, ValidationError, fields, validate, validates_schema

from schemas.form_schema import ALLOWED_FIELD_TYPES


class AIGenerateRequestSchema(Schema):
    prompt = fields.String(required=True, validate=validate.Length(min=5, max=2000))


class AIGeneratedFieldSchema(Schema):
    type = fields.String(required=True, validate=validate.OneOf(list(ALLOWED_FIELD_TYPES)))
    label = fields.String(required=True, validate=validate.Length(min=1, max=255))
    options = fields.List(fields.String(), required=False, allow_none=True)

    @validates_schema
    def validate_options(self, data, **kwargs):
        field_type = data.get("type")
        options = data.get("options")
        if field_type == "select" and (not options or len(options) < 1):
            raise ValidationError("Select fields require options.", field_name="options")
        if field_type != "select" and options:
            raise ValidationError("Only select fields can include options.", field_name="options")


class AIGenerateResponseSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    fields = fields.List(fields.Nested(AIGeneratedFieldSchema), required=True, validate=validate.Length(min=1))
