from datetime import datetime
from pathlib import Path

from app.api.audio.song_service import SongService
from app.models.model import Song
from tests.utils.base import BaseTestCase


class TestSongService(BaseTestCase):

    def create_obj(self):
        req_data = {
            "name": "hight",
            "duration": 123456
        }
        s = Song(**req_data)
        self.db.session.add(s)
        self.db.session.commit()
        return s, req_data

    def test_get_object_by_id_song(self):
        s, req_data = self.create_obj()
        resp = SongService.get(s.id)
        self.assertEquals(resp[0]["status"], True)
        self.assertEquals(resp[0]["song"]["name"], s.name)

    def test_reject_get_object_by_unknown_id(self):
        resp = SongService.get(300)
        self.assertEquals(resp[0]["status"], False)
        self.assertEquals(resp[1], 404)

    def test_create_song(self):
        req_data = {
            "name": "hight",
            "duration": 123456
        }
        resp = SongService.create(req_data)
        self.assertEquals(resp[0]["status"], True)
        self.assertEquals(resp[1], 200)
        self.assertEquals(resp[0]["song"]["name"], req_data["name"])
        pd = Song.query.filter_by(name=req_data["name"]).first()
        self.assertIsNotNone(pd)

    def test_reject_create_on_bad_data(self):
        req_data = {

        }
        resp = SongService.create(req_data)
        self.assertEquals(resp[0]["status"], False)
        self.assertEquals(resp[1], 400)
        errs = resp[0]["errors"]
        self.assertEquals(errs["name"], ["Missing data for required field."])
        self.assertEquals(errs["duration"], ["Missing data for required field."])

    def test_update_song(self):
        s, req_data = self.create_obj()
        uploaded_time = datetime.now()
        file_path = Path("tests/utils/littleaudio.wav")
        resp = SongService.update(s.id, file_path, uploaded_time)
        self.assertIsNotNone(resp[0]["song"]["uploaded_time"])
        pd = Song.query.get(s.id)
        self.assertIsNotNone(pd)
        self.assertIsNotNone(pd.uploaded_time)

    def test_reject_update_given_unknown_id(self):
        uploaded_time = datetime.now()
        file_path = Path("tests/utils/littleaudio.wav")
        resp = SongService.update(3000, file_path, uploaded_time)
        self.assertEquals(resp[1], 404)

    def test_delete_song(self):
        s, req_data = self.create_obj()
        resp = SongService.delete(s.id)
        self.assertEquals(resp["status"], True)
        sng = Song.query.get(s.id)
        self.assertIsNone(sng)
