from datetime import datetime
from pathlib import Path

from app.api.audio.podcast_service import PodcastService
from app.models.model import Podcast
from tests.utils.base import BaseTestCase


class TestPodcastService(BaseTestCase):

    def create_obj(self):
        req_data = {
            "name": "hight",
            "host": "dan",
            "participants": ["narrator", "narratee", "narrater"],
            "duration": 123456
        }
        s = Podcast(**req_data)
        self.db.session.add(s)
        self.db.session.commit()
        return s, req_data

    def test_get_object_by_id_audio_book(self):
        s, req_data = self.create_obj()
        resp = PodcastService.get(s.id)
        self.assertEquals(resp[0]["status"], True)
        self.assertEquals(resp[0]["podcast"]["name"], s.name)

    def test_reject_get_object_by_unknown_id(self):
        resp = PodcastService.get(300)
        self.assertEquals(resp[0]["status"], False)
        self.assertEquals(resp[1], 404)

    def test_create_song(self):
        req_data = {
            "name": "hight",
            "host": "dan",
            "participants": ["narrator", "narratee", "narrater"],
            "duration": 123456
        }
        resp = PodcastService.create(req_data)
        self.assertEquals(resp[0]["status"], True)
        self.assertEquals(resp[1], 200)
        self.assertEquals(resp[0]["podcast"]["host"], req_data["host"])
        pd = Podcast.query.filter_by(host=req_data["host"]).first()
        self.assertIsNotNone(pd)

    def test_reject_create_on_bad_data(self):
        req_data = {
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        resp = PodcastService.create(req_data)
        self.assertEquals(resp[0]["status"], False)
        self.assertEquals(resp[1], 400)
        errs = resp[0]["errors"]
        self.assertEquals(errs["name"], ["Missing data for required field."])
        self.assertEquals(errs["host"], ["Missing data for required field."])

    def test_update_song(self):
        s, req_data = self.create_obj()
        uploaded_time = datetime.now()
        file_path = Path("tests/utils/littleaudio.wav")
        resp = PodcastService.update(s.id, file_path, uploaded_time)
        self.assertIsNotNone(resp[0]["podcast"]["uploaded_time"])
        pd = Podcast.query.get(s.id)
        self.assertIsNotNone(pd)
        self.assertIsNotNone(pd.uploaded_time)

    def test_reject_update_given_unknown_id(self):
        uploaded_time = datetime.now()
        file_path = Path("tests/utils/littleaudio.wav")
        resp = PodcastService.update(3000, file_path, uploaded_time)
        self.assertEquals(resp[1], 404)
