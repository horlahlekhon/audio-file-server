from app.api.audio.audiobook_service import AudioBookService
from app.models.model import AudioBook
from tests.utils.base import BaseTestCase


class TestAudiobookService(BaseTestCase):

    def test_get_object_by_id_audio_book(self):
        req_data = {
            "title": "hight",
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        s = AudioBook(**req_data)
        self.db.session.add(s)
        self.db.session.commit()
        resp = AudioBookService.get(s.id)
        self.assertEquals(resp[0]["status"], True)
        self.assertEquals(resp[0]["audiobook"]["narrator"], s.narrator)

    def test_reject_get_object_by_unknown_id(self):
        req_data = {
            "title": "hight",
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        s = AudioBook(**req_data)
        self.db.session.add(s)
        self.db.session.commit()
        resp = AudioBookService.get(300)
        self.assertEquals(resp[0]["status"], False)
        self.assertEquals(resp[1], 404)

    def test_create_audio_book(self):
        req_data = {
            "title": "hight",
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        resp = AudioBookService.create(req_data)
        self.assertEquals(resp[0]["status"], True)
        self.assertEquals(resp[1], 200)
        self.assertEquals(resp[0]["audiobook"]["title"], req_data["title"])

    def test_reject_create_on_bad_data(self):
        req_data = {
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        resp = AudioBookService.create(req_data)
        self.assertEquals(resp[0]["status"], False)
        self.assertEquals(resp[1], 400)
        errs = resp[0]["errors"]
        self.assertEquals(errs["title"], ["Missing data for required field."])

    def test_update_audio_book(self):
        req_data = {
            "title": "hight",
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        s = AudioBook(**req_data)
        self.db.session.add(s)
        self.db.session.commit()
        resp = AudioBookService.update(s.id)
        self.assertIsNotNone(resp[0]["audiobook"]["uploaded_time"])

    def test_reject_update_given_unknown_id(self):
        resp = AudioBookService.update(10020)
        self.assertEquals(resp[1], 404)

    def test_delete_song(self):
        req_data = {
            "title": "hight",
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        s = AudioBook(**req_data)
        self.db.session.add(s)
        self.db.session.commit()
        resp = AudioBookService.delete(s.id)
        self.assertEquals(resp["status"], True)
        aud = AudioBook.query.get(s.id)
        self.assertIsNone(aud)
