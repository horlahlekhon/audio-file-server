from flask import request, current_app
from flask_restx import Resource
from werkzeug.exceptions import BadRequestKeyError

from app.api.audio.dto import AudioFilesDTO
from app.api.audio.service import AudioService
from app.utils import err_resp

api = AudioFilesDTO.api
data_resp = AudioFilesDTO.data_resp

@api.route("/<string:file_type>/", defaults={"audio_id": None})
@api.route("/<string:file_type>/<int:audio_id>")
class AudioGet(Resource):
    def get(self, file_type, audio_id=None):
        """ Get a specific audio file's data by its filetype and id """
        if audio_id is None:
            return AudioService.get_all(file_type)
        return AudioService.get(audio_id, file_type)

@api.route("/<string:file_type>/<int:audio_id>")
class AudioDeleteUpdate(Resource):

    def delete(self, file_type, audio_id):
        """ Delete a specific audio file's data by its filetype and id """
        return AudioService.delete(audio_id, file_type)

    def put(self, file_type, audio_id):
        """ Upload an audio file given its id and file type"""
        try:
            file = request.files[file_type]
            return AudioService.update(audio_id, file_type, file)
        except BadRequestKeyError as e:
            current_app.logger.exception("file not found in the request files", e)
            return err_resp("Unable to find file in request files.."
                            " please kindly use the filetype passed"
                            " ast path param as the key while uploading", "bad_request_400", 400)





@api.route("/create")
class AudioCreate(Resource):

    def post(self):
        data = request.get_json()
        return AudioService.create(data)
