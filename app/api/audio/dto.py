from flask_restx import Namespace, fields

from app.models.model import AudioBase


class AudioFilesDTO:
    api = Namespace("audio", description="Audio file related operations.")
    user = api.model(
        "Audio object",
        {
            "duration": fields.Integer,
            "name": fields.String,
            "author": fields.String,
            "uploaded_time": fields.DateTime,
            "host": fields.String,
            "participants": fields.List(fields.String),
            "narrator": fields.String,
            "title": fields.String,
            "id": fields.Integer,
        },
    )

    data_resp = api.model(
        "Audio Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "audio_file": fields.Nested(model=AudioBase),
        },
    )
