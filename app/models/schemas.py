# Model Schemas
from marshmallow import fields, validate, EXCLUDE

from app import ma


class SongSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True)
    duration = fields.Integer(required=True)
    uploaded_time = fields.DateTime()

    class Meta:
        fields = ("uploaded_time", "name", "duration", "id")
        unknown = EXCLUDE


class PodcastSchema(ma.SQLAlchemyAutoSchema):
    duration = fields.Integer(required=True)
    uploaded_time = fields.DateTime()
    host = fields.String(required=True, validate=validate.Length(min=1, max=100))
    participants = fields.List(fields.String(validate=validate.Length(min=1, max=100)))
    name = fields.String(validate=validate.Length(min=1, max=100), required=True)

    class Meta:
        fields = ("uploaded_time", "name", "duration", "id", "host", "participants")
        unknown = EXCLUDE


class AudioBookSchema(ma.SQLAlchemyAutoSchema):
    duration = fields.Integer(required=True)
    uploaded_time = fields.DateTime()
    author = fields.String(required=True, validate=validate.Length(min=1, max=100))
    narrator = fields.String(required=True, validate=validate.Length(min=1, max=100))
    title = fields.String(required=True, validate=validate.Length(min=1, max=100))

    class Meta:
        fields = ("uploaded_time", "duration", "id", "author", "narrator", "title")
        unknown = EXCLUDE
