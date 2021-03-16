import datetime

from flask import current_app

from app import db
from app.models.model import Song
from app.models.schemas import SongSchema
from app.utils import err_resp, message, internal_err_resp, validation_error


class SongService:
    @staticmethod
    def get(song_id):

        if not (song := Song.query.get(song_id)):
            return err_resp("Song not found", "audio_404", 404)
        try:
            song_data = SongService.load_data(song)

            resp = message(True, "Song data sent")
            resp["song"] = song_data
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def create(data):
        if errors := SongSchema().validate(data=data):
            return validation_error(False, errors), 400
        try:
            new_song = Song(name=data["name"], duration=data["duration"])
            db.session.add(new_song)
            db.session.commit()
            resp = message(True, "Song has been created.")
            resp["song"] = SongService.load_data(new_song)
            return resp, 200
        except Exception as reason:
            current_app.logger.exception(f"an error occur while creating Audiobook: {reason}", reason)
            return internal_err_resp(reason.__str__())

    @staticmethod
    def delete(audio_id):
        msg = message(True, "")
        if not (audio_book := Song.query.get(audio_id)):
            return msg
        db.session.delete(audio_book)
        db.session.commit()
        return msg

    @staticmethod
    def update(audio_id, file_path, uploaded_time):
        if not (song := Song.query.get(audio_id)):
            return err_resp("Song not found", "song_404", 404)
        if not file_path.exists() and file_path.is_file():
            return internal_err_resp("Unable to get the path where the upload is stored, please retry")
        try:
            song.uploaded_time = uploaded_time
            song.file_path = file_path.__str__()
            db.session.commit()
            audiobook_data = SongService.load_data(song)
            resp = message(True, "Song data updated")
            resp["song"] = audiobook_data
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp(error.__str__())

    @staticmethod
    def get_object(audio_id):
        return Song.query.get(audio_id)

    @staticmethod
    def get_all():
        songs = Song.query.all()
        song_data = SongService.load_data(songs)
        resp = message(True, "")
        resp["song"] = song_data
        return resp, 200

    @staticmethod
    def load_data(song):
        """ Load song's data

        Parameters:
        - AudioBook db object or a list of the object
        """
        song_schema = SongSchema()
        if isinstance(song, list):
            data = song_schema.dump(song, many=True)
            return data
        return song_schema.dump(song)
