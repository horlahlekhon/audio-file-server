import unittest

from app.models.schemas import AudioBookSchema, SongSchema, PodcastSchema


class TestModeSchemas(unittest.TestCase):

    def test_audio_book(self):
        req_data = {
            "title": "hight",
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        resp = AudioBookSchema().validate(req_data)
        self.assertEquals(resp, {})

    def test_audio_book_invalid(self):
        req_data = {
            # "title": "hight",
            # "author": "dan",
            # "narrator": "narrator",
            # "duration": 123456
        }
        resp = AudioBookSchema().validate(req_data)
        self.assertEquals(len(resp), 4)
        self.assertEquals(resp["title"], ["Missing data for required field."])
        self.assertEquals(resp["author"], ["Missing data for required field."])
        self.assertEquals(resp["narrator"], ["Missing data for required field."])
        self.assertEquals(resp["duration"], ["Missing data for required field."])

    def test_podcast(self):
        req_data = {
            "name": "hight",
            "host": "dan",
            "participants": ["narrator", "narratee", "narrater"],
            "duration": 123456
        }
        errors = PodcastSchema().validate(req_data)
        self.assertEquals(errors, {})

    def test_podcast_invalid(self):
        req_data = {}
        errors = PodcastSchema().validate(req_data)
        self.assertEquals(errors["name"], ["Missing data for required field."])
        self.assertEquals(errors["host"], ["Missing data for required field."])
        self.assertEquals(errors["duration"], ["Missing data for required field."])

    def test_song(self):
        req_data = {
            "name": "hight",
            "duration": 123456
        }
        errors = SongSchema().validate(req_data)
        self.assertEquals(errors, {})

    def test_song_invalid(self):
        req_data = {
            "name": "hight",
        }
        errors = SongSchema().validate(req_data)
        self.assertEquals(len(errors), 1)
        self.assertEquals(errors["duration"], ["Missing data for required field."])
