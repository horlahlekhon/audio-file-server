import datetime

from flask import current_app

from app import db
from app.models.model import Podcast
from app.models.schemas import PodcastSchema
from app.utils import err_resp, message, internal_err_resp, validation_error


class PodcastService:
    @staticmethod
    def get(pdcast_id):
        if not (song := Podcast.query.get(pdcast_id)):
            return err_resp("Podcast file not found", "audio_404", 404)
        try:
            podcast_data = PodcastService.load_data(song)

            resp = message(True, "Podcast data sent")
            resp["podcast"] = podcast_data
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def create(data):
        if errors := PodcastSchema().validate(data=data):
            return validation_error(False, errors), 400
        try:
            new_song = Podcast(name=data["name"], host=data["host"],
                               participants=data["participants"],
                               duration=data["duration"])
            db.session.add(new_song)
            db.session.commit()
            resp = message(True, "Podcast has been created.")
            resp["podcast"] = PodcastService.load_data(new_song)
            return resp, 200
        except Exception as reason:
            current_app.logger.exception(f"an error occur while creating Podcast: {reason}", reason)
            return internal_err_resp()

    @staticmethod
    def delete(audio_id):
        msg = message(True, "")
        if not (audio_book := Podcast.query.get(audio_id)):
            return msg
        db.session.delete(audio_book)
        db.session.commit()
        return msg

    @staticmethod
    def update(audio_id, file_path, uploaded_time):
        if not (podcast := Podcast.query.get(audio_id)):
            return err_resp("Podcast not found", "podcast_404", 404)
        if not file_path.exists() and file_path.is_file():
            return internal_err_resp("Unable to get the path where the upload is stored, please retry")
        try:
            podcast.uploaded_time = uploaded_time
            podcast.file_path = file_path.__str__()
            db.session.commit()
            podcast_data = PodcastService.load_data(podcast)
            resp = message(True, "Song data sent")
            resp["podcast"] = podcast_data
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_object(audio_id):
        return Podcast.query.get(audio_id)

    @staticmethod
    def get_all():
        books = Podcast.query.all()
        podcast_data = PodcastService.load_data(books)
        resp = message(True, "")
        resp["podcasts"] = podcast_data
        return resp, 200

    @staticmethod
    def load_data(podcast):
        """ Load audio's data

        Parameters:
        - AudioBook db object or a list of the object
        """
        podcast_schema = PodcastSchema()
        if isinstance(podcast, list):
            data = podcast_schema.dump(podcast, many=True)
            return data
        return podcast_schema.dump(podcast)
