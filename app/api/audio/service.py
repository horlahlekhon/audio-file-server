import datetime
from pathlib import Path

from werkzeug.utils import secure_filename

from app.api.audio.audiobook_service import AudioBookService
from app.api.audio.podcast_service import PodcastService
from app.api.audio.song_service import SongService
from app.models.model import FiletypeEnum
from app.utils import err_resp
from config import Config


class AudioService:

    @staticmethod
    def get(audio_id, filetype: FiletypeEnum):
        """ Get audio file data by filetype and file id """

        resp = AudioService.audios[FiletypeEnum(filetype).value].get(audio_id)
        return resp

    @staticmethod
    def create(data: dict):
        try:
            filetype = data["filetype"]
            data.pop("filetype")
            resp = getattr(AudioService.audios[filetype], "create").__call__(data)
            return resp
        except KeyError as reason:
            return err_resp(f"{reason} is not a valid audio file type, try one"
                            f" of audio_book, song or podcast",
                            "400_badRequest", 400)

    audios = {
        "audio_book": AudioBookService,
        "podcast": PodcastService,
        "song": SongService
    }

    @staticmethod
    def delete(audio_id, file_type):
        resp = AudioService.audios[FiletypeEnum(file_type).value].delete(audio_id)
        return resp

    @staticmethod
    def update(audio_id, file_type, file):
        audio_service = AudioService.audios[FiletypeEnum(file_type).value]
        content_type = file.content_type
        if content_type.split("/")[0] != "audio":
            return err_resp("Only Audio file format is allowed", "invalid_audio_format", 400)
        audio = audio_service.get_object(audio_id)
        uploaded_time = datetime.datetime.now()
        if audio:
            fname = secure_filename(file.filename)
            fname = f"{uploaded_time}__{audio.id}__{fname}"
            save_path = AudioService.check_upload_dir(file_type) / fname
            file.save(save_path.__str__())
            resp = audio_service.update(audio_id, save_path, uploaded_time)
            return resp
        else:
            resp = err_resp("Audio data not found in database", "404_notfound", 404)
            return resp

    @staticmethod
    def check_upload_dir(filetype):
        upload_dir = Path(Config.UPLOAD_PATH) / filetype
        if upload_dir.exists() and upload_dir.is_dir():
            n_upload = upload_dir
            return n_upload
        Path(upload_dir).mkdir(parents=True, exist_ok=True, mode=0o777)
        return upload_dir

    @staticmethod
    def get_all(file_type):
        resp = AudioService.audios[FiletypeEnum(file_type).value].get_all()
        return resp
