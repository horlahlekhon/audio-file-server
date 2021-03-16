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
    def update(audio_id):
        if not (audio_book := Song.query.get(audio_id)):
            return err_resp("Song not found", "song_404", 404)
        try:
            audio_book.uploaded_time = datetime.datetime.now()
            db.session.commit()
            audiobook_data = SongService.load_data(audio_book)
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
        books = Song.query.all()
        audiobook_data = SongService.load_data(books)
        resp = message(True, "")
        resp["song"] = audiobook_data
        return resp, 200

    @staticmethod
    def load_data(song):
        """ Load audio's data

        Parameters:
        - AudioBook db object or a list of the object
        """
        audio_schema = SongSchema()
        if isinstance(song, list):
            data = audio_schema.dump(song, many=True)
            return data
        return audio_schema.dump(song)
