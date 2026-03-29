from marshmallow import Schema, fields, validate


class ResponseCreateSchema(Schema):
    form_id = fields.Int(required=True)
    answers = fields.Dict(
        keys=fields.String(validate=validate.Length(min=1)),
        values=fields.Raw(),
        required=True,
        validate=validate.Length(min=1),
    )
    respondent_email = fields.Email(required=False, allow_none=True)


class ResponseOutputSchema(Schema):
    id = fields.Int(required=True)
    form_id = fields.Int(required=True)
    answers = fields.Dict(keys=fields.String(), values=fields.Raw(), required=True)
    respondent_email = fields.String(allow_none=True)
    submitted_at = fields.DateTime(required=True)
