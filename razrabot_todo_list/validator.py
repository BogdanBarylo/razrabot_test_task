from marshmallow import Schema, fields, validate


class TaskSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1,
                                                                  max=255))
    description = fields.String(validate=validate.Length(max=255))


class TaskUpdateSchema(Schema):
    title = fields.String(validate=validate.Length(min=1, max=255))
    description = fields.String(validate=validate.Length(max=255))
