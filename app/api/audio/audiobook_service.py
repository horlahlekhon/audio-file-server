import datetime
from pathlib import Path

from flask import current_app

from app import db
from app.models.model import AudioBook
from app.models.schemas import AudioBookSchema
from app.utils import err_resp, message, internal_err_resp, validation_error


class AudioBookService:

    @staticmethod
    def get(audio_id):
        if not (audio_book := AudioBook.query.get(audio_id)):
            return err_resp("Audio file not found", "audio_404", 404)
        try:
            audiobook_data = AudioBookService.load_data(audio_book)
            resp = message(True, "Podcast data sent")
            resp["audiobook"] = audiobook_data
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def create(data):
        if errors := AudioBookSchema().validate(data=data):
            return validation_error(False, errors), 400
        try:
            new_book = AudioBook(title=data["title"], author=data["author"], narrator=data["narrator"])
            db.session.add(new_book)
            db.session.commit()
            resp = message(True, "AudioBook has been created.")
            resp["audiobook"] = AudioBookService.load_data(new_book)
            return resp, 200
        except Exception as reason:
            current_app.logger.exception(f"an error occur while creating Audiobook: {reason}", reason)
            return internal_err_resp()

    @staticmethod
    def delete(audio_id):
        msg = message(True, "")
        if not (audio_book := AudioBook.query.get(audio_id)):
            return msg
        db.session.delete(audio_book)
        db.session.commit()
        return msg

    @staticmethod
    def update(audio_id, file_path: Path, uploaded_time):
        if not (audio_book := AudioBook.query.get(audio_id)):
            return err_resp("Audio file not found", "audio_404", 404)
        if not file_path.exists() and file_path.is_file():
            return internal_err_resp("Unable to get the path where the upload is stored, please retry")
        try:
            audio_book.uploaded_time = uploaded_time
            audio_book.file_path = file_path.__str__()
            db.session.commit()
            audiobook_data = AudioBookService.load_data(audio_book)
            resp = message(True, "Audiobook data sent")
            resp["audiobook"] = audiobook_data
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_object(audio_id):
        return AudioBook.query.get(audio_id)

    @staticmethod
    def get_all():
        books = AudioBook.query.all()
        audiobook_data = AudioBookService.load_data(books)
        resp = message(True, "")
        resp["audiobooks"] = audiobook_data
        return resp, 200

    @staticmethod
    def load_data(audiobook_data):
        """ Load audio's data

        Parameters:
        - AudioBook db object or a list of the object
        """
        from app.models.schemas import AudioBookSchema
        audio_schema = AudioBookSchema()
        if isinstance(audiobook_data, list):
            data = audio_schema.dump(audiobook_data, many=True)
            return data
        return audio_schema.dump(audiobook_data)
